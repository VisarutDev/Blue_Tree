from django.urls import path, include
from blue_tree_app import views

urlpatterns = [
    # path('CreateTokenUser',views.CreateTokenUser.as_view()),
    path('RefreshTokenAPI',views.RefreshTokenAPI.as_view()),
    path('Register',views.Register.as_view()),
    path('confirm_email',views.ConfirmEmail.as_view()),
    path('login',views.LoginApp.as_view()),
    path('forget_password',views.ForgetPassword.as_view()),
    path('get/banner/home_page',views.GetBannerHomePage.as_view()),
    path('get/promotion/home_page',views.GetPromotionHomePage.as_view()),
    path('get/service/home_page',views.GetServiceHomePage.as_view()),
    path('get/happening/home_page',views.GetHappeningHomePage.as_view()),
    path('get/notification/home_page',views.GetNotificationHomePage.as_view()),
    path('get/user/infromation',views.GetInformation.as_view()),
    path('test',views.Test.as_view())
]