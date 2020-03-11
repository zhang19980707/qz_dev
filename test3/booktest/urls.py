from django.conf.urls import url
from booktest import views


urlpatterns = [
    url(r'^index', views.index),  # 返回主页
    url(r'^showarg(\d+)$', views.show_arg),  # 捕获url位置参数
    # url(r'^showarg(?p<num>\d+)$', views.show_arg)  # 捕获关键字参数
    url(r'^login$', views.login),
    url(r'^login_check$', views.login_check),
    url(r'^test_ajax$', views.ajax_test),
    url(r'^ajax_handle$', views.ajax_handle),
    url(r'login_ajax$', views.login_ajax),
    url(r'^login_ajax_check$', views.login_ajax_check),
]