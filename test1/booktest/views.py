from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# http://127.0.0.1:8000/index
# 1.定义视图
# 2.配置url，建立url地址和视图对应

def index(request):
    # 进行处理，和M和T进行交互。。。。
    return HttpResponse("hello")
