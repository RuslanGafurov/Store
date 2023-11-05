from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket, Category, Product

__all__ = (
    'HomePageView',
    'ProductsPageView',
    'basket_add',
    'basket_remove',
)


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


@login_required
def basket_add(request, product_id):
    """Добавление товара в корзину"""
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    """Удаление товара из корзины"""
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
