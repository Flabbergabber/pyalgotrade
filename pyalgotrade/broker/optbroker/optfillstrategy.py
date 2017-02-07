# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import abc

from pyalgotrade.broker import fillstrategy
import pyalgotrade.bar


class OptionFillStrategy(fillstrategy.FillStrategy):
    def __init__(self):
        super(OptionFillStrategy, self).__init__()

    @abc.abstractmethod
    def fillOptionOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a market order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.MarketOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()
        
    @abc.abstractmethod
    def fillOptionLimitOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a limit order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.LimitOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def fillOptionStopOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a stop order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.StopOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def fillOptionStopLimitOrder(self, broker_, order, bar):
        """Override to return the fill price and quantity for a stop limit order or None if the order can't be filled
        at the given time.

        :param broker_: The broker.
        :type broker_: :class:`Broker`
        :param order: The order.
        :type order: :class:`pyalgotrade.broker.StopLimitOrder`
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`
        :rtype: A :class:`FillInfo` or None if the order should not be filled.
        """
        raise NotImplementedError()


class OptionDefaultStrategy(OptionFillStrategy, fillstrategy.DefaultStrategy):
    """
    Default fill strategy for options.

    :param volumeLimit: The proportion of the volume that orders can take up in a bar. Must be > 0 and <= 1.
        If None, then volume limit is not checked.
    :type volumeLimit: float

    """

    def __init__(self, volumeLimit=0.25):
        OptionFillStrategy.__init__(self)
        fillstrategy.DefaultStrategy.__init__(self, volumeLimit)

    def fillOptionOrder(self, broker_, order, bar):
        # Calculate the fill size for the order.
        fillSize = self._calculateFillSize(broker_, order, bar)
        if fillSize == 0:
            broker_.getLogger().debug(
                "Not enough volume to fill %s market order [%s] for %s share/s" % (
                    order.getInstrument(),
                    order.getId(),
                    order.getRemaining()
                )
            )
            return None

        # Unless its a fill-on-close order, use the open price.
        if order.getFillOnClose():
            price = bar.getClose(broker_.getUseAdjustedValues())
        else:
            price = bar.getOpen(broker_.getUseAdjustedValues())
        assert price is not None
        


        # Don't slip prices when the bar represents the trading activity of a single trade.
        if bar.getFrequency() != pyalgotrade.bar.Frequency.TRADE:
            price = self._slippageModel.calculatePrice(
                order, price, fillSize, bar, self._volumeUsed[order.getInstrument()]
            )
            
        # If expiry date is met, prix a 0
#        if bar.getDateTime() >= order.getExpiry():
#            price=0
            
            
        return fillstrategy.FillInfo(price, fillSize)
    
    def fillOptionLimitOrder(self, broker_, order, bar):
        # Calculate the fill size for the order.
        fillSize = self._calculateFillSize(broker_, order, bar)
        if fillSize == 0:
            broker_.getLogger().debug("Not enough volume to fill %s limit order [%s] for %s share/s" % (
                order.getInstrument(), order.getId(), order.getRemaining())
            )
            return None

        ret = None
        price = fillstrategy.get_limit_price_trigger(order.getAction(), order.getLimitPrice(), broker_.getUseAdjustedValues(), bar)
        if price is not None:
            # If expiry date is met, prix a 0
 #           if bar.getDateTime() >= order.getExpiry():
#                price=0
         
            ret = fillstrategy.FillInfo(price, fillSize)
        return ret

    def fillOptionStopOrder(self, broker_, order, bar):
        ret = None

        # First check if the stop price was hit so the market order becomes active.
        stopPriceTrigger = None
        if not order.getStopHit():
            stopPriceTrigger = fillstrategy.get_stop_price_trigger(
                order.getAction(),
                order.getStopPrice(),
                broker_.getUseAdjustedValues(),
                bar
            )
            order.setStopHit(stopPriceTrigger is not None)

        # If the stop price was hit, check if we can fill the market order.
        if order.getStopHit():
            # Calculate the fill size for the order.
            fillSize = self._calculateFillSize(broker_, order, bar)
            if fillSize == 0:
                broker_.getLogger().debug("Not enough volume to fill %s stop order [%s] for %s share/s" % (
                    order.getInstrument(),
                    order.getId(),
                    order.getRemaining()
                ))
                return None

            # If we just hit the stop price we'll use it as the fill price.
            # For the remaining bars we'll use the open price.
            if stopPriceTrigger is not None:
                price = stopPriceTrigger
            else:
                price = bar.getOpen(broker_.getUseAdjustedValues())
            assert price is not None

            # Don't slip prices when the bar represents the trading activity of a single trade.
            if bar.getFrequency() != pyalgotrade.bar.Frequency.TRADE:
                price = self._slippageModel.calculatePrice(
                    order, price, fillSize, bar, self._volumeUsed[order.getInstrument()]
                )
            # If expiry date is met, prix a 0
#            if bar.getDateTime() >= order.getExpiry():
#                price=0
         
            ret = fillstrategy.FillInfo(price, fillSize)
        return ret

    def fillOptionStopLimitOrder(self, broker_, order, bar):
        ret = None

        # First check if the stop price was hit so the limit order becomes active.
        stopPriceTrigger = None
        if not order.getStopHit():
            stopPriceTrigger = fillstrategy.get_stop_price_trigger(
                order.getAction(),
                order.getStopPrice(),
                broker_.getUseAdjustedValues(),
                bar
            )
            order.setStopHit(stopPriceTrigger is not None)

        # If the stop price was hit, check if we can fill the limit order.
        if order.getStopHit():
            # Calculate the fill size for the order.
            fillSize = self._calculateFillSize(broker_, order, bar)
            if fillSize == 0:
                broker_.getLogger().debug("Not enough volume to fill %s stop limit order [%s] for %s share/s" % (
                    order.getInstrument(),
                    order.getId(),
                    order.getRemaining()
                ))
                return None

            price = fillstrategy.get_limit_price_trigger(
                order.getAction(),
                order.getLimitPrice(),
                broker_.getUseAdjustedValues(),
                bar
            )
            if price is not None:
                # If we just hit the stop price, we need to make additional checks.
                if stopPriceTrigger is not None:
                    if order.isBuy():
                        # If the stop price triggered is lower than the limit price, then use that one.
                        # Else use the limit price.
                        price = min(stopPriceTrigger, order.getLimitPrice())
                    else:
                        # If the stop price triggered is greater than the limit price, then use that one.
                        # Else use the limit price.
                        price = max(stopPriceTrigger, order.getLimitPrice())
                # If expiry date is met, prix a 0
#                if bar.getDateTime() >= order.getExpiry():
#                    price=0
         
                ret = fillstrategy.FillInfo(price, fillSize)

        return ret
