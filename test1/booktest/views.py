from django.shortcuts import render
from django.http import HttpResponse
from booktest.models import BookInfo, HeroInfo
from django.template import loader, RequestContext
# Create your views here.
# http://127.0.0.1:8000/index
# 1.定义视图
# 2.配置url，建立url地址和视图对应


def my_render(request, template_path, context_dict=None):
    # 进行处理，和M和T进行交互。。。。
    # return HttpResponse("hello")
    # 使用模板文件
    # 1.加载模板文件
    if context_dict is None:
        context_dict = {}
    temp = loader.get_template(template_path)

    # 2.定义模板文件上下文：给模板文件创建数据
    context = RequestContext(request, context_dict)

    # 3.模板渲染
    res_html = temp.render(context)
    # 4.返回给浏览器
    return HttpResponse(res_html)


# 首页，展示所有图书
def index(reqeust):
    # 查询所有图书
    booklist = BookInfo.objects.all()
    # 将图书列表传递到模板中，然后渲染模板
    return render(reqeust, 'booktest/index.html', {'booklist': booklist})


# 详细页，接收图书的编号，根据编号查询，再通过关系找到本图书的所有英雄并展示
def detail(reqeust, bid):
    # 根据图书编号对应图书
    book = BookInfo.objects.get(id=int(bid))
    # 查找book图书中的所有英雄信息
    heros = book.heroinfo_set.all()
    # 将图书信息传递到模板中，然后渲染模板
    return render(reqeust, 'booktest/detail.html', {'book': book, 'heros': heros})

