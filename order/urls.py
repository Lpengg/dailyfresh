from django.conf.urls import url
from .views import *
urlpatterns=[
    url(r'^$',order),
    url(r'^order_handle/$',order_handle),
]