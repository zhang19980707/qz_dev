from django.conf.urls import url
from booktest import views

index_ = [url(r'^index', views.index), ]
urlpatterns = index_