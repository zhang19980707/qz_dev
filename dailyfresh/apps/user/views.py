from django.shortcuts import render, redirect
# from user.models import User
from user.models import User  # 调用django内部认证模块
from django.core.urlresolvers import reverse  # 调用反向解析模块
from django.views.generic import View  # 调用视图类模块
import re
# Create your views here.


def register(request):
    """注册页面视图"""
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        """处理注册信息"""
        # 1.接受数据
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

        # 4.应答,使用方向解析跳转首页
        return redirect(reverse('goods:index'))


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

        # 4.应答,使用方向解析跳转首页
        return redirect(reverse('goods:index'))


