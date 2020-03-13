from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from booktest.models import BookInfo


# Create your views here.

"""
def my_render(request, templates_path, context=None):
    "自己封装的render函数"
    # 1. 加载模板，获取模板内容，产生一个模板对象
    if context is None:
        context = {}
    temp = loader.get_template(templates_path)

    # 2.定义模板上下文，给模板文件传递数据
    context = RequestContext(request, context)

    # 3.模板渲染，产生一个替换后的html对象
    res_html = temp.render(context)

    # 4.返回页面
    return HttpResponse(res_html)
"""


def login_required(view_func):
    """判断登录的装饰器函数"""
    def wrapper(request, *view_args, **kwview_kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录，调用对应的视图
            return view_func(request, *view_args, **kwview_kwargs)
        else:
            # 用户未登录，跳转一个相应页面
            return redirect('/login')

    return wrapper


def index(request):
    """首页视图函数"""
    # return my_render(request, 'booktest/index.html')
    return render(request, 'booktest/index.html')


def login(request):
    """显示登录页面"""
    # 判断用户是否登录
    if request.session.has_key('islogin'):
        # 用户已登录
        return redirect('/change_pwd')
    else:
        # 获取页面cookie username
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    """登录校验"""
    # 1.校验密码
    username = request.POST.get('username')  # get的是input标签的name值
    password = request.POST.get('password')
    # print(username+":"+password)

    # 获取remember值，判断cookie
    remember = request.POST.get('remember')

    # 2. 根据用户名和密码在数据库中查找数据
    if username == "admin" and password == "123456":
        "登录成功,跳转首页"
        # 根据cookie判断是否需要记住用户名
        if remember == 'on':
            response = redirect('/change_pwd')  # 返回一个httpresponseredirect类的对象
            response.set_cookie('username', username, max_age=14*24*3600)  # 设置coolie过期时间为2周

            # 记住用户登录状态
            request.session['islogin'] = True
            # 记住用户名
            request.session['username'] = username

            return response
    else:
        "登录失败，跳转登录页"
        return redirect('/login')
    # 2.相应页面
    # return HttpResponse('ok')


@login_required
def change_pwd(request):
    """显示修改密码页面"""
    return render(request, 'booktest/change_pwd.html')


@login_required
def change_pwd_action(request):
    """模拟修改密码"""
    # 1.获取新密码
    pwd = request.POST.get('pwd')
    username = request.session['username']
    # 2.实际开发时， 修改数据库中的内容

    # 3.提供用户反馈
    return HttpResponse("%s修改密码为%s" % (str(username), str(pwd)))


def temp_var(request):
    """模板变量"""
    my_dict = {'title': '字典键值对'}
    my_list = [1, 2, 3]
    book = BookInfo.objects.get(id=2)

    context = {'my_dict': my_dict, 'my_list': my_list, 'book': book}
    return render(request, 'booktest/temp_var.html', context)


def temp_tags(request):
    """模板标签视图"""
    # 1.查找图书信息
    books = BookInfo.objects.all()

    # 2.传递模板变量
    return render(request, 'booktest/temp_tags.html', {'books': books})


def temp_filter(request):
    """定义模板过滤器"""
    books = BookInfo.objects.all()
    return render(request, 'booktest/temp_filter.html', {'books': books})


def temp_inherit(request):
    """模板继承"""
    return render(request, 'booktest/child.html')


def html_escape(request):
    """模板转义"""
    return render(request, 'booktest/html_escape.html',  {'context': '<h1>hello</h1>'})

