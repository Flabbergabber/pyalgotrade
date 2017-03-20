import unittest
import datetime

from pyalgotrade.broker import optbroker
from pyalgotrade import broker as stockbroker
from pyalgotrade.broker.optbroker import optfillstrategy
from pyalgotrade.broker import fillstrategy as stockfillstrategy
from pyalgotrade.broker.optbroker import optbacktesting

import broker_backtesting_opt_test
from pyalgotrade import bar

class BaseTestCase(unittest.TestCase):
    TestInstrument = "orcl"


class FreeFunctionsTestCase(BaseTestCase):
    def testStopOrderTriggerBuy(self):
        barsBuilder = broker_backtesting_opt_test.BarsBuilder(BaseTestCase.TestInstrument, bar.Frequency.MINUTE)
        # Bar is below
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(5, 5, 5, 5)), None)
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(5, 6, 4, 5)), None)
        # High touches
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(5, 10, 4, 9)), 10)
        # High penetrates
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(5, 11, 4, 9)), 10)
        # Open touches
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(10, 10, 10, 10)), 10)
        # Open is above
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(11, 12, 4, 9)), 11)
        # Bar gaps above
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(12, 13, 11, 12)), 12)

    def testStopOrderTriggerSell(self):
        barsBuilder = broker_backtesting_opt_test.BarsBuilder(BaseTestCase.TestInstrument, bar.Frequency.MINUTE)
        # Bar is above
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(15, 15, 15, 15)), None)
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(15, 16, 11, 15)), None)
        # Low touches
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(15, 16, 10, 11)), 10)
        # Low penetrates
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(15, 16, 9, 11)), 10)
        # Open touches
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(10, 10, 10, 10)), 10)
        # Open is below
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(9, 12, 4, 9)), 9)
        # Bar gaps below
        self.assertEqual(stockfillstrategy.get_stop_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(8, 9, 6, 9)), 8)

    def testLimitOrderTriggerBuy(self):
        barsBuilder = broker_backtesting_opt_test.BarsBuilder(BaseTestCase.TestInstrument, bar.Frequency.MINUTE)
        # Bar is above
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(15, 15, 15, 15)), None)
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(15, 16, 11, 15)), None)
        # Low touches
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(15, 16, 10, 11)), 10)
        # Low penetrates
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(15, 16, 9, 11)), 10)
        # Open touches
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(10, 10, 10, 10)), 10)
        # Open is below
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(9, 12, 4, 9)), 9)
        # Bar gaps below
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.BUY, 10, False, barsBuilder.nextBar(8, 9, 6, 9)), 8)

    def testLimitOrderTriggerSell(self):
        barsBuilder = broker_backtesting_opt_test.BarsBuilder(BaseTestCase.TestInstrument, bar.Frequency.MINUTE)
        # Bar is below
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(5, 5, 5, 5)), None)
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(5, 6, 4, 5)), None)
        # High touches
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(5, 10, 4, 9)), 10)
        # High penetrates
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(5, 11, 4, 9)), 10)
        # Open touches
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(10, 10, 10, 10)), 10)
        # Open is above
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(11, 12, 4, 9)), 11)
        # Bar gaps above
        self.assertEqual(stockfillstrategy.get_limit_price_trigger(optbroker.Order.Action.SELL, 10, False, barsBuilder.nextBar(12, 13, 11, 12)), 12)


class DefaultStrategyTestCase(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.barsBuilder = broker_backtesting_opt_test.BarsBuilder(BaseTestCase.TestInstrument, bar.Frequency.MINUTE)
        self.strategy = optfillstrategy.OptionDefaultStrategy()

    def __getFilledMarketOrder(self, quantity, price):
        order = optbacktesting.OptionMarketOrder(
            optbroker.Order.Action.BUY,
            BaseTestCase.TestInstrument,
            quantity,
            False,
            optbroker.OptionOrder.Right.CALL,
            20,
            "2016-01-01",
            stockbroker.IntegerTraits()
        )
        order.setState(stockbroker.Order.State.ACCEPTED)
        order.addExecutionInfo(stockbroker.OrderExecutionInfo(price, quantity, 0, datetime.datetime.now()))
        return order

    def testVolumeLimitPerBar(self):
        volume = 100
        self.strategy.onBars(None, self.barsBuilder.nextBars(11, 12, 4, 9, volume))
        self.assertEquals(self.strategy.getVolumeLeft()[BaseTestCase.TestInstrument], 25)
        self.assertEquals(self.strategy.getVolumeUsed()[BaseTestCase.TestInstrument], 0)

        self.strategy.onOrderFilled(None, self.__getFilledMarketOrder(24, 11))
        self.assertEquals(self.strategy.getVolumeLeft()[BaseTestCase.TestInstrument], 1)
        self.assertEquals(self.strategy.getVolumeUsed()[BaseTestCase.TestInstrument], 24)

        with self.assertRaisesRegexp(Exception, "Invalid fill quantity 25. Not enough volume left 1"):
            self.strategy.onOrderFilled(None, self.__getFilledMarketOrder(25, 11))
        self.assertEquals(self.strategy.getVolumeLeft()[BaseTestCase.TestInstrument], 1)
        self.assertEquals(self.strategy.getVolumeUsed()[BaseTestCase.TestInstrument], 24)