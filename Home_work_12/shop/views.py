# shop/views.py
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Product
from .forms import ProductForm


# 1. Список товаров (аналог функции product_list)
class ProductListView(ListView):
    model = Product                              # Какую модель использовать
    template_name = 'shop/product_list.html'     # Какой шаблон рендерить
    context_object_name = 'products'             # Имя переменной в шаблоне


# 2. Детали товара (аналог функции product_detail)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'


# 3. Создание товара (аналог функции product_create)
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm                     # Какую форму использовать
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('product_list')   # Куда редиректить после сохранения


# 4. Редактирование товара (аналог функции product_update)
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('product_list')


# 5. Удаление товара (НОВОЕ!)
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')