from pyalgotrade.strategy import optstrategy
#from pyalgotrade.barfeed import yahoofeed
#from pyalgotrade.barfeed import googlefeed
from pyalgotrade.barfeed import ibfeed
from pyalgotrade.technical import ma
from pyalgotrade.broker import optbroker
import datetime
from pyalgotrade.stratanalyzer import returns
from pyalgotrade import plotter


class MyStrategy(optstrategy.OptionBacktestingStrategy):
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
        
    def getSMA(self):
        return self.__sma
        
    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
        
    def UpdateExpired(self, bars):
        if bars is not None:
            for instrument, shares in self.getBroker().getPositions().iteritems():
                ##### on va chercher la date pour detarminer lexpiration 'un option
                
                ##### on detecte vaguement si le format est pour une option
                if len(instrument) > 8:
                    time = self.getBroker()._getBar(bars, instrument).getDateTime()
                    year = self.getBroker()._getBar(bars, instrument).getDateTime().year
                    month = self.getBroker()._getBar(bars, instrument).getDateTime().month
                    day = self.getBroker()._getBar(bars, instrument).getDateTime().day
                    ####### Si la date de la bar est egale ou superieure a la date d'expiration, on annule les part et empeche les order sur cet instrument
                    currentdatetime= datetime.strptime(instrument[-8:], '%Y%m%d')
                    if datetime.strptime(instrument[-8:], '%Y%m%d') <= datetime(year, month, day):
                        self.__logger.debug("POSITION EST EXPIREE")
                        shares = 0
#                        instument=None
                        for order in self.getBroker().getActiveOrders(instrument):
                            self.getBroker().cancelOrder(order)
         
    
    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        if self.__sma[-1] is None:
            return
        self.UpdateExpired(bars)    

        bar = bars[self.__instrument]
#        self.info("current bar price: $%.2f and current sma: $%.2f" % (bar.getPrice(), self.__sma[-1]))
        # If a position was not opened, check if we should enter a long position.
#        if self.__option is None and not self.__optionAlreadyExecuted:
        if self.__position is None: 
            
            if bar.getPrice() > self.__sma[-1]:
                right = optbroker.OptionOrder.Right.PUT
                strike = bar.getPrice() + 10
                bar.getDateTime()
                expiry = datetime.datetime(2016, 3, 30, 16, 30)
                
                #if bar.getPrice() > self.__sma[-1]:
                    # Enter a buy market order for 10 shares. The order is good till canceled.
                self.__position = self.enterOptionLong(self.__instrument, 10, right, strike, expiry, True)
                #self.__optionAlreadyExecuted = True
                
#                print "Option executed for: $%.2f" % (bar.getPrice())
        # Check if we have to exit the position.
        #elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            #self.__position.exitMarket()
        
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()
#            print "Option exited at: $%.2f" % bar.getPrice()
        

        
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
    feed.addBarsFromCSV("bac", "bac.csv")

    # Evaluate the strategy with the feed.
#    myStrategy = MyStrategy(feed, "orcl", smaPeriod)
    myStrategy = MyStrategy(feed, "bac", smaPeriod)
    
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)
    
    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy)
    # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
    plt.getInstrumentSubplot("bac").addDataSeries("SMA", myStrategy.getSMA())
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    myStrategy.run()
    print "Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

    plt.plot()
    
run_strategy(10)
