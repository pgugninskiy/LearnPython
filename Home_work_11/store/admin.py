from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'products_count')
    search_fields = ('name', 'description')
    #prepopulated_fields = {'slug': ('name',)}  # если добавите поле slug
    
    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'is_expensive')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'price')
        }),
        ('Дополнительно', {
            'fields': ('description', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_expensive(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'red' if obj.price > 1000 else 'green',
            'Дорого' if obj.price > 1000 else 'Доступно'
        )
    is_expensive.short_description = 'Статус цены'