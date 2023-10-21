from django.shortcuts import render

from products.models import Category, Product


def home_view(request):
    return render(request, 'home.html')


def products_view(request):
    context = {
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'products/products.html', context)
