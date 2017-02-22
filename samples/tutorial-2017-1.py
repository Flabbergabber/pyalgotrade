from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.barfeed import ibfeed
from pyalgotrade.tools import filename as filenametool

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instruments):
        super(MyStrategy, self).__init__(feed)
        self.__smaList = []
        for instrument in instruments:
            self.__smaList.append(ma.SMA(feed[instrument].getOpenDataSeries(),5))

        self.__instruments = instruments

    def onBars(self, bars):
        count = 0
        for instrument in self.__instruments:
            bar = bars[instrument]
            self.info("%s %s" % (bar.getOpen(), self.__smaList[count][-1]))
            count = count + 1


# Load the yahoo feed from the CSV file
feed = ibfeed.Feed()

parser = filenametool.Parser()

fileList = ["bac_20p20170217.csv","bac_21p20170217.csv","bac_22p20170217.csv"]

instru1 = parser.parse("bac_20p20170217.csv")
instru2 = parser.parse("bac_21p20170217.csv")
instru3 = parser.parse("bac_22p20170217.csv")

idList = []

feed.addBarsFromCSV(instru1.id, instru1.filename)
idList.append(instru1.id);
feed.addBarsFromCSV(instru2.id, instru2.filename)
idList.append(instru2.id);
feed.addBarsFromCSV(instru3.id, instru3.filename)
idList.append(instru3.id);

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feed, idList)
myStrategy.run()