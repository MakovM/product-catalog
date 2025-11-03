from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


User = get_user_model()


class SignUpViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view_get(self):
        response = self.client.get(reverse("accounts:sign-up"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_view_post_creates_user(self):
        data = {
            "username": "newuser",
            "email": "test@admin.com",
            "password1": "Testpass123",
            "password2": "Testpass123",
        }
        response = self.client.post(reverse("accounts:sign-up"), data)
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
