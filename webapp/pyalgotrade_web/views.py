from django.shortcuts import render
import json
from django.http import Http404, HttpResponse
import sys
import StringIO
import contextlib
import os
import re

from os.path import abspath, dirname
sys.path.append(abspath(dirname(__file__) + '/' + '../..'))
from pyalgotrade.barfeed import ibfeed
from .util.sandbox import RestrictedExecutionEnv

# Global variables

base_dir = os.path.abspath(os.path.dirname(__file__) + '/' + '../..')
data_folder = base_dir + "\\data\\"
samples_folder = base_dir + "\\samples\\"

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


def loadChartDataCsv(request):

    if request.is_ajax() and request.method == 'GET':

        result = []

        # Ici on load les noms de fichiers CSV
        file_list = os.listdir(data_folder)

        for filename in file_list:
            matchobj = re.match(r'^([a-z]{3,4})_([0-9]{2,4})(p|c)([0-9]{8})(.csv)$', filename, re.IGNORECASE)
            if matchobj is not None:
                item = dict()
                item['file'] = filename.lower().split(".csv")[0]
                curr_instr = matchobj.group(1).upper()
                curr_opt_type = "PUT" if matchobj.group(3).lower() == 'p' else "CALL"
                curr_strike_price = matchobj.group(2)
                curr_expiry_date = matchobj.group(4)[0:4] \
                            + "-" + matchobj.group(4)[4:6] \
                            + "-" + matchobj.group(4)[6:8]
                item['title'] = curr_instr + " | " + curr_opt_type + " | " + curr_strike_price + "$ | " \
                                + curr_expiry_date
                result.append(item)
            else:
                continue

        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        raise Http404


def requestChartData(request):
    if request.is_ajax() and request.POST:

        selectedfile = str(request.POST.get('selectedData'))

        # REGEX pour le 'selectedData'
        matchobj = re.match(r'^([a-z]{3,4})_([0-9]{2,4})(p|c)([0-9]{8})$', selectedfile, re.IGNORECASE)

        if matchobj is not None:

            # instrument = selectedFile[0:3] + selectedFile[7:]
            instrument = matchobj.group(1) + matchobj.group(4)

            # Read the file line by line and construct array of chart dots {date, open, high, low, close, ask, bid}
            feed = ibfeed.Feed()
            feed.addBarsFromCSV(instrument, data_folder + selectedfile + ".csv")

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
            return HttpResponse(json.dumps(None), content_type='application/json')
    else:
        raise Http404

