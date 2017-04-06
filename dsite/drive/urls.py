from django.conf.urls import url
from . import views
urlpatterns = [url(r'index$',views.index,name='index'),
               url(r'index/(?P<number>[0-9]+)/$', views.index),
               url(r'detail/(?P<number>[0-9]+)/$', views.details)]
