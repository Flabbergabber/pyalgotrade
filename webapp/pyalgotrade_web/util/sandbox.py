import sys
import re
from os.path import abspath, dirname
sys.path.append(abspath(dirname(__file__) + '/' + '../../..'))
from pyalgotrade.strategy import optstrategy
from pyalgotrade.barfeed import ibfeed
from pyalgotrade.technical import ma
from pyalgotrade.broker import optbroker
import datetime
from pyalgotrade.stratanalyzer import returns
from datasourcehelper import DataSourceHelper

class RestrictedExecutionEnv:
    blacklist = {'import': 'import[ ]{1}[A-Za-z\.]*', 'open': '.*open[ |\(].*[ |\)].*'}

    def __init__(self):
        pass

    def executeUnstrustedCode(self, code):
        """Executes an untrusted block of code.
        In an effort to prevent malicious intent, before compilation, code is scanned to see if it contains any
        blacklisted elements.

        :param code: str
        :return: tuple(success: bool, msgList: str[])
        """
        messages = []
        blackListElementFound = False
        for keyword, regexp in self.blacklist.iteritems():
            if re.search(regexp, code):
                messages.append('Code cannot contain keyword: ' + keyword)
                blackListElementFound = True

        if blackListElementFound:
            return (False, messages)
        else:
            try:
                compiledCode = compile(code, '<string>', 'exec')
                exec (compiledCode, globals())
                return (True, ['Code successfully executed!'])
            except SyntaxError as se:
                return (False, ['Compilation error: %s' % str(se)])


