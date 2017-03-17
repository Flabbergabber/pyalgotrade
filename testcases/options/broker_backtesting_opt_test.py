import datetime

import testcases.common as common

from pyalgotrade import broker as stockbroker
from pyalgotrade.broker import backtesting as stockbacktesting
from pyalgotrade.broker import optbroker
from pyalgotrade.broker.optbroker import optbacktesting
from pyalgotrade import bar
from pyalgotrade import barfeed


class OrderUpdateCallback:
    def __init__(self, broker_):
        self.eventCount = 0
        self.events = []
        broker_.getOrderUpdatedEvent().subscribe(self.onOrderEvent)

    def onOrderEvent(self, broker_, orderEvent):
        self.eventCount += 1
        self.events.append(orderEvent)


class BarsBuilder(object):
    def __init__(self, instrument, frequency):
        self.__instrument = instrument
        self.__frequency = frequency
        self.__nextDateTime = datetime.datetime(2011, 1, 1)
        if frequency == bar.Frequency.TRADE:
            self.__delta = datetime.timedelta(milliseconds=1)
        elif frequency == bar.Frequency.SECOND:
            self.__delta = datetime.timedelta(seconds=1)
        elif frequency == bar.Frequency.MINUTE:
            self.__delta = datetime.timedelta(minutes=1)
        elif frequency == bar.Frequency.HOUR:
            self.__delta = datetime.timedelta(hours=1)
        elif frequency == bar.Frequency.DAY:
            self.__delta = datetime.timedelta(days=1)
        else:
            raise Exception("Invalid frequency")

    def getCurrentDateTime(self):
        return self.__nextDateTime

    def advance(self, sessionClose):
        if sessionClose:
            self.__nextDateTime = datetime.datetime(self.__nextDateTime.year, self.__nextDateTime.month, self.__nextDateTime.day)
            self.__nextDateTime += datetime.timedelta(days=1)
        else:
            self.__nextDateTime += self.__delta

    # sessionClose is True if the next bars should start at a different date.
    def nextBars(self, openPrice, highPrice, lowPrice, closePrice, volume=None, sessionClose=False):
        if volume is None:
            volume = closePrice*10
        bar_ = bar.BasicBar(self.__nextDateTime, openPrice, highPrice, lowPrice, closePrice, volume, closePrice, self.__frequency)
        ret = {self.__instrument: bar_}
        self.advance(sessionClose)
        return bar.Bars(ret)

    # sessionClose is True if the next bars should start at a different date.
    def nextBar(self, openPrice, highPrice, lowPrice, closePrice, volume=None, sessionClose=False):
        return self.nextBars(openPrice, highPrice, lowPrice, closePrice, volume, sessionClose)[self.__instrument]

    # sessionClose is True if the next bars should start at a different date.
    def nextTuple(self, openPrice, highPrice, lowPrice, closePrice, volume=None, sessionClose=False):
        ret = self.nextBars(openPrice, highPrice, lowPrice, closePrice, volume, sessionClose)
        return (ret.getDateTime(), ret)


class DecimalTraits(optbroker.InstrumentTraits):
    def __init__(self, decimals):
        self.__decimals = decimals

    def roundQuantity(self, quantity):
        return round(quantity, self.__decimals)


class BarFeed(barfeed.BaseBarFeed):
    def __init__(self, instrument, frequency):
        barfeed.BaseBarFeed.__init__(self, frequency)
        self.__builder = BarsBuilder(instrument, frequency)
        self.__nextBars = None

    def getCurrentDateTime(self):
        return self.__builder.getCurrentDateTime()

    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def join(self):
        raise NotImplementedError()

    def eof(self):
        raise NotImplementedError()

    def peekDateTime(self):
        raise NotImplementedError()

    def dispatchBars(self, openPrice, highPrice, lowPrice, closePrice, volume=None, sessionClose=False):
        self.__nextBars = self.__builder.nextBars(openPrice, highPrice, lowPrice, closePrice, volume, sessionClose)
        self.dispatch()

    def barsHaveAdjClose(self):
        raise True

    def getNextBars(self):
        return self.__nextBars


class BaseTestCase(common.TestCase):
    TestInstrument = "orcl"

    def buildBroker(self, *args, **kwargs):
        return optbacktesting.OptionBroker(*args, **kwargs)

    def buildBarFeed(self, *args, **kwargs):
        return BarFeed(*args, **kwargs)


class CommissionTestCase(common.TestCase):
    def testNoCommission(self):
        comm = optbacktesting.NoCommission()
        self.assertEqual(comm.calculate(None, 1, 1), 0)

    def testFixedPerTrade(self):
        comm = stockbacktesting.FixedPerTrade(1.2)
        order = optbacktesting.OptionMarketOrder(optbroker.Order.Action.BUY, "orcl", 1, optbroker.OptionOrder.Right.CALL, 20, "2016-01-01", False, stockbroker.IntegerTraits())
        self.assertEqual(comm.calculate(order, 1, 1), 1.2)

    def testTradePercentage(self):
        comm = stockbacktesting.TradePercentage(0.1)
        self.assertEqual(comm.calculate(None, 1, 1), 0.1)
        self.assertEqual(comm.calculate(None, 2, 2), 0.4)