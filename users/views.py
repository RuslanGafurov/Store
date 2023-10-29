from django.contrib import auth, messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm

__all__ = (
    'user_login_view',
    'user_registration_view',
    'user_profile_view',
    'user_logout_view',
)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('products:home'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def user_registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно зарегистрирован')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


def user_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно изменены')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'users/profile.html', context)


def user_logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:home'))
