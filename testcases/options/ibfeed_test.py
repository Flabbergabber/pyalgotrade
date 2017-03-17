import testcases.common
import testcases.barfeed_test
import testcases.feed_test
from pyalgotrade.barfeed import ibfeed
from pyalgotrade import marketsession
from pyalgotrade.utils import dt
from pyalgotrade import bar

class IBTestCase(testcases.common.TestCase):
    def __loadBarFeed(self, timeZone=None):
        ret = ibfeed.Feed(bar.Frequency.DAY, timeZone)
        ret.addBarsFromCSV("bac", testcases.common.get_data_file_path("ib-bac_20p20160819.csv"))
        ret.loadAll()
        return ret

    def testBaseFeedInterface(self):
        barFeed = ibfeed.Feed()
        barFeed.addBarsFromCSV("bac", testcases.common.get_data_file_path("ib-bac_20p20160819.csv"))
        testcases.feed_test.tstBaseFeedInterface(self, barFeed)

    def testWithTimezone(self):
        timeZone = marketsession.USEquities.getTimezone()
        barFeed = self.__loadBarFeed(timeZone)
        ds = barFeed.getDataSeries()

        for i, currentBar in enumerate(ds):
            self.assertFalse(dt.datetime_is_naive(currentBar.getDateTime()))
            self.assertEqual(ds[i].getDateTime(), ds.getDateTimes()[i])

    def testWithIntegerTimezone(self):
        try:
            barFeed = ibfeed.Feed(timezone=-3)
            self.assertTrue(False, "Exception expected")
        except Exception, e:
            self.assertTrue(str(e).find("timezone as an int parameter is not supported anymore") == 0)

        try:
            barFeed = ibfeed.Feed()
            barFeed.addBarsFromCSV("bac", testcases.common.get_data_file_path("ib-bac_20p20160819.csv"), -5)
            self.assertTrue(False, "Exception expected")
        except Exception, e:
            self.assertTrue(str(e).find("timezone as an int parameter is not supported anymore") == 0)

    def testBounded(self):
        barFeed = ibfeed.Feed(maxLen=2)
        barFeed.addBarsFromCSV("bac", testcases.common.get_data_file_path("ib-bac_20p20160819.csv"))
        barFeed.loadAll()

        barDS = barFeed["bac"]
        self.assertEqual(len(barDS), 2)
        self.assertEqual(len(barDS.getDateTimes()), 2)
        self.assertEqual(len(barDS.getCloseDataSeries()), 2)
        self.assertEqual(len(barDS.getCloseDataSeries().getDateTimes()), 2)
        self.assertEqual(len(barDS.getOpenDataSeries()), 2)
        self.assertEqual(len(barDS.getHighDataSeries()), 2)
        self.assertEqual(len(barDS.getLowDataSeries()), 2)
        self.assertEqual(len(barDS.getAdjCloseDataSeries()), 2)

    def testBaseBarFeed(self):
        barFeed = ibfeed.Feed()
        barFeed.addBarsFromCSV("bac", testcases.common.get_data_file_path("ib-bac_20p20160819.csv"))
        testcases.barfeed_test.check_base_barfeed(self, barFeed, False)

    def testReset(self):
        instrument = "bac"
        barFeed = ibfeed.Feed()
        barFeed.addBarsFromCSV(instrument, testcases.common.get_data_file_path("ib-bac_20p20160819.csv"))

        barFeed.loadAll()
        instruments = barFeed.getRegisteredInstruments()
        ds = barFeed[instrument]

        barFeed.reset()
        barFeed.loadAll()
        reloadedDs = barFeed[instrument]

        self.assertEqual(len(reloadedDs), len(ds))
        self.assertNotEqual(reloadedDs, ds)
        self.assertEqual(instruments, barFeed.getRegisteredInstruments())
        for i in range(len(ds)):
            self.assertEqual(ds[i].getDateTime(), reloadedDs[i].getDateTime())
            self.assertEqual(ds[i].getClose(), reloadedDs[i].getClose())
