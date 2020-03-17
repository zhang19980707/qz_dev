from django.conf.urls import url
# from user import views
from user.views import RegisterView, Active, LoginView

urlpatterns = {
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    # url(r'^send$', views.send, name='send'),
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册视图类
    url(r'^active/(?P<token>.*)$', Active.as_view(), name='active'),
    url(r'^login$', LoginView.as_view(), name='login'),
}
