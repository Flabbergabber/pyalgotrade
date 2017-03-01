from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testExec/$', views.testExec, name='test_exec'),
    url(r'^ajax/beginBacktest/$', views.beginBacktest, name='begin_backtest'),
    url(r'^ajax/requestChartData/$', views.requestChartData, name='requestChartData'),
]
