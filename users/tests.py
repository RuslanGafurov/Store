from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class RegistrationViewTestCase(TestCase):
    """Тестирование регистрации пользователя"""
    def setUp(self) -> None:
        self.data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username',
            'email': 'test_email@testmail.com',
            'password1': 'TestPassword163',
            'password2': 'TestPassword163',
        }
        self.path = reverse('users:registration')
        self.username = self.data['username']

    def _common_tests(self, response, template, title) -> None:
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], title)
        self.assertTemplateUsed(response, template)

    def test_registration_view_get(self) -> None:
        response = self.client.get(self.path)
        self._common_tests(response, 'users/registration.html', 'Store - Регистрация')

    def test_registration_view_post_success(self) -> None:
        self.assertFalse(User.objects.filter(username=self.username).exists())
        response = self.client.post(self.path, self.data)

        # Проверка создания аккаунта
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username=self.username).exists())

        # Проверка создания кода подтверждения
        verification = EmailVerification.objects.filter(user__username=self.username)
        self.assertTrue(verification.exists())
        self.assertEqual(
            verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def registration_view_post_error(self) -> None:
        User.objects.create(username=self.username)
        response = self.client.post(self.path, self.data)
        self._common_tests(response, 'users/registration.html', 'Store - Регистрация')
        self.assertContains(response, 'Пользователь с таким именем уже существует', html=True)
