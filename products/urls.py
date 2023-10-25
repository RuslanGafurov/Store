from django.urls import path

from products.views import HomePageView, ProductsPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductsPageView.as_view(), name='products'),
]
