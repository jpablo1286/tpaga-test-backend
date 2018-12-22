from django.contrib import admin
from django.urls import path
from miniapp import views

urlpatterns = [
    path('admin/', views.AdminView.as_view(), name='Admin'),
    path('open/', views.OpenView.as_view(), name='Open'),
]
