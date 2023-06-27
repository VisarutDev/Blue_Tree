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
    path('genOrderCode',views.GenOrderCode.as_view())
]