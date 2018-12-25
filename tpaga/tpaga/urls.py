"""
Author: Juan Pablo Rivera Velasco
Version: 1.0
Correo: jpablo.localhost@gmail.com

Este archivo contiene el mapeo de las URL con las vistas de la aplicación, así mismo los parametros de
dichas URLs.
"""
from django.contrib import admin
from django.urls import path
from miniapp import views

urlpatterns = [
    path('key/create', views.CreateKey.as_view(), name='CreateKey'), #almacena las llaves de integración de la tienda con terceros, en este caso tpaga
    # Mapeo de metodos para creación, listado y eliminación de items, se omiten otros por sencilles de implementación
    path('item/list', views.ListItems.as_view(), name='ListItems'),
    path('item/create', views.CreateItems.as_view(), name='CreateItems'),
    path('item/delete/<str:itemId>', views.DeleteItem.as_view(), name='DeleteItem'),
    # Mapeo de metodos para ordenes
    path('order/list', views.ListOrders.as_view(), name='ListOrders'),
    path('order/info/<str:id>', views.InfoOrder.as_view(), name='InfoOrder'),
    path('order/checkout/<str:id>', views.CheckOutOrder.as_view(), name='CheckOutOrder'),
    path('order/confirm/<str:id>', views.ConfirmOrder.as_view(), name='ConfirmOrder'),
    path('order/refund/<str:id>', views.RefundOrder.as_view(), name='RefundOrder'),
    path('order/create', views.CreateOrder.as_view(), name='CreateOrder'),
    # metodos para asociar un item a una orden (agregar al carrito)
    path('purchaseditem/create', views.CreatePurchasedItem.as_view(), name='CreatePurchasedItem'),
    path('purchaseditem/listbyorderid/<str:orderId>', views.ListPurchasedItemsByOrderId.as_view(), name='ListPurchasedItemsByOrderId'),
    path('purchaseditem/delete/<str:itemId>', views.DeletePurchasedItem.as_view(), name='DeletePurchasedItem'),
]
