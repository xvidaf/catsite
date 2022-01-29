from django.urls import path

from catapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cat/<cat_id>', views.cat, name="cat"),
]