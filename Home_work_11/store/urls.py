from django.urls import path
from . import views

app_name = 'store'  # пространство имён для URL

urlpatterns = [
    path('', views.product_list, name='product_list'),           # /store/
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  # /store/category/1/
]