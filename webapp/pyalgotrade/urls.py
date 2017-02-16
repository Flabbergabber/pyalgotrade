from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testExec/$', views.testExec, name='test_exec'),
    url(r'^testExec/execStrategy/$', views.execStrategy, name='exec_strategy'),
]
