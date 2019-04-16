from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from order.models import OrderInfo
from . import user_decorator
from .models import *
from goods.models import GoodsInfo
from hashlib import sha1


# 登陆
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登陆', 'errot_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'user/login.html', context)


def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)

    # 根据用户名查询对象
    users = UserInfo.objects.filter(username=uname)

    # 如果为查到用户
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == users[0].password:
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                # 删除cookie
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = users[0].username
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'user/login.html', context)


def logout(request):
    # request.session.flush()     #清空session信息
    del request.session['user_id']
    del request.session['user_name']
    return redirect('/')

@user_decorator.login
def info(request):      #个人信息
    user_email = UserInfo.objects.get(id=request.session['user_id']).email

    goods_ids1=request.session.get(str(request.session['user_id']),'')
    goods_list = [] #存储商品浏览信息
    for goods_id in goods_ids1:
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {'title':'用户中心',
               'user_name':request.session['user_name'],
               'user_email': user_email,
               'goods_list':goods_list,
            }
    return render(request, 'user/user_center_info.html', context)

@user_decorator.login
def order(request):     #全部订单
    # 查询订单数据
    uid = request.session['user_id']
    orders = OrderInfo.objects.filter(user_id=uid).all()
    context = {'title': '用户中心','orders':orders}
    return render(request, 'user/user_center_order.html', context)

@user_decorator.login
def site(request):      #收货地址
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        if not(user.ushou and user.uaddress and user.uaddress and user.uphone):
            return redirect('/user/site/')
    context = {'title': '用户中心', 'user': user}
    user.save()
    return render(request, 'user/user_center_site.html', context)


# 请求注册的页面
def register(request):
    return render(request, 'user/register.html')


# 注册添加数据
def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post['user_name']
    upwd = post['pwd']
    upwd2 = post['cpwd']
    uemail = post['email']

    # 判断两次密码是否一致
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf8"))
    upwd3 = s1.hexdigest()

    # 创建对象
    user = UserInfo()
    user.username = uname
    user.password = upwd3
    user.email = uemail
    user.save()

    # 返回登录页
    return redirect('/user/login/')


# 验证用户名是否存在
def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(username=uname).count()
    return JsonResponse({'count': count})
