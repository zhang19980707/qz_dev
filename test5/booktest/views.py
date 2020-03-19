from django.shortcuts import render

# Create your views here.


def index(request):
    """网站首页"""
    # 获取浏览器端ip地址
    user_ip = request.META['REMOTE_ADDR']
    print(user_ip)
    return render(request, 'booktest/index.html')


def static_test(request):
    """展示静态文件"""
    return render(request, 'booktest/static_test.html')
