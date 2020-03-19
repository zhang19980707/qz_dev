from django.conf.urls import url
from booktest import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^delete(\d+)/$', views.delete),
    url(r'^create/$', views.create),
    url(r'^areas$', views.areas),
]