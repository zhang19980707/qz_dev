from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.
"""
request是httprequest的一个对象
request包含一些浏览器的提交信息
"""


def index(request):
    # num = "1" + 1
    return render(request, 'booktest/index.html')


def show_arg(num):

    return HttpResponse(num)


def login(request):
    """显示登录页面"""
    return render(request, 'booktest/login.html')


def login_check(request):
    """登录校验"""
    # request.post 保存post方式提交的参数  Querydict类型
    # request.get  保存get提交的参数    Querydict类型
    # 1.校验密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # print(username+":"+password)
    # 1.1 根据用户名和密码在数据库中查找数据
    if username == "admin" and password == "123456":
        "登录成功,跳转首页"
        return redirect('/index')
    else:
        "登录失败，跳转登录页"
        return redirect('/login')
    # 2.相应页面
    # return HttpResponse('ok')


def ajax_test(request):
    """显示ajax页面"""
    return render(request, 'booktest/ajax.html')


def ajax_handle():
    """处理ajax请求"""
    # 返回一个数据{‘res’:1}
    return JsonResponse({'res': 1})


def login_ajax(request):
    """ajax登录页"""
    return render(request, 'booktest/login_ajax.html')


# login_ajax_check
def login_ajax_check(request):
    """
    ajax登录校验
    ajax请求返回的是一个json，不是一个页面
    """
    # 1.获取用户名、密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # print(username+":"+password)

    # 2. 根据用户名和密码在数据库中查找数据
    if username == "admin" and password == "123456":
        "登录成功,跳转首页"
        return JsonResponse({'res': 1})
    else:
        "登录失败，跳转登录页"
        return JsonResponse({'res': 0})
