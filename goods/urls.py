from django.conf.urls import url
from .views import *
urlpatterns=[
    url('^$',index),
    # 第一个d+为类型的id, 第二个为当前是第几页,第三个是排序的依据
    url(r'^list(\d+)_(\d+)_(\d+)/$', list_views, name='list'),
    url(r'^(\d+)/$', detail, name='detail'),  # 详细页
]