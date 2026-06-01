from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    """Публичная страница со списком товаров"""
    # Получаем все товары с подгрузкой категории (оптимизация запросов)
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'title': 'Каталог товаров'
    }
    return render(request, 'store/product_list.html', context)


def category_detail(request, category_id):
    """Страница категории с фильтрацией товаров"""
    category = Category.objects.get(id=category_id)
    products = category.products.all()
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
        'title': f'Товары категории: {category.name}',
        'current_category': category
    })
