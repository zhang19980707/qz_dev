from django.conf.urls import url
# from user import views
from user.views import RegisterView

urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^register_handle$', views.register_handle, name='register_handle'),
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册视图类
]
