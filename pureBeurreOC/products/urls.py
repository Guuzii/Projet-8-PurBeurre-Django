from django.urls import include, path

from . import views


urlpatterns = [    
    path('', views.index),
    path('search-results/', views.searchResults),
    path('user-results/', views.userResults),
]