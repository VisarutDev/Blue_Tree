from django.contrib import admin
from django.urls import path, include
from blue_tree_api import views

urlpatterns = [
    path('createToken',views.CreateToken.as_view()),
    path('refreshToken',views.RefreshTokenAPI.as_view()),
    path('check_user',views.UserTestRefreshToken.as_view()),
    path('register',views.Register.as_view()),
    path('check',views.Apicheck.as_view()),
]