from django.shortcuts import render
import json
from django.http import Http404, HttpResponse
import sys
import StringIO
import contextlib
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
            env.executeUnstrustedCode(code)

        execResult = s.getvalue()
        data = {'message': execResult}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

