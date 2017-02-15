from django.shortcuts import render
import json
from django.http import Http404, HttpResponse
import sys
import StringIO
import contextlib

# Create your views here.


def index(request):
    return render(request, 'pyalgotrade/index.html')


def testExec(request):
    return render(request, 'pyalgotrade/testExec.html')


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def execStrategy(request):
    if request.is_ajax() and request.POST:
        code = request.POST.get('strategy')
        with stdoutIO() as s:
            exec(code)

        execResult = s.getvalue()
        data = {'message': execResult}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404
