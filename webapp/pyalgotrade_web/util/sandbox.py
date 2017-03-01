import sys
from os.path import abspath, dirname
sys.path.append(abspath(dirname(__file__) + '/' + '../../..'))
from pyalgotrade.strategy import optstrategy
from pyalgotrade.barfeed import ibfeed
from pyalgotrade.technical import ma
from pyalgotrade.broker import optbroker
import datetime
from pyalgotrade.stratanalyzer import returns

class RestrictedExecutionEnv:
    def __init__(self):
        pass

    def executeUnstrustedCode(self, code):
        compiledCode = compile(code, '<string>', 'exec')
        exec(compiledCode, globals())
