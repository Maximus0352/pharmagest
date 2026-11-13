from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'Test-password-123!'
        get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_custom_user_model_is_configured(self):
        from .models import User

        self.assertIs(get_user_model(), User)

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.username, 'password': self.password},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'utilisateurs/accueil.html')

    def test_login_with_invalid_credentials_is_rejected(self):
        response = self.client.post(
            reverse('login'),
            {'username': self.username, 'password': 'incorrect'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue(response.context['form'].errors)

    def test_private_page_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse('accueil'))

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("accueil")}',
        )

    def test_logout_ends_session_and_redirects_to_login(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTemplateUsed(response, 'registration/login.html')
