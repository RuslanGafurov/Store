from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('profile/<int:pk>', ProfilePageView.as_view(), name='profile'),
    path('registration/', login_required(RegistrationPageView.as_view()), name='registration'),
    path('logout/', logout_page_view, name='logout'),
]
