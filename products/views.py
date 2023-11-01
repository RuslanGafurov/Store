from django.views.generic import ListView, TemplateView

from common.views import TitleMixin
from products.models import Category, Product


class HomePageView(TitleMixin, TemplateView):
    """Отображение домашней страницы"""
    template_name = 'home.html'
    title = 'Store'


class ProductsPageView(TitleMixin, ListView):
    """Отображение каталога товаров"""
    template_name = 'products/products.html'
    title = 'Store - Каталог'
    model = Product
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(ProductsPageView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductsPageView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset
