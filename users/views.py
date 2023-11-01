from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import User

__all__ = (
    'LoginPageView',
    'RegistrationPageView',
    'ProfilePageView',
    'logout_page_view',
)


class LoginPageView(TitleMixin, SuccessMessageMixin, LoginView):
    """Отображение авторизации пользователя"""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'
    success_message = 'Вход в аккаунт выполнен'


class RegistrationPageView(TitleMixin, SuccessMessageMixin, CreateView):
    """Отображение регистрации пользователя"""
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    model = User
    title = 'Store - Регистрация'
    success_message = 'Аккаунт успешно создан'
    success_url = reverse_lazy('users:login')


class ProfilePageView(TitleMixin, SuccessMessageMixin, UpdateView):
    """Отображение профиля пользователя"""
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    model = User
    title = 'Store - Личный кабинет'
    success_message = 'Данные успешно изменены'

    def get_context_data(self, **kwargs):
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.id})


def logout_page_view(request):
    """Выход из аккаунта с сообщением"""
    auth.logout(request)
    messages.success(request, 'Выход из аккаунта выполнен')
    return HttpResponseRedirect(reverse('products:home'))
