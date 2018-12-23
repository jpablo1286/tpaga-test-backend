from django.contrib import admin
from django.urls import path
from miniapp import views

urlpatterns = [
    path('admin/', views.AdminView.as_view(), name='Admin'),
    path('key/create', views.CreateKey.as_view(), name='CreateKey'),
    path('item/list', views.ListItems.as_view(), name='ListItems'),
    path('item/create', views.CreateItems.as_view(), name='CreateItems'),
    path('order/list', views.ListOrders.as_view(), name='ListOrders'),
    path('order/info/<str:id>', views.InfoOrder.as_view(), name='InfoOrder'),
    path('order/checkout/<str:id>', views.CheckOutOrder.as_view(), name='CheckOutOrder'),
    path('order/create', views.CreateOrder.as_view(), name='CreateOrder'),
    path('purchaseditem/create', views.CreatePurchasedItem.as_view(), name='CreatePurchasedItem'),
    path('purchaseditem/listbyorderid/<str:orderId>', views.ListPurchasedItemsByOrderId.as_view(), name='ListPurchasedItemsByOrderId'),
    path('purchaseditem/delete/<str:itemId>', views.DeletePurchasedItem.as_view(), name='DeletePurchasedItem'),
]
