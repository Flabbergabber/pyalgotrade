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
import util.datasourcehelper as dsh

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


def find_second_last(text, pattern):
    return text.rfind(pattern, 0, text.rfind(pattern))


def beginBacktest(request):
    if request.is_ajax() and request.method == 'POST':

        code = request.POST.get('strategy')

        with stdoutIO() as s:
            env = RestrictedExecutionEnv()
            success, messages = env.executeUnstrustedCode(code)

        execResult = ''
        with open(dsh.PYALGOTRADE_TEMP_DUMP_JSON_FILE, 'r') as strat_exec_json_dump:
            execResult = json.load(strat_exec_json_dump)

        stdoutExecResult = s.getvalue()
        startportfolio = 1000.0
        endportfolio = stdoutExecResult[find_second_last(stdoutExecResult, "\n"):]
        endportfolio = float(endportfolio[endportfolio.index('$')+1:endportfolio.rfind("\n")])
        performance = str((endportfolio - startportfolio) / startportfolio * 100) + " %"
        results = " Start: $ " + str(startportfolio) + "\n End: $ " + str(endportfolio) + "\n Performance: " + performance + "\n"

        data = {'message': execResult, 'statusmessages': messages, 'results': results}

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


def loadChartDataCsv(request):

    if request.is_ajax() and request.method == 'GET':

        result = []

        # Ici on load les noms de fichiers CSV
        file_list = os.listdir(dsh.PYALGOTRADE_DATA_FOLDER)

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
    if request.is_ajax() and request.method == 'POST':

        selectedfile = str(request.POST.get('selectedData'))

        # REGEX pour le 'selectedData'
        matchobj = re.match(r'^([a-z]{3,4})_([0-9]{2,4})(p|c)([0-9]{8})$', selectedfile, re.IGNORECASE)

        if matchobj is not None:

            # instrument = selectedFile[0:3] + selectedFile[7:]
            instrument = matchobj.group(1) + matchobj.group(4)

            # Read the file line by line and construct array of chart dots {date, open, high, low, close, ask, bid}
            feed = ibfeed.Feed()
            feed.addBarsFromCSV(instrument, dsh.PYALGOTRADE_DATA_FOLDER + selectedfile + ".csv")

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

