from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse
from booktest.models import BookInfo


# Create your views here.


def my_render(request, templates_path, context=None):
    """封装的render函数"""
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


def index(request):
    """首页视图函数"""
    # return my_render(request, 'booktest/index.html')
    return render(request, 'booktest/index.html')


def login(request):
    """login视图函数"""
    return render(request, 'booktest/index2.html')


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
