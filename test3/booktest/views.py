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
    # 判断用户是否登录
    if request.session.has_key('islogin'):
        # 用户已登录
        return redirect('/index')
    else:
        # 获取页面cookie username
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    """登录校验"""
    # request.post 保存post方式提交的参数  Querydict类型
    # request.get  保存get提交的参数    Querydict类型
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
            response = redirect('/index')  # 返回一个httpresponseredirect类的对象
            response.set_cookie('username', username, max_age=14*24*3600)  # 设置coolie过期时间为2周

            # 记住用户登录状态
            request.session['islogin'] = True
            return response
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


def set_cookie():
    """设置网页cookie信息"""
    response = HttpResponse('设置cookie')
    # 设置一个cookie信息
    response.set_cookie('num', 1, max_age=14*24*3600)

    return response


def get_cookie(request):
    """获取cookie信息"""
    num = request.COOKIES['num']
    return HttpResponse(num)


def set_session(request):
    """设置seeeion"""
    request.session['username'] = 'zsk'
    request.session['age'] = 18
    return HttpResponse('设置session')


def get_session(request):
    """获取session"""
    username = request.session['username']
    age = request.session['age']
    return HttpResponse(username+":"+str(age))
