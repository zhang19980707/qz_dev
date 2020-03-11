from django.shortcuts import render, redirect
from booktest.models import BookInfo, HeroInfo, AreaInfo
from datetime import date
from django.http import HttpResponseRedirect
# Create your views here.


# 查询所有图书并显示
def index(request):
    list = BookInfo.objects.all()
    return render(request, 'booktest/index.html', {'list': list})


# 创建新图书
def create(request):
    book = BookInfo()
    book.btitle = '流星蝴蝶剑'
    book.bpub_date = date(1995, 12, 30)
    book.save()
    # 转向到首页,重定向
    # return HttpResponseRedirect(redirect_to='/')    # 方法1
    return redirect('/index')


# 逻辑删除指定编号的图书
def delete(request, bid):
    book = BookInfo.objects.get(id=int(bid))
    book.delete()
    # 转向到首页
    # return HttpResponseRedirect(redirect_to='/')  # 方法1
    return redirect('/index')


# 查询广州市的信息
def areas(request):
    area = AreaInfo.objects.get(pk=440100)   # 按编号获得城市信息，返回一个object
    return render(request, 'booktest/area.html', {'area': area})