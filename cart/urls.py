from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', cart, name='cart'),
    url(r'^add(\d+)_(\d+)/$', add),     #加入购物车  分别为商品的id和数量
    url(r'^edit(\d+)_(\d+)/$', edit),   #修改购物车中商品的数量 分别为商品的id和数量
    url(r'^delete(\d+)/$',delete),      #删除购物车中的某个商品
]