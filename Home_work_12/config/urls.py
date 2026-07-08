from django.contrib import admin
from django.urls import path, include # Добавь include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Все запросы, начинающиеся с '', отправляем в файл shop/urls.py
    path('', include('shop.urls')), 
]