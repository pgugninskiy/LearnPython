from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

# 1. Показать список всех товаров
def product_list(request):
    products = Product.objects.all() # Берем все товары из БД
    return render(request, 'shop/product_list.html', {'products': products})

# 2. Показать один конкретный товар
def product_detail(request, pk): # pk - это id товара из адресной строки
    product = get_object_or_404(Product, pk=pk) # Ищем товар или выдаем ошибку 404
    return render(request, 'shop/product_detail.html', {'product': product})

# 3. Добавить новый товар
def product_create(request):
    if request.method == 'POST': # Если пользователь НАЖАЛ КНОПКУ "Сохранить"
        form = ProductForm(request.POST) # Заполняем бланк данными от пользователя
        if form.is_valid():              # Проверяем, нет ли ошибок (например, цена > 0)
            form.save()                  # Если всё ок, сохраняем в БД
            return redirect('product_list') # Перекидываем пользователя на список товаров
    else: # Если пользователь просто ЗАШЕЛ на страницу (GET-запрос)
        form = ProductForm() # Создаем пустой бланк
        
    return render(request, 'shop/product_form.html', {'form': form})

# 4. Редактировать существующий товар
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        # Заполняем бланк новыми данными и говорим, какой именно товар меняем (instance=product)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        # Показываем бланк, уже заполненный текущими данными товара
        form = ProductForm(instance=product)
        
    return render(request, 'shop/product_form.html', {'form': form})
