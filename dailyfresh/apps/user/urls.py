from django.conf.urls import url
from django.contrib.auth.decorators import login_required  # 引用django内部认证系统的登录装饰器函数login_required
# from user import views
from user.views import RegisterView, Active, LoginView, UserInfoView, UserOrderView, UserSiteView, LogoutView

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    # url(r'^send$', views.send, name='send'),
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册视图类
    url(r'^active/(?P<token>.*)$', Active.as_view(), name='active'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    # url(r'^$', login_required(UserInfoView.as_view()), name='user'),
    # url(r'^order$', login_required(UserOrderView.as_view()), name='order'),
    # url(r'^address$', login_required(UserSiteView.as_view()), name='address'),
    url(r'^$', UserInfoView.as_view(), name='user'),
    url(r'^order$', UserOrderView.as_view(), name='order'),
    url(r'^address$', UserSiteView.as_view(), name='address'),
]
