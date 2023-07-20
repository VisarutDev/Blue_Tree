from django.contrib import admin
from django.urls import path, include
from blue_tree_bof import views

urlpatterns = [
    # path('get/fill_type',views.GetFillType.as_view()),
    path('manage/order',views.ManageOrderBof.as_view()),
    path('manage/fill_list',views.ManageFillList.as_view()),
    path('manage/sub_fill',views.ManageSubFillList.as_view()),
    path('get/fill_list/sub_fill',views.GetFillListAndSubFill.as_view()),
    path('get/order/by_id',views.GetOrderById.as_view()),
    path('get/channel_type',views.GetChannelType.as_view()),
    path('genOrderCode',views.GenOrderCode.as_view()),
    path('manage/promotion',views.ManagePromotion.as_view()),
    path('chang/status/promotion',views.ChangStatusPromotion.as_view()),
    path('get/all/promotion',views.GetAllPromotion.as_view()),
    path('manage/happening',views.ManageHappening.as_view()),
    path('chang/status/happening',views.ChangStatusHappening.as_view()),
    path('get/all/happening',views.GetAllHappening.as_view()),
    path('manage/banner',views.ManageBanner.as_view()),
    path('chang/status/banner',views.ChangStatusBanner.as_view()),
    path('get/all/banner',views.GetAllBanner.as_view()),
    path('manage/users',views.ManageUsers.as_view()),
    path('get/all/users',views.GetAllUser.as_view()),
]