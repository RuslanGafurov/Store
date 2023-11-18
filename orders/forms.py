from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    """Форма оформления заказа"""
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Фамилия',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес для получения заказа',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адрес электронной почты',
    }))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
