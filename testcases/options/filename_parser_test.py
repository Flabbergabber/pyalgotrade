import testcases.common as common
import datetime
from pyalgotrade.tools import filename as filenametool


class ParsingTestCase(common.TestCase):
    def testGoodCase(self):
        parser = filenametool.Parser()

        instru1 = parser.parse("bac_2000-p20170217.csv")
        self.assertEqual(instru1.id, "bac_2000-p20170217")
        self.assertEqual(instru1.expiry, datetime.datetime.strptime("20170217", '%Y%m%d'))
        self.assertEqual(instru1.filename , "bac_2000-p20170217.csv")
        self.assertEqual(instru1.right , "PUT")
        self.assertEqual(instru1.strike , float("20.00"))
        self.assertEqual(instru1.symbol, "bac")

        instru2 = parser.parse("a_4550-c20130101.csv")
        self.assertEqual(instru2.id, "a_4550-c20130101")
        self.assertEqual(instru2.expiry, datetime.datetime.strptime("20130101", '%Y%m%d'))
        self.assertEqual(instru2.filename, "a_4550-c20130101.csv")
        self.assertEqual(instru2.right, "CALL")
        self.assertEqual(instru2.strike, float("45.50"))
        self.assertEqual(instru2.symbol, "a")

        instru3 = parser.parse("zz_1234-p20190723.csv")
        self.assertEqual(instru3.id, "zz_1234-p20190723")
        self.assertEqual(instru3.expiry, datetime.datetime.strptime("20190723", '%Y%m%d'))
        self.assertEqual(instru3.filename, "zz_1234-p20190723.csv")
        self.assertEqual(instru3.right, "PUT")
        self.assertEqual(instru3.strike, float("12.34"))
        self.assertEqual(instru3.symbol, "zz")

        instru4 = parser.parse("appl_99999-p20150505.csv")
        self.assertEqual(instru4.id, "appl_99999-p20150505")
        self.assertEqual(instru4.expiry, datetime.datetime.strptime("20150505", '%Y%m%d'))
        self.assertEqual(instru4.filename, "appl_99999-p20150505.csv")
        self.assertEqual(instru4.right, "PUT")
        self.assertEqual(instru4.strike, float("999.99"))
        self.assertEqual(instru4.symbol, "appl")

        instru5 = parser.parse("bbbb_17-p20150505.csv")
        self.assertEqual(instru5.id, "bbbb_17-p20150505")
        self.assertEqual(instru5.expiry, datetime.datetime.strptime("20150505", '%Y%m%d'))
        self.assertEqual(instru5.filename, "bbbb_17-p20150505.csv")
        self.assertEqual(instru5.right, "PUT")
        self.assertEqual(instru5.strike, float("0.17"))
        self.assertEqual(instru5.symbol, "bbbb")

        instru6 = parser.parse("bbbb_017-p20150505.csv")
        self.assertEqual(instru6.id, "bbbb_017-p20150505")
        self.assertEqual(instru6.expiry, datetime.datetime.strptime("20150505", '%Y%m%d'))
        self.assertEqual(instru6.filename, "bbbb_017-p20150505.csv")
        self.assertEqual(instru6.right, "PUT")
        self.assertEqual(instru6.strike, float("0.17"))
        self.assertEqual(instru6.symbol, "bbbb")