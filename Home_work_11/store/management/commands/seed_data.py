from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from store.models import Category, Product
from factory.django import DjangoModelFactory

# Опционально: можно использовать factory_boy, но для простоты — вручную
fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Генерирует тестовые данные для категорий и товаров'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='Количество категорий для создания'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=20,
            help='Количество товаров для создания'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        categories_count = options['categories']
        products_count = options['products']
        
        self.stdout.write('🌱 Начинаю генерацию данных...')
        
        # Создаём категории
        categories = []
        for i in range(categories_count):
            cat, created = Category.objects.get_or_create(
                name=fake.word().title(),
                defaults={'description': fake.sentence()}
            )
            if created:
                categories.append(cat)
                self.stdout.write(f'✓ Категория: {cat.name}')
        
        # Создаём товары
        for i in range(products_count):
            Product.objects.create(
                name=fake.catch_phrase(),
                description=fake.paragraph(),
                price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                category=fake.random_element(categories) if categories else Category.objects.first()
            )
            if (i + 1) % 5 == 0:
                self.stdout.write(f'→ Создано товаров: {i + 1}/{products_count}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Готово! Создано категорий: {len(categories)}, товаров: {products_count}'
            )
        )