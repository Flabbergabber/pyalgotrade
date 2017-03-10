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

from pyalgotrade.stratanalyzer import returns
from pyalgotrade import warninghelpers
from pyalgotrade import broker

from pyalgotrade.strategy.position import Position

import datetime


class OptionPosition(Position):
    """Base class for option positions.

    Positions are higher level abstractions for placing orders.
    They are escentially a pair of entry-exit orders and allow
    to track returns and PnL easier that placing orders manually.

    :param strategy: The strategy that this position belongs to.
    :type strategy: :class:`pyalgotrade.strategy.BaseStrategy`.
    :param entryOrder: The order used to enter the position.
    :type entryOrder: :class:`pyalgotrade.broker.Order`
    :param goodTillCanceled: True if the entry order should be set as good till canceled.
    :type goodTillCanceled: boolean.
    :param allOrNone: True if the orders should be completely filled or not at all.
    :type allOrNone: boolean.

    .. note::
        This is a base class and should not be used directly.
    """

    def __init__(self, strategy, entryOrder, goodTillCanceled, allOrNone):
        super(OptionPosition, self).__init__(strategy, entryOrder, goodTillCanceled, allOrNone)

        self.__expiry = None
        self.__right = None
        self.__strike = None

    def setExpiryDate(self, dateTime):
        self.__expiry = dateTime

    def getExpiryDate(self):
        return self.__expiry

    def setRight(self, right):
        self.__right = right

    def getRight(self):
        return self.__right

    def setStrike(self, strike):
        self.__strike = strike

    def getStrike(self):
        return self.__strike


class LongOptionPosition(OptionPosition):
    def __init__(self, strategy, instrument, stopPrice, limitPrice, quantity, right, strike, expiry, goodTillCanceled, allOrNone):
        if limitPrice is None and stopPrice is None:
            entryOrder = strategy.getBroker().createOptionMarketOrder(broker.Order.Action.BUY, instrument, quantity, right, strike, expiry, False)
        elif limitPrice is not None and stopPrice is None:
            entryOrder = strategy.getBroker().createOptionLimitOrder(broker.Order.Action.BUY, instrument, limitPrice, quantity, right, strike, expiry)
        elif limitPrice is None and stopPrice is not None:
            entryOrder = strategy.getBroker().createOptionStopOrder(broker.Order.Action.BUY, instrument, stopPrice, quantity, right, strike, expiry)
        elif limitPrice is not None and stopPrice is not None:
            entryOrder = strategy.getBroker().createOptionStopLimitOrder(broker.Order.Action.BUY, instrument, stopPrice, limitPrice, quantity, right, strike, expiry)
        else:
            assert(False)

        super(LongOptionPosition, self).__init__(strategy, entryOrder, goodTillCanceled, allOrNone)

    def buildExitOrder(self, stopPrice, limitPrice):
        quantity = self.getShares()
        assert(quantity > 0)
        if limitPrice is None and stopPrice is None:
            ret = self.getStrategy().getBroker().createOptionMarketOrder(broker.Order.Action.SELL, self.getInstrument(), quantity, self.getRight, self.getStrike, self.getExpiryDate, False)
        elif limitPrice is not None and stopPrice is None:
            ret = self.getStrategy().getBroker().createOptionLimitOrder(broker.Order.Action.SELL, self.getInstrument(), limitPrice, quantity,  self.getRight, self.getStrike, self.getExpiryDate)
        elif limitPrice is None and stopPrice is not None:
            ret = self.getStrategy().getBroker().createOptionStopOrder(broker.Order.Action.SELL, self.getInstrument(), stopPrice, quantity,  self.getRight, self.getStrike, self.getExpiryDate)
        elif limitPrice is not None and stopPrice is not None:
            ret = self.getStrategy().getBroker().createOptionStopLimitOrder(broker.Order.Action.SELL, self.getInstrument(), stopPrice, limitPrice, quantity, self.getRight, self.getStrike, self.getExpiryDate)
        else:
            assert(False)

        return ret
    
    def executeOptionOrder(self):
        raise NotImplementedError()


class ShortOptionPosition(OptionPosition):
    def __init__(self, strategy, instrument, stopPrice, limitPrice, quantity , right, strike, expiry, goodTillCanceled, allOrNone):
        if limitPrice is None and stopPrice is None:
            entryOrder = strategy.getBroker().createOptionMarketOrder(broker.Order.Action.SELL_SHORT, instrument, quantity, right, strike, expiry, False)
        elif limitPrice is not None and stopPrice is None:
            entryOrder = strategy.getBroker().createOptionLimitOrder(broker.Order.Action.SELL_SHORT, instrument, limitPrice, quantity, right, strike, expiry)
        elif limitPrice is None and stopPrice is not None:
            entryOrder = strategy.getBroker().createOptionStopOrder(broker.Order.Action.SELL_SHORT, instrument, stopPrice, quantity, right, strike, expiry)
        elif limitPrice is not None and stopPrice is not None:
            entryOrder = strategy.getBroker().createOptionStopLimitOrder(broker.Order.Action.SELL_SHORT, instrument, stopPrice, limitPrice, quantity, right, strike, expiry)
        else:
            assert(False)

        super(ShortOptionPosition, self).__init__(strategy, entryOrder, goodTillCanceled, allOrNone)

    def buildExitOrder(self, stopPrice, limitPrice):
        quantity = self.getShares() * -1
        assert(quantity > 0)
        if limitPrice is None and stopPrice is None:
            ret = self.getStrategy().getBroker().createOptionMarketOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), quantity, self.getRight, self.getStrike, self.getExpiryDate, False)
        elif limitPrice is not None and stopPrice is None:
            ret = self.getStrategy().getBroker().createOptionLimitOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), limitPrice, quantity, self.getRight, self.getStrike, self.getExpiryDate)
        elif limitPrice is None and stopPrice is not None:
            ret = self.getStrategy().getBroker().createOptionStopOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), stopPrice, quantity, self.getRight, self.getStrike, self.getExpiryDate)
        elif limitPrice is not None and stopPrice is not None:
            ret = self.getStrategy().getBroker().createOptionStopLimitOrder(broker.Order.Action.BUY_TO_COVER, self.getInstrument(), stopPrice, limitPrice, quantity, self.getRight, self.getStrike, self.getExpiryDate)
        else:
            assert(False)

        return ret
        
    def executeOptionOrder(self):
        raise NotImplementedError()
