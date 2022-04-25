from django.urls import path

from catapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cat/<cat_id>', views.cat, name="cat"),
    path('cats', views.cat_list, name="cats"),
    path('search_cat', views.search_cat, name="search_cat"),
    path('advanced_search', views.advanced_search, name="advanced_search"),
    path('catinfo', views.cat_info_list, name="catInfo"),
    path('breedinfo/<cat_id>', views.breed_info, name="breedInfo"),
]