from django.urls import path

from products.views import HomePageView, ProductsPageView

app_name = 'products'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductsPageView.as_view(), name='products'),
]
