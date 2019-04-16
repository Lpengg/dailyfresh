from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^register/$',register),
    url(r'^register_handle/$',register_handle),
    url(r'^register_exist/$',register_exist),
    url(r'^login/$',login),
    url(r'^login_handle/$',login_handle),
    url(r'^info/$',info),
    url(r'order/$',order),
    url(r'site/$',site),
    url(r'^logout/$', logout, name='logout'),
]