from pyalgotrade.strategy import optstrategy
from pyalgotrade.technical import ma
from pyalgotrade.barfeed import ibfeed
from pyalgotrade.tools import filename as filenametool

class MyStrategy(optstrategy.OptionBacktestingStrategy):
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
feed = ibfeed.Feed(maxLen=2)

parser = filenametool.Parser()

fileList = ["bac_2000-p20170217.csv","bac_2100-p20170217.csv","bac_2200-p20170217.csv"]

instru1 = parser.parse("bac_2000-p20170217.csv")
print instru1.id + " " + str(instru1.expiry) + " " +instru1.filename + " " +instru1.right+ " " +str(instru1.strike)+ " " +instru1.symbol
instru2 = parser.parse("bac_2100-p20170217.csv")
print instru2.id +  " " +str(instru2.expiry) + " " +instru2.filename + " " +instru2.right+ " " +str(instru2.strike)+ " " +instru2.symbol
instru3 = parser.parse("bac_2200-p20170217.csv")
print instru3.id + " " + str(instru3.expiry) + " " +instru3.filename + " " +instru3.right+ " " +str(instru3.strike)+ " " +instru3.symbol

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