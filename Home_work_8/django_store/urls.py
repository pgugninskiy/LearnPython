from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),  # ← подключаем наше приложение
    # Опционально: главная страница проекта
    path('', lambda request: render(request, 'index.html'), name='home'),
]