from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [    
    path('', views.index, name='home'),
    path('user/', views.user, name='user'),
    # path('user/login', auth_views.LoginView, name='login'),
    # path('user/logout', auth_views.LogoutView, name='logout'),
    path('user/sign-up', views.userCreate, name='user-create'),
    path('user/login', views.UserLogin, name='login'),
    path('user/logout', views.UserLogout, name='logout'),
    path('search-results/', views.searchResults, name='product-search-results'),
    path('user-results/', views.userResults, name='product-user-results'),
    path('details/<int:product_id>', views.productDetails, name='product-details'),
]