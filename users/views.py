from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User

__all__ = (
    'LoginPageView',
    'RegistrationPageView',
    'ProfilePageView',
    'logout_page_view',
    'VerificationPageView',
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

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.id})


def logout_page_view(request):
    """Выход из аккаунта с сообщением"""
    auth.logout(request)
    messages.success(request, 'Выход из аккаунта выполнен')
    return HttpResponseRedirect(reverse('products:home'))


class VerificationPageView(TitleMixin, TemplateView):
    """Отображение верификации пользователя"""
    template_name = 'users/verification.html'
    title = 'Store - Верификация'

    def get(self, request, *args, **kwargs):
        """Подтверждение верификации"""
        user = User.objects.get(email=kwargs['email'])
        code = kwargs['code']
        verifications = EmailVerification.objects.filter(user=user, code=code)
        if verifications.exists() and not verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(VerificationPageView, self).get(request, *args, **kwargs)
        else:
            HttpResponseRedirect(reverse('home'))
