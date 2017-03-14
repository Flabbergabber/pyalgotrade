import datetime
import json
import os
from pyalgotrade.broker import Order

# Hardcoded paths to the temporary json transfer file to be used by webapp.
PYALGOTRADE_BASE = os.path.abspath(os.path.join(__file__, "../../../../"))
PYALGOTRADE_TEMP_DUMP_JSON_FILE = os.path.join(PYALGOTRADE_BASE, "data/temp/jsondump.json")


class StrategyTransferObject:
    BUY_ACTION_STR = "BUY"
    SELL_ACTION_STR = "SELL"

    def __init__(self):
        self.__initialEquity = 0
        self.__finalEquity = 0
        self.__buySellHistory = []

    def setInitialEquity(self, equity):
        """
        Sets the initial equity of the transfer object.
        :param equity: as the initial equity
        :return: None
        """
        self.__initialEquity = equity

    def setFinalEquity(self, equity):
        """
        Sets the final equity of the transfer object.
        :param equity: as the final equity
        :return: None
        """
        self.__finalEquity = equity

    def recordBuySell(self, action, instrument, date, price):
        """
        Records a Buy or Sell action according to a specified instrument, date and price.
        :param action: Order.Action.BUY or Order.Action.SELL
        :param instrument: as the instrument str
        :param date: as the order date
        :param price: as the order price
        :return: None
        """
        buySell = ""
        if action == Order.Action.BUY:
            buySell = StrategyTransferObject.BUY_ACTION_STR
        elif action == Order.Action.SELL:
            buySell = StrategyTransferObject.SELL_ACTION_STR

        dateStr = date.strftime("%Y-%m-%d %H:%M:%S")
        buySell = {"buysell": buySell, "instrument": instrument, "date": dateStr, "price": price}
        self.__buySellHistory.append(buySell)

    def dumpToFile(self):
        """
        Dumps the transfer object to a specified file in json formatting.
        :return: None
        """
        jsonToDump = {"initialEquity": self.__initialEquity,
                    "finalEquity": self.__finalEquity,
                    "buySellHistory": self.__buySellHistory}
        with open(PYALGOTRADE_TEMP_DUMP_JSON_FILE, 'w') as jsonfp:
            json.dump(jsonToDump, jsonfp)

