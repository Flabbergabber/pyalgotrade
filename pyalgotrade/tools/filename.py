from pyalgotrade.barfeed import ibfeed
import datetime

class Parser(object):
    def parse(self, filename):
        slashIndex = filename.rfind('/')

        if (slashIndex > -1):
            filename = filename[slashIndex + 1:]

        zinstrument = filename[0:3]
        zStrikePrice = filename[4:6]
        zDate = filename[7:15]
        zID = filename[0:15]
        optiontype = filename[6]
        if (optiontype.lower() == "p"):
            optiontype = "PUT"
        elif (optiontype.lower() == "c"):
            optiontype = "CALL"
        else:
            optiontype = str(None)

        date = datetime.datetime.strptime(zDate, '%Y%m%d')

        instrument = ibfeed.Instrument(zinstrument,zStrikePrice,optiontype,date,filename,zID)

        return instrument
