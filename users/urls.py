from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('profile/', user_profile_view, name='profile'),
    path('registration/', user_registration_view, name='registration'),
]
