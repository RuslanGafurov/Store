from django.urls import path

from users.views import user_login_view, user_registration_view

app_name = 'users'

urlpatterns = [
    path('login/', user_login_view, name='login'),
    path('registration/', user_registration_view, name='registration'),
]
