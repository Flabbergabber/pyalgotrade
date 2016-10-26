from pyalgotrade import strategy
#from pyalgotrade.barfeed import yahoofeed
#from pyalgotrade.barfeed import googlefeed
from pyalgotrade.barfeed import ibfeed
from pyalgotrade.technical import ma
from pyalgotrade import broker
import datetime


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod):
        super(MyStrategy, self).__init__(feed, 1000)
        self.__position = None
        self.__option = None
        self.__optionAlreadyExecuted = False
        self.__instrument = instrument
        # We'll use adjusted close values instead of regular close values.
        #self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return

        bar = bars[self.__instrument]
        # If a position was not opened, check if we should enter a long position.
#        if self.__option is None and not self.__optionAlreadyExecuted:
        if self.__position is None: 
            
            right = broker.OptionOrder.Right.PUT
            strike = bar.getPrice() + 10
            bar.getDateTime()
            expiry = datetime.date(bar.getDateTime().year, bar.getDateTime().month +1, bar.getDateTime().day)
            
            #if bar.getPrice() > self.__sma[-1]:
                # Enter a buy market order for 10 shares. The order is good till canceled.
            self.__position = self.enterOptionLong(self.__instrument, 10, right, strike, expiry, True)
            #self.__optionAlreadyExecuted = True
            print "Option executed for: $%.2f" % (bar.getPrice())
        # Check if we have to exit the position.
        #elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            #self.__position.exitMarket()
        
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()
            print "Option exited at: $%.2f" % bar.getPrice()
        
        #### l'ordre devrait etre generer a partir de la position de l'option avec le strike price si expiry n'est pas depasse
#        elif self.__position is None and self.__option.getAge().days == 25 :
#            self.__position = self.enterLong(self.__option.getInstrument(), 10, True)
#            print "Order executed at: $%.2f" % bar.getPrice()
        
#        elif self.__position is not None and self.__position.getAge().days == 60 :
#            self.__position.exitMarket()
#            print "Order exited at: $%.2f" % bar.getPrice()

def run_strategy(smaPeriod):
    # Load the yahoo feed from the CSV file
#    feed = yahoofeed.Feed()
#    feed.addBarsFromCSV("orcl", "orcl-2000.csv")
    feed = ibfeed.Feed()
    feed.addBarsFromCSV("bac", "samples/bac.csv")

    # Evaluate the strategy with the feed.
#    myStrategy = MyStrategy(feed, "orcl", smaPeriod)
    myStrategy = MyStrategy(feed, "bac", smaPeriod)
    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

run_strategy(15)
