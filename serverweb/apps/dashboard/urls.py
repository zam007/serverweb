#!_*_coding:utf-8_*_
# __author__:"zam"
from django.conf.urls import url
from serverweb.apps.dashboard import views as dashboard_view

urlpatterns = [
    url(r'^server_fun_categ/$', dashboard_view.server_fun_categ, name='server_fun_categ'),
    url(r'^server_app_categ/$', dashboard_view.server_app_categ, name='server_app_categ'),
    url(r'^server_list/$', dashboard_view.server_list, name='server_list'),
    url(r'^module_list/$', dashboard_view.module_list, name='module_list'),
    url(r'^module_info/$', dashboard_view.module_info, name='module_info'),
    url(r'^module_add/$', dashboard_view.module_add, name='module_add'),
    url(r'^module_run/$', dashboard_view.module_run, name='module_run'),
    url(r'^$', dashboard_view.index, name='index'),
]
