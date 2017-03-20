# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
import logging

import pyalgotrade.broker
from pyalgotrade.strategy import BaseStrategy
from pyalgotrade.broker.optbroker.optbacktesting import OptionBroker
from . import optposition
from .strategytransferobject import StrategyTransferObject

class OptionBaseStrategy(BaseStrategy):
    """Base class for strategies.

    :param barFeed: The bar feed that will supply the bars.
    :type barFeed: :class:`pyalgotrade.barfeed.BaseBarFeed`.
    :param broker: The broker that will handle orders.
    :type broker: :class:`pyalgotrade.broker.Broker`.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, barFeed, broker):
        super(OptionBaseStrategy, self).__init__(barFeed, broker)

    def optionMarketOrder(self, instrument, quantity, right, strike, expiry, onClose=False, goodTillCanceled=False,
                          allOrNone=False):
        """Submits a market order.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param quantity: The amount of shares. Positive means buy, negative means sell.
        :type quantity: int/float.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.


        :param onClose: True if the order should be filled as close to the closing price as possible (Market-On-Close order). Default is False.
        :type onClose: boolean.
        :param goodTillCanceled: True if the order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the order should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`pyalgotrade.broker.MarketOrder` submitted.
        """

        ret = None
        if quantity > 0:
            ret = self.getBroker().createOptionMarketOrder(pyalgotrade.broker.Order.Action.BUY, instrument, quantity, right,
                                                     strike, expiry, onClose)
        elif quantity < 0:
            ret = self.getBroker().createOptionMarketOrder(pyalgotrade.broker.Order.Action.SELL, instrument, quantity * -1,
                                                     right, strike, expiry, onClose)
        if ret:
            ret.setGoodTillCanceled(goodTillCanceled)
            ret.setAllOrNone(allOrNone)
            self.getBroker().submitOrder(ret)
        return ret

    def optionLimitOrder(self, instrument, limitPrice, quantity, right, strike, expiry, goodTillCanceled=False,
                         allOrNone=False):
        """Submits a limit order.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param limitPrice: Limit price.
        :type limitPrice: float.
        :param quantity: The amount of shares. Positive means buy, negative means sell.
        :type quantity: int/float.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.


        :param goodTillCanceled: True if the order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the order should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`pyalgotrade.broker.LimitOrder` submitted.
        """

        ret = None
        if quantity > 0:
            ret = self.getBroker().createOptionLimitOrder(pyalgotrade.broker.Order.Action.BUY, instrument, limitPrice,
                                                    quantity, right, strike, expiry)
        elif quantity < 0:
            ret = self.getBroker().createOptionLimitOrder(pyalgotrade.broker.Order.Action.SELL, instrument, limitPrice,
                                                    quantity * -1, right, strike, expiry)
        if ret:
            ret.setGoodTillCanceled(goodTillCanceled)
            ret.setAllOrNone(allOrNone)
            self.getBroker().submitOrder(ret)
        return ret

    def optionStopOrder(self, instrument, stopPrice, quantity, right, strike, expiry, goodTillCanceled=False,
                        allOrNone=False):
        """Submits a stop order.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: Stop price.
        :type stopPrice: float.
        :param quantity: The amount of shares. Positive means buy, negative means sell.
        :type quantity: int/float.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the order should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`pyalgotrade.broker.StopOrder` submitted.
        """

        ret = None
        if quantity > 0:
            ret = self.getBroker().createOptionStopOrder(pyalgotrade.broker.Order.Action.BUY, instrument, stopPrice, quantity,
                                                         right, strike, expiry)
        elif quantity < 0:
            ret = self.getBroker().createOptionStopOrder(pyalgotrade.broker.Order.Action.SELL, instrument, stopPrice,
                                                   quantity * -1, right, strike, expiry)
        if ret:
            ret.setGoodTillCanceled(goodTillCanceled)
            ret.setAllOrNone(allOrNone)
            self.getBroker().submitOrder(ret)
        return ret

    def optionStopLimitOrder(self, instrument, stopPrice, limitPrice, quantity, right, strike, expiry,
                             goodTillCanceled=False, allOrNone=False):
        """Submits a stop limit order.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: Stop price.
        :type stopPrice: float.
        :param limitPrice: Limit price.
        :type limitPrice: float.
        :param quantity: The amount of shares. Positive means buy, negative means sell.
        :type quantity: int/float.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.


        :param goodTillCanceled: True if the order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the order should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`pyalgotrade.broker.StopLimitOrder` submitted.
        """

        ret = None
        if quantity > 0:
            ret = self.getBroker().createOptionStopLimitOrder(pyalgotrade.broker.Order.Action.BUY, instrument, stopPrice,
                                                        limitPrice, quantity, right, strike, expiry)
        elif quantity < 0:
            ret = self.getBroker().createOptionStopLimitOrder(pyalgotrade.broker.Order.Action.SELL, instrument, stopPrice,
                                                        limitPrice, quantity * -1, right, strike, expiry)
        if ret:
            ret.setGoodTillCanceled(goodTillCanceled)
            ret.setAllOrNone(allOrNone)
            self.getBroker().submitOrder(ret)
        return ret

    def enterOptionLong(self, instrument, quantity, right, strike, expiry, goodTillCanceled=False, allOrNone=False):
        """Generates a buy :class:`pyalgotrade.broker.MarketOrder` to enter a long position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.


        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.LongOptionPosition(self, instrument, None, None, quantity, right, strike,
                                                                expiry, goodTillCanceled, allOrNone)

    def enterOptionLongCall(self, instrument, quantity, right, strike, expiry, goodTillCanceled=False, allOrNone=False):
        """Generates a buy :class:`pyalgotrade.broker.MarketOrder` to enter a long position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.


        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.LongOptionPosition(self, instrument, None, None, quantity, right, strike,
                                                                expiry, goodTillCanceled, allOrNone)

    def enterOptionShort(self, instrument, quantity, right, strike, expiry, goodTillCanceled=False, allOrNone=False):
        """Generates a sell short :class:`pyalgotrade.broker.MarketOrder` to enter a short position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.ShortOptionPosition(self, instrument, None, None, quantity, right, strike,
                                                                 expiry, goodTillCanceled, allOrNone)

    def enterOptionLongLimit(self, instrument, limitPrice, quantity, right, strike, expiry, goodTillCanceled=False,
                             allOrNone=False):
        """Generates a buy :class:`pyalgotrade.broker.LimitOrder` to enter a long position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param limitPrice: Limit price.
        :type limitPrice: float.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.LongOptionPosition(self, instrument, None, limitPrice, quantity, right,
                                                                strike, expiry, goodTillCanceled, allOrNone)

    def enterOptionShortLimit(self, instrument, limitPrice, quantity, right, strike, expiry, goodTillCanceled=False,
                              allOrNone=False):
        """Generates a sell short :class:`pyalgotrade.broker.LimitOrder` to enter a short position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param limitPrice: Limit price.
        :type limitPrice: float.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.ShortOptionPosition(self, instrument, None, limitPrice, quantity, right,
                                                                 strike, expiry, goodTillCanceled, allOrNone)

    def enterOptionLongStop(self, instrument, stopPrice, quantity, right, strike, expiry, goodTillCanceled=False,
                            allOrNone=False):
        """Generates a buy :class:`pyalgotrade.broker.StopOrder` to enter a long position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: Stop price.
        :type stopPrice: float.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.LongOptionPosition(self, instrument, stopPrice, None, quantity, right,
                                                                strike, expiry, goodTillCanceled, allOrNone)

    def enterOptionShortStop(self, instrument, stopPrice, quantity, right, strike, expiry, goodTillCanceled=False,
                             allOrNone=False):
        """Generates a sell short :class:`pyalgotrade.broker.StopOrder` to enter a short position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: Stop price.
        :type stopPrice: float.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.ShortOptionPosition(self, instrument, stopPrice, None, quantity, right,
                                                                 strike, expiry, goodTillCanceled, allOrNone)

    def enterOptionLongStopLimit(self, instrument, stopPrice, limitPrice, quantity, right, strike, expiry,
                                 goodTillCanceled=False, allOrNone=False):
        """Generates a buy :class:`pyalgotrade.broker.StopLimitOrder` order to enter a long position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: Stop price.
        :type stopPrice: float.
        :param limitPrice: Limit price.
        :type limitPrice: float.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.LongOptionPosition(self, instrument, stopPrice, limitPrice, quantity,
                                                                right, strike, expiry, goodTillCanceled, allOrNone)

    def enterOptionShortStopLimit(self, instrument, stopPrice, limitPrice, quantity, right, strike, expiry,
                                  goodTillCanceled=False, allOrNone=False):
        """Generates a sell short :class:`pyalgotrade.broker.StopLimitOrder` order to enter a short position.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: The Stop price.
        :type stopPrice: float.
        :param limitPrice: Limit price.
        :type limitPrice: float.
        :param quantity: Entry order quantity.
        :type quantity: int.

        :param right: PUT or CALL.
        :type right: Right.
        :param strike: strike price.
        :type strike: float.
        :param expiry: expiry price.
        :type expiry: date.

        :param goodTillCanceled: True if the entry order is good till canceled. If False then the order gets automatically canceled when the session closes.
        :type goodTillCanceled: boolean.
        :param allOrNone: True if the orders should be completely filled or not at all.
        :type allOrNone: boolean.
        :rtype: The :class:`optposition.Position` entered.
        """

        return optposition.ShortOptionPosition(self, instrument, stopPrice, limitPrice, quantity,
                                                                 right, strike, expiry, goodTillCanceled, allOrNone)


class OptionBacktestingStrategy(OptionBaseStrategy):
    """Base class for backtesting strategies.

    :param barFeed: The bar feed to use to backtest the strategy.
    :type barFeed: :class:`pyalgotrade.barfeed.BaseBarFeed`.
    :param cash_or_brk: The starting capital or a broker instance.
    :type cash_or_brk: int/float or :class:`pyalgotrade.broker.Broker`.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, barFeed, cash_or_brk=1000000):
        # The broker should subscribe to barFeed events before the strategy.
        # This is to avoid executing orders submitted in the current tick.

        if isinstance(cash_or_brk, pyalgotrade.broker.Broker):
            broker = cash_or_brk
        else:
            broker = OptionBroker(cash_or_brk, barFeed)

        OptionBaseStrategy.__init__(self, barFeed, broker)
        self.__useAdjustedValues = False
        self.setUseEventDateTimeInLogs(True)
        self.setDebugMode(True)
        self.__strategyTransferObject = StrategyTransferObject()

    def getUseAdjustedValues(self):
        self.attachAnalyzer()
        return self.__useAdjustedValues

    def setUseAdjustedValues(self, useAdjusted):
        self.getFeed().setUseAdjustedValues(useAdjusted)
        self.getBroker().setUseAdjustedValues(useAdjusted)
        self.__useAdjustedValues = useAdjusted

    def setDebugMode(self, debugOn):
        """Enable/disable debug level messages in the strategy and backtesting broker.
        This is enabled by default."""
        level = logging.DEBUG if debugOn else logging.INFO
        self.getLogger().setLevel(level)
        self.getBroker().getLogger().setLevel(level)

    def onEnterOk(self, position):
        # TODO Add Buy to result output object with date and price
        execInfo = position.getEntryOrder().getExecutionInfo()
        inst = position.getInstrument()
        action = pyalgotrade.broker.Order.Action.BUY
        self.__strategyTransferObject.recordBuySell(action, inst, execInfo.getDateTime(), execInfo.getPrice())

    def onExitOk(self, position):
        # TODO Add Sell to result output object with date and price
        execInfo = position.getExitOrder().getExecutionInfo()
        inst = position.getInstrument()
        action = pyalgotrade.broker.Order.Action.SELL
        self.__strategyTransferObject.recordBuySell(action, inst, execInfo.getDateTime(), execInfo.getPrice())

    def onStart(self):
        # TODO Add initial Equity
        self.__strategyTransferObject.setInitialEquity(self.getBroker().getEquity())

    def onFinish(self, bars):
        # TODO Add final Equity to result output object
        # TODO Dump data from output object to json file
        self.__strategyTransferObject.setFinalEquity(self.getBroker().getEquity())
        self.__strategyTransferObject.dumpToFile()
