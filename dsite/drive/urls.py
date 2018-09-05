from django.urls import re_path,path
from . import views
urlpatterns = [re_path(r'index$',views.index,name='index'),
               path('index/<int:number>/', views.index),
               path('details/<int:number>/', views.details)]
