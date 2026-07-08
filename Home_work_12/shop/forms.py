from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product          # Связываем форму с моделью Product
        fields = ['name', 'description', 'price'] # Какие поля разрешаем заполнять
        
    # Кастомная проверка (валидация): цена не может быть отрицательной
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            # Если цена <= 0, выдаем ошибку, которая покажется в шаблоне
            raise forms.ValidationError("Цена должна быть больше нуля!")
        return price