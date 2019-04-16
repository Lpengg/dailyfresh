from django.db import models

# Create your models here.

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)
    user = models.ForeignKey('user.UserInfo')
    odate = models.DateTimeField('下单日期',auto_now=True)
    oIsPay=models.BooleanField('是否支付',default=False)
    ototal = models.DecimalField('总金额',max_digits=6,decimal_places=2)
    oaddress=models.CharField('收货地址',max_length=150)

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('goods.GoodsInfo')
    order=models.ForeignKey(OrderInfo)
    price=models.DecimalField('价格',max_digits=5,decimal_places=2)
    count=models.IntegerField('数量',)
