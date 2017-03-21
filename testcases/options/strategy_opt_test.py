import datetime
import testcases.common as common

from pyalgotrade.strategy import optstrategy
from pyalgotrade.broker import optbroker
from pyalgotrade.barfeed import yahoofeed


def get_by_datetime_or_date(dict_, dateTimeOrDate):
    ret = dict_.get(dateTimeOrDate, [])
    if len(ret) == 0 and isinstance(dateTimeOrDate, datetime.datetime):
        ret = dict_.get(dateTimeOrDate.date(), [])
    return ret


class TestStrategy(optstrategy.OptionBacktestingStrategy):
    def __init__(self, barFeed, cash):
        optstrategy.OptionBacktestingStrategy.__init__(self, barFeed, cash)

        # Maps dates to a tuple of (method, params)
        self.__orderEntry = {}

        self.__brokerOrdersGTC = False
        self.orderUpdatedCalls = 0
        self.onStartCalled = False
        self.onIdleCalled = False
        self.onFinishCalled = False

    def addOrder(self, dateTime, method, *args, **kwargs):
        self.__orderEntry.setdefault(dateTime, [])
        self.__orderEntry[dateTime].append((method, args, kwargs))

    def setBrokerOrdersGTC(self, gtc):
        self.__brokerOrdersGTC = gtc

    def onStart(self):
        self.onStartCalled = True

    def onIdle(self):
        self.onIdleCalled = True

    def onFinish(self, bars):
        self.onFinishCalled = True

    def onOrderUpdated(self, order):
        self.orderUpdatedCalls += 1

    def onBars(self, bars):
        dateTime = bars.getDateTime()

        # Check order entry.
        for meth, args, kwargs in get_by_datetime_or_date(self.__orderEntry, dateTime):
            order = meth(*args, **kwargs)
            order.setGoodTillCanceled(self.__brokerOrdersGTC)
            self.getBroker().submitOrder(order)


class StrategyTestCase(common.TestCase):
    TestInstrument = "doesntmatter"

    def loadDailyBarFeed(self):
        barFeed = yahoofeed.Feed()
        barFeed.addBarsFromCSV(StrategyTestCase.TestInstrument, common.get_data_file_path("orcl-2000-yahoofinance.csv"))
        return barFeed

    def createStrategy(self):
        barFeed = self.loadDailyBarFeed()
        strat = TestStrategy(barFeed, 1000)
        return strat


class BrokerOrderTestCase(StrategyTestCase):
    def testMarketOrder(self):
        strat = self.createStrategy()

        o = strat.getBroker().createOptionMarketOrder(optbroker.Order.Action.BUY, StrategyTestCase.TestInstrument, 1
                                                      , optbroker.OptionOrder.Right.CALL, 20, "2016-01-01")
        strat.getBroker().submitOrder(o)
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEqual(strat.orderUpdatedCalls, 3)


class StrategyOrderTestCase(StrategyTestCase):
    def testOrder(self):
        strat = self.createStrategy()

        o = strat.optionMarketOrder(StrategyTestCase.TestInstrument, 1, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01")
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEqual(strat.orderUpdatedCalls, 3)

    def testMarketOrderBuy(self):
        strat = self.createStrategy()

        o = strat.optionMarketOrder(StrategyTestCase.TestInstrument, 1, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01")
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.BUY)
        self.assertEquals(o.getQuantity(), 1)
        self.assertEquals(o.getFilled(), 1)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)

    def testMarketOrderSell(self):
        strat = self.createStrategy()

        o = strat.optionMarketOrder(StrategyTestCase.TestInstrument, -2, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01")
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.SELL)
        self.assertEquals(o.getQuantity(), 2)
        self.assertEquals(o.getFilled(), 2)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)

    def testLimitOrderBuy(self):
        strat = self.createStrategy()

        o = strat.optionLimitOrder(StrategyTestCase.TestInstrument, 60, 1, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01", True)
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.BUY)
        self.assertEquals(o.getAvgFillPrice(), 56.13)
        self.assertEquals(o.getQuantity(), 1)
        self.assertEquals(o.getFilled(), 1)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)

    def testLimitOrderSell(self):
        strat = self.createStrategy()

        o = strat.optionLimitOrder(StrategyTestCase.TestInstrument, 60, -3, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01", False)
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.SELL)
        self.assertEquals(o.getAvgFillPrice(), 124.62)
        self.assertEquals(o.getQuantity(), 3)
        self.assertEquals(o.getFilled(), 3)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)

    def testStopOrderBuy(self):
        strat = self.createStrategy()

        o = strat.optionStopOrder(StrategyTestCase.TestInstrument, 100, 1, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01", False)
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.BUY)
        self.assertEquals(o.getAvgFillPrice(), 124.62)
        self.assertEquals(o.getQuantity(), 1)
        self.assertEquals(o.getFilled(), 1)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)

    def testStopOrderSell(self):
        strat = self.createStrategy()

        o = strat.optionStopOrder(StrategyTestCase.TestInstrument, 55, -2, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01", True)
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.SELL)
        self.assertEquals(o.getAvgFillPrice(), 55)
        self.assertEquals(o.getQuantity(), 2)
        self.assertEquals(o.getFilled(), 2)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)
        self.assertEqual(o.getExecutionInfo().getDateTime(), datetime.datetime(2000, 1, 19))

    def testStopLimitOrderBuy(self):
        strat = self.createStrategy()

        o = strat.optionStopLimitOrder(StrategyTestCase.TestInstrument, 110, 100, 1, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01", True)
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.BUY)
        self.assertEquals(o.getAvgFillPrice(), 100)
        self.assertEquals(o.getQuantity(), 1)
        self.assertEquals(o.getFilled(), 1)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)
        self.assertEqual(o.getExecutionInfo().getDateTime(), datetime.datetime(2000, 1, 5))

    def testStopLimitOrderSell(self):
        strat = self.createStrategy()

        o = strat.optionStopLimitOrder(StrategyTestCase.TestInstrument, 100, 110, -2, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01", True)
        strat.run()
        self.assertTrue(o.isFilled())
        self.assertEquals(o.getAction(), optbroker.Order.Action.SELL)
        self.assertEquals(o.getAvgFillPrice(), 110)
        self.assertEquals(o.getQuantity(), 2)
        self.assertEquals(o.getFilled(), 2)
        self.assertEquals(o.getRemaining(), 0)
        self.assertEqual(strat.orderUpdatedCalls, 3)
        self.assertEqual(o.getExecutionInfo().getDateTime(), datetime.datetime(2000, 1, 10))


class OptionalOverridesTestCase(StrategyTestCase):
    def testOnStartIdleFinish(self):
        strat = self.createStrategy()
        strat.run()
        self.assertTrue(strat.onStartCalled)
        self.assertTrue(strat.onFinishCalled)
        self.assertFalse(strat.onIdleCalled)
