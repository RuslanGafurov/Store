from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product
from products.views import ProductsView


class HomeViewTestCase(TestCase):
    """Тестирование домашней страницы"""
    def test_home_page_view(self) -> None:
        path = reverse('products:home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'home.html')


class ProductsViewTestCase(TestCase):
    """Тестирование страницы с каталогом товаров"""
    fixtures = ['categories.json', 'goods.json']

    def setUp(self) -> None:
        self.products = Product.objects.all()
        self.category = Category.objects.first()
        self.pages = ProductsView.paginate_by

    def _common_tests(self, response, template, title) -> None:
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], title)
        self.assertTemplateUsed(response, template)

    def test_products_view(self) -> None:
        path = reverse('products:products')
        response = self.client.get(path)

        self._common_tests(response, 'products/products.html', 'Store - Каталог')
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products[:self.pages])
        )

    def test_products_view_with_category(self) -> None:
        path = reverse('products:category', kwargs={'category_id': self.category.id})
        response = self.client.get(path)

        self._common_tests(response, 'products/products.html', 'Store - Каталог')
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=self.category.id))
        )
