from pyalgotrade.barfeed import ibfeed
import datetime

class Parser(object):
    def parse(self, filename):
        slashIndex = filename.rfind('/')

        if (slashIndex > -1):
            filename = filename[slashIndex + 1:]

        underscoreIndex = filename.rfind('_')
        hyphenIndex = filename.rfind('-')

        zinstrument = filename[0:underscoreIndex]
        zStrikePrice = filename[underscoreIndex+1:hyphenIndex]
        zDate = filename[hyphenIndex+2:hyphenIndex+10]
        zID = filename[0:hyphenIndex+10]
        optiontype = filename[hyphenIndex+1]
        if (optiontype.lower() == "p"):
            optiontype = "PUT"
        elif (optiontype.lower() == "c"):
            optiontype = "CALL"
        else:
            optiontype = str(None)

        #Todo Gerer mauvaise date
        date = datetime.datetime.strptime(zDate, '%Y%m%d')

        floatStrike = float(zStrikePrice[:len(zStrikePrice)-2] + '.' + zStrikePrice[len(zStrikePrice)-2:])

        instrument = ibfeed.Instrument(zinstrument,floatStrike,optiontype,date,filename,zID)

        return instrument
