from django.urls import path

from catapp import views

urlpatterns = [
    path('', views.home, name="home"),
]