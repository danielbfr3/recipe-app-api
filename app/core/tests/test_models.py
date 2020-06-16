from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """It should successfully create a new user with a email"""

        email = "user@test.com"
        password = "Testpass123&"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """It should check if user email is normalized"""

        email = "teste@EMAIL.COM"
        user = get_user_model().objects.create_user(email, "123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_no_email(self):
        """It should raise an error it try to create a user with no email"""

        with self.assertRaises(ValueError):
            email = ""
            user = get_user_model().objects.create_user(email, "123")

    def test_create_new_superuser(self):
        """It should create a now superuser"""

        user = get_user_model().objects.create_superuser("test@user.com", "test123")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
