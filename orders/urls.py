from django.urls import path

from orders.views import *

app_name = 'orders'

urlpatterns = [
    path('success/', SuccessOrderView.as_view(), name='success'),
    path('cancel/', CancelOrderView.as_view(), name='cancel'),
    path('create/', OrderCreateView.as_view(), name='create'),
]
