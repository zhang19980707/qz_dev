from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.models import User, Address  # 调用django内部认证模块,  导入地址信息模型类，便于操作地址信息
from goods.models import GoodsSKU
from django.contrib.auth import authenticate, login, logout  # 导入登录验证所需函数
from django.core.urlresolvers import reverse  # 调用反向解析模块
from django.views.generic import View  # 调用视图类模块
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 引入加密信息模块
from django.conf import settings  # 引入设置项，来设置token
from itsdangerous import SignatureExpired  # 导入验证过期异常
# from django.core.mail import send_mail
from celery_tasks.tasks import send_register_active_email  # 导入celery发送邮件的模块
from utils.mixin import LoginRequiredMixin  # 导入小工具中的登录验证装饰器
from django_redis import get_redis_connection  # 使用django_redis链接方式
import re


# Create your views here.


# def register(request):
#     """注册页面视图"""
#     if request.method == 'GET':
#         return render(request, 'register.html')
#     else:
#         """处理注册信息"""
#         # 1.接受数据
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         cpassword = request.POST.get('cpwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#
#         # 2.数据校验  TUDO
#         # if not all([username, password, email]):
#         #     # 数据不完整
#         #     return render(request, 'register.html', {'errmsg': '数据不完整'})
#         # # 校验邮箱
#         # if not re.match(r'^[/^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/]', email):
#         #     return render(request, 'register.html', {'errmsg': '邮箱不合法'})
#         # # 校验两次密码是否一致
#         # # if password != cpassword:
#         # #     return render(request, 'register.html', {'errmsg': '密码不一致'})
#         # # 校验是否同意协议
#         # if allow != 'on':
#         #     return render(request, 'register.html', {'errmsg': '请同意协议'})
#
#         # 3.业务处理（用户注册）
#         """
#         ORM的方法：
#         user = User()
#         user.username = username
#         user.password = password
#         user.email = email
#         user.save()
#         """
#         # 使用django内置的认证系统
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # 用户名不存在
#             user = None
#
#         if user:
#             # 用户名已经存在
#             return render(request, 'register.html', {'errmsg': '用户名已存在'})
#         else:
#             user = User.objects.create_user(username, email, password)
#             user.is_active = 0
#             user.save()
#
#         # 4.应答,使用方向解析跳转首页
#         return redirect(reverse('goods:index'))


class RegisterView(View):
    """登录视图类"""

    def get(self, request):
        """定义get视图实例方法"""
        return render(request, 'register.html')

    def post(self, request):
        """定义post视图实例方法"""
        # 1.接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2.数据校验  TUDO
        # if not all([username, password, email]):
        #     # 数据不完整
        #     return render(request, 'register.html', {'errmsg': '数据不完整'})
        # # 校验邮箱
        # if not re.match(r'^[/^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/]', email):
        #     return render(request, 'register.html', {'errmsg': '邮箱不合法'})
        # # 校验两次密码是否一致
        # # if password != cpassword:
        # #     return render(request, 'register.html', {'errmsg': '密码不一致'})
        # # 校验是否同意协议
        # if allow != 'on':
        #     return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 3.业务处理（用户注册）
        """
        ORM的方法：
        user = User()
        user.username = username
        user.password = password
        user.email = email
        user.save()
        """
        # 使用django内置的认证系统
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已经存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        else:
            user = User.objects.create_user(username, email, password)
            user.is_active = 0
            user.save()

            # 发送激活邮件，设置激活链接http;//127.0.0.1:8000/user/activate/加密后的用户身份信息
            # 激活链接包含用户信息
            # 加密用户身份信息，生成激活的token
            serializer = Serializer(settings.SECRET_KEY, 3600)
            info = {'confirm': user.id}
            token = serializer.dumps(info)  # bytes
            token = token.decode()

            # 发送邮件
            """
            subject = '天天生鲜欢迎信息'
            message = ''
            html_message = '<h1>%s,欢迎您成为天天呢生鲜的注册会员</h1>请点击下方链接激活账户<br/>' \
                           '<a href="http://127.0.0.1:8000/user/active/%s">' \
                           'http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
            sender = settings.EMAIL_FROM
            receiver = [email]
            """
            send_register_active_email.delay(email, username, token)

        # 4.应答,使用方向解析跳转首页
        return redirect(reverse('goods:index'))


class Active(View):
    """激活类视图"""
    def get(self, request, token):
        """进行用户激活"""
        # 解密用户信息
        token = token.encode()
        serializer = Serializer(settings.SECRET_KEY, 5)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的信息
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            return HttpResponse('用户验证身份已经过期')


class LoginView(View):
    """登录视图类"""
    def get(self, request):
        """显示登录页面"""
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username':username, 'checked':checked})

    def post(self, request):
        """登录校验"""
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 数据校验
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg':'数据不完整'})

        # 业务处理
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户登录状态
                login(request, user)

                # 跳转到指定地址
                next_url = request.GET.get('next', reverse('goods:index'))
                response = redirect(next_url)  # HttpResponseRedirect对象

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 说明需要记住用户名
                    response.set_cookie('username', username, max_age=14*24*3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response

            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '用户未激活'})
        else:
            # 用户名和密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


class LogoutView(View):
    """退出视图类"""
    def get(self, requset):
        """用户退出"""
        # 清楚用户session信息
        logout(requset)

        return redirect(reverse('goods:index'))


class UserInfoView(LoginRequiredMixin, View):
    """用户中心视图类"""
    def get(self, request):
        """显示"""
        # page==user
        # request.user.is_authenticated()
        # 除了传递模板变量，django框架也可以将request.user传递给模板文件

        # TOTO1 获取用户个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # TOTO2 获取用户浏览记录
        # 方法一
        # from redis import StrictRedis
        # sr = StrictRedis(host='127.0.0.1', port='6379', db=9)
        con = get_redis_connection('default')

        history_key = 'history_%d' % user.id

        # 获取最新5个浏览商品记录
        sku_id = con.lrange(history_key, 0, 4)  # [2, 3, 1]

        # 从数据库查询用户浏览的商品信息
        goods_li = GoodsSKU.objects.filter(id__in=sku_id)

        # goods_res = []
        # for a_id in sku_id:
        #     for goods in goods_li:
        #         if a_id == goods.id:
        #             goods_res.append(goods)

        goods_li = []
        for id in sku_id:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods_li)

        # 组织上下文
        context = {
            'page':'user',
            'address':address,
            'goods_li':goods_li
        }

        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
    """用户订单视图类"""
    def get(self, request):
        """显示"""

        # TUDO1 获取用户的订单信息

        return render(request, 'user_center_order.html', {'page': 'order'})


class UserSiteView(LoginRequiredMixin, View):
    """用户地址视图类"""
    def get(self, request):
        """显示"""
        # 获取登录用户对应的User对象
        user = request.user

        # 获取用户默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在收货地址
        #     address = None

        address = Address.objects.get_default_address(user)

        return render(request, 'user_center_site.html', {'page': 'address', 'address':address})

    def post(self, request):
        """新增收货地址"""
        # 1.接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 2.校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {'errmsg':'数据不完整'})

        if not re.match(r'^1[3|4|5|6|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg':'手机号不合法'})

        # 3.业务处理
        # 如果已经存在默认收货地址，添加的地址不作为默认地址，否则设为默认收货地址
        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在收货地址
        #     address = None

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加收货地址
        Address.objects.create(
            user=user,
            receiver=receiver,
            addr=addr,
            zip_code=zip_code,
            phone=phone,
            is_default=is_default
        )

        # 4.返回应答，刷新地址页面
        return redirect(reverse('user:address'))  # get请求方式
