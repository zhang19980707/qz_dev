from django.shortcuts import render

# Create your views here.


def index(request):
    """首页视图"""
    return render(request, 'base.html')
