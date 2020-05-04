from django.urls import include, path

from . import views


urlpatterns = [    
    path('', views.index),
    path('search-results/', views.searchResults, name='product-search-results'),
    path('user-results/', views.userResults, name='product-user-results'),
]