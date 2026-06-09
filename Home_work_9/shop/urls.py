from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),               # Адрес: /
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # Адрес: /product/1/
    path('product/new/', views.product_create, name='product_create'),      # Адрес: /product/new/
    path('product/<int:pk>/edit/', views.product_update, name='product_update'), # Адрес: /product/1/edit/
]