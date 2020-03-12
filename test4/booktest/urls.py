from django.conf.urls import url
from booktest import views


urlpatterns = [
    url(r'^index$', views.index),
    url(r'^login$', views.login),
    url(r'^temp_var', views.temp_var),
    url(r'^temp_tags', views.temp_tags),
    url(r'^temp_filter$', views.temp_filter),
]
