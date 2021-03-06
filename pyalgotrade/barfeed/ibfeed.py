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

from pyalgotrade.barfeed import csvfeed
from pyalgotrade import bar
from pyalgotrade.utils import dt

import datetime


######################################################################
## Interactive Broker CSV parser
# Each bar must be on its own line and fields must be separated by semicolon (;).
#
# Minute Bars Format:
# mm/dd/YYYY HH:mm;open price;high price;low price;close price;number_ticks;volume;value
#
# The exported data will be in the UTC time zone.(have to verify that)

def parse_datetime(dateTime):
    # Sample: 20081231 230600
    # This custom parsing works faster than:
    # datetime.datetime.strptime(dateTime, "%Y%m%d %H%M%S")
    # year = int(dateTime[0:4])
    # month = int(dateTime[4:6])
    # day = int(dateTime[6:8])
    # hour = int(dateTime[9:11])
    # minute = int(dateTime[11:13])
    # sec = int(dateTime[13:15])
    # return datetime.datetime(year, month, day, hour, minute, sec)
    return datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M")


class RowParser(csvfeed.RowParser):
    def __init__(self, frequency, dailyBarTime, timezone=None):
        self.__frequency = frequency
        self.__dailyBarTime = dailyBarTime
        self.__timezone = timezone

    def __parseDateTime(self, dateTime):
        ret = parse_datetime(dateTime)

        # Localize bars if a market session was set.
        if self.__timezone:
            ret = dt.localize(ret, self.__timezone)
        return ret

    def getFieldNames(self):
        return None

    def getDelimiter(self):
        return ";"

    def parseBar(self, csvRowDict):
        dateTime = self.__parseDateTime(csvRowDict["Date"])
        close = float(csvRowDict["Close"])
        open_ = float(csvRowDict["OPEN"])
        high = float(csvRowDict["HIGH"])
        low = float(csvRowDict["LOW"])
        volume = float(csvRowDict["VOLUME"])
        return bar.BasicBar(dateTime, open_, high, low, close, volume, None, self.__frequency)


class Feed(csvfeed.BarFeed):
    """A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files exported from Interactive Broker.

    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.MINUTE** are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        super(Feed, self).__init__(frequency, maxLen)

        if isinstance(timezone, int):
            raise Exception("timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.")

        self.__timezone = timezone

    def barsHaveAdjClose(self):
        return False

    def addBarsFromCSV(self, instrument, path, timezone=None):
        """Loads bars for a given instrument from a CSV formatted file.
        The instrument gets registered in the bar feed.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param path: The path to the file.
        :type path: string.
        :param timezone: The timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
        :type timezone: A pytz timezone.
        """

        if isinstance(timezone, int):
            raise Exception(
                "timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.")

        if timezone is None:
            timezone = self.__timezone

        rowParser = RowParser(self.getFrequency(), self.getDailyBarTime(), timezone)
        super(Feed, self).addBarsFromCSV(instrument, path, rowParser)

#Option contract
class Instrument:
    def __init__(self, symbol, strike, right, expiry, filename, id):
        self.symbol = symbol
        self.strike = strike
        self.right = right
        self.expiry = expiry
        self.filename = filename
        self.id = id