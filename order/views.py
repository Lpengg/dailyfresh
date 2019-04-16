import datetime

from decimal import Decimal
from django.db import transaction
from django.shortcuts import render,redirect

from goods.models import GoodsInfo
from user import user_decorator
from user.models import UserInfo
from .models import *
from cart.models import *


@user_decorator.login
def order(request):
    cart_ids = request.GET.getlist('cart_id')
    carts=[]    #存放选中的购物车商品
    ids =''
    for cart_id in cart_ids:
        ids=cart_id + ','+ids
        carts.append(CartInfo.objects.get(id=cart_id))
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    context = {
        'title': '提交订单',
        'page_name': 1,
        'carts': carts,
        'user':user,
        'ids':ids
    }
    return render(request,'order/order.html',context)

def order_handle(request):
    tran_id =transaction.savepoint()    #事务
    ids = request.GET['ids'].split(',')
    ids = ids[0:len(ids)-1]
    # 创建一个订单
    try:
        #     创建订单对象
        order = OrderInfo()
        now = datetime.datetime.now()
        print(now)
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        order.oaddress = UserInfo.objects.get(id=uid).uaddress
        order.odata=now
        total=0
        for id in ids:
            cart = CartInfo.objects.get(id=id)
            price = cart.goods.gprice
            total +=  price * cart.count
        order.ototal=Decimal(total+10)
        order.save()

        # 创建详单对象
        for id1 in ids:
            detail = OrderDetailInfo()
            detail.order=order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods=cart.goods
            if goods.gkucun>=cart.count:
                goods.gkucun=cart.goods.gkucun-cart.count
                goods.save()
                # 完善详细信息
                detail.goods_id=goods.id
                detail.price=goods.gprice
                detail.count=cart.count
                detail.save()
                #删除购物车数据
                cart.delete()
            else:#如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('=============%s'%e)
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/order/')
