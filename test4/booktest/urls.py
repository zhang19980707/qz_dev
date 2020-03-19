from django.conf.urls import url
from booktest import views


urlpatterns = [
    url(r'^index$', views.index),
    url(r'^login$', views.login),
    url(r'^login_check$', views.login_check),
    url(r'^change_pwd$', views.change_pwd),
    url(r'^change_pwd_action$', views.change_pwd_action),
    url(r'^temp_var$', views.temp_var),
    url(r'^temp_tags$', views.temp_tags),
    url(r'^temp_filter$', views.temp_filter),
    url(r'^temp_inherit$', views.temp_inherit),
    url(r'^html_escape$', views.html_escape),
]
