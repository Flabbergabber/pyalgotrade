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

from pyalgotrade import broker
from pyalgotrade.broker import Order


class InstrumentTraits(object):

    __metaclass__ = abc.ABCMeta

    # Return the floating point value number rounded.
    @abc.abstractmethod
    def roundQuantity(self, quantity):
        raise NotImplementedError()


class OptionOrder(Order):
    """Base class for Option orders.

    .. note::

        This is a base class and should not be used directly.


    Valid ** type ** parameter
    values
    are:

    *OptionOrder.OptionType.OPTION_MARKET
    *OptionOrder.OptionType.OPTION_LIMIT
    *OptionOrder.OptionType.OPTION_STOP
    *OptionOrder.OptionType.OPTION_STOP_LIMIT
    """

    class OptionType(Order.Type):
        OPTION_MARKET = 5
        OPTION_LIMIT = 6
        OPTION_STOP = 7
        OPTION_STOP_LIMIT = 8

    class Right(object):
        PUT = 1
        CALL = 2

    def __init__(self, type_, action, instrument, quantity, right, strike, expiry, instrumentTraits):
        super(OptionOrder, self).__init__(type_, action, instrument, quantity, instrumentTraits)
        self.__right = right
        self.__strike = strike
        self.__expiry = expiry

    def getRight(self):
        return self.__right

    def setRight(self, right):
        self.__right = right

    def getStrike(self):
        return self.__strike

    def setStrike(self, strike):
        self.__strike = strike

    def getExpiry(self):
        return self.__expiry

    def setExpiry(self, expiry):
        self.__expiry = expiry


class OptionMarketOrder(OptionOrder):
    """Base class for market orders.

    .. note::

        This is a base class and should not be used directly.
    """

    def __init__(self, action, instrument, quantity, right, strike, expiry, onClose, instrumentTraits):
        super(OptionMarketOrder, self).__init__(self.OptionType.OPTION_MARKET, action, instrument, quantity, right, strike, expiry, instrumentTraits)
        self.__onClose = onClose

    def getFillOnClose(self):
        """Returns True if the order should be filled as close to the closing price as possible (Market-On-Close order)."""
        return self.__onClose


class OptionLimitOrder(OptionOrder):
    """Base class for limit orders.

    .. note::

        This is a base class and should not be used directly.
    """

    def __init__(self, action, instrument, limitPrice, quantity, right, strike, expiry, instrumentTraits):
        super(OptionLimitOrder, self).__init__(self.OptionType.OPTION_LIMIT, action, instrument, quantity, right, strike, expiry, instrumentTraits)
        self.__limitPrice = limitPrice

    def getLimitPrice(self):
        """Returns the limit price."""
        return self.__limitPrice


class OptionStopOrder(OptionOrder):
    """Base class for stop orders.

    .. note::

        This is a base class and should not be used directly.
    """

    def __init__(self, action, instrument, stopPrice, quantity, right, strike, expiry, instrumentTraits):
        super(OptionStopOrder, self).__init__(self.OptionType.OPTION_STOP, action, instrument, quantity, instrumentTraits)
        self.__stopPrice = stopPrice

    def getStopPrice(self):
        """Returns the stop price."""
        return self.__stopPrice


class OptionStopLimitOrder(OptionOrder):
    """Base class for stop limit orders.

    .. note::

        This is a base class and should not be used directly.
    """

    def __init__(self, action, instrument, stopPrice, limitPrice, quantity, right, strike, expiry, instrumentTraits):
        super(OptionStopLimitOrder, self).__init__(self.OptionType.OPTION_STOP_LIMIT, action, instrument, quantity,
                                                   instrumentTraits)
        self.__stopPrice = stopPrice
        self.__limitPrice = limitPrice

    def getStopPrice(self):
        """Returns the stop price."""
        return self.__stopPrice

    def getLimitPrice(self):
        """Returns the limit price."""
        return self.__limitPrice


class AbstractOptionBroker(broker.Broker):
    """Base class for brokers.

    .. note::

        This is a base class and should not be used directly.
    """
    def __init__(self):
        super(AbstractOptionBroker, self).__init__()

    @abc.abstractmethod
    def createOptionMarketOrder(self, action, instrument, quantity, right, strike, expiry, onClose=False):
        """Creates a Market order.
        A market order is an order to buy or sell a stock at the best available price.
        Generally, this type of order will be executed immediately. However, the price at which a market order will be executed
        is not guaranteed.

        :param action: The order action.
        :type action: Order.Action.BUY, or Order.Action.BUY_TO_COVER, or Order.Action.SELL or Order.Action.SELL_SHORT.
        :param instrument: Instrument identifier.
        :type instrument: string.
        :param quantity: Order quantity.
        :type quantity: int/float.
        :param onClose: True if the order should be filled as close to the closing price as possible (Market-On-Close order). Default is False.
        :type onClose: boolean.
        :rtype: A :class:`MarketOrder` subclass.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def createOptionLimitOrder(self, action, instrument, limitPrice, quantity, right, strike, expiry):
        """Creates a Limit order.
        A limit order is an order to buy or sell a stock at a specific price or better.
        A buy limit order can only be executed at the limit price or lower, and a sell limit order can only be executed at the
        limit price or higher.

        :param action: The order action.
        :type action: Order.Action.BUY, or Order.Action.BUY_TO_COVER, or Order.Action.SELL or Order.Action.SELL_SHORT.
        :param instrument: Instrument identifier.
        :type instrument: string.
        :param limitPrice: The order price.
        :type limitPrice: float
        :param quantity: Order quantity.
        :type quantity: int/float.
        :rtype: A :class:`LimitOrder` subclass.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def createOptionStopOrder(self, action, instrument, stopPrice, quantity, right, strike, expiry):
        """Creates a Stop order.
        A stop order, also referred to as a stop-loss order, is an order to buy or sell a stock once the price of the stock
        reaches a specified price, known as the stop price.
        When the stop price is reached, a stop order becomes a market order.
        A buy stop order is entered at a stop price above the current market price. Investors generally use a buy stop order
        to limit a loss or to protect a profit on a stock that they have sold short.
        A sell stop order is entered at a stop price below the current market price. Investors generally use a sell stop order
        to limit a loss or to protect a profit on a stock that they own.

        :param action: The order action.
        :type action: Order.Action.BUY, or Order.Action.BUY_TO_COVER, or Order.Action.SELL or Order.Action.SELL_SHORT.
        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: The trigger price.
        :type stopPrice: float
        :param quantity: Order quantity.
        :type quantity: int/float.
        :rtype: A :class:`StopOrder` subclass.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def createOptionStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity, right, strike, expiry):
        """Creates a Stop-Limit order.
        A stop-limit order is an order to buy or sell a stock that combines the features of a stop order and a limit order.
        Once the stop price is reached, a stop-limit order becomes a limit order that will be executed at a specified price
        (or better). The benefit of a stop-limit order is that the investor can control the price at which the order can be executed.

        :param action: The order action.
        :type action: Order.Action.BUY, or Order.Action.BUY_TO_COVER, or Order.Action.SELL or Order.Action.SELL_SHORT.
        :param instrument: Instrument identifier.
        :type instrument: string.
        :param stopPrice: The trigger price.
        :type stopPrice: float
        :param limitPrice: The price for the limit order.
        :type limitPrice: float
        :param quantity: Order quantity.
        :type quantity: int/float.
        :rtype: A :class:`StopLimitOrder` subclass.
        """
        raise NotImplementedError()