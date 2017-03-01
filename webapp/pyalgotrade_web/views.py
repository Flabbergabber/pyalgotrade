from django.shortcuts import render
import json
from django.http import Http404, HttpResponse
import sys
import StringIO
import contextlib
import os
from os.path import abspath, dirname
sys.path.append(abspath(dirname(__file__) + '/' + '../..'))
from pyalgotrade.barfeed import ibfeed
from .util.sandbox import RestrictedExecutionEnv

# Create your views here.


def index(request):
    return render(request, 'pyalgotrade_web/index.html')


def testExec(request):
    return render(request, 'pyalgotrade_web/testExec.html')


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def beginBacktest(request):
    if request.is_ajax() and request.POST:
        code = request.POST.get('strategy')
        with stdoutIO() as s:
            env = RestrictedExecutionEnv()
            success, messages = env.executeUnstrustedCode(code)

        execResult = s.getvalue()
        data = {'message': execResult, 'statusmessages': messages}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

def requestChartData(request):

    if request.is_ajax() and request.POST:
        # TODO: Validation REGEX pour le 'selectedData'
        selectedFile = str(request.POST.get('selectedData'))

        basePath = os.path.abspath(os.path.dirname(__file__) + '/' + '../..') + "\\samples\\"

        # TODO: Permettre d'avoir d'autres instruments
        instrument = selectedFile[0:3] + selectedFile[7:]


        # Read the file line by line and construct array of chart dots {date, open, high, low, close, ask, bid}
        feed = ibfeed.Feed()
        feed.addBarsFromCSV(instrument, basePath + selectedFile + ".csv")

        data = []
        for date, bars in feed:
            item = dict()
            item['date'] = str(date)
            item['low'] = str(bars.getBar(instrument).getLow())
            item['high'] = str(bars.getBar(instrument).getHigh())
            item['close'] = str(bars.getBar(instrument).getClose())
            item['open'] = str(bars.getBar(instrument).getOpen())
            data.append(item)

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

