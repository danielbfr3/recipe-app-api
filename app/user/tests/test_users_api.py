from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

USER_CREATE_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test Public User API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_sucess(self):
        """It should sucessfully create a new user"""
        payload = {
            "email": "test@user.com",
            "password": "123123test",
            "name": "Test User",
        }
        response = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)

        self.assertTrue(user.check_password(payload["password"]))
        self.assertTrue(user.email == payload["email"])
        self.assertTrue(user.name == payload["name"])
        self.assertNotIn("password", response.data)

    def test_create_user_already_exists(self):
        """It should fail if the user try to creata a already existing user"""
        payload = {
            "email": "test@user.com",
            "password": "123123test",
            "name": "Test User",
        }
        create_user(**payload)

        response = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """It should reject a new user if password is too short (less than 5 characteres)"""
        payload = {
            "email": "test@user.com",
            "password": "123",
            "name": "Test User",
        }

        response = self.client.post(USER_CREATE_URL, payload)

        self.assertTrue(response.status_code == status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_valid_credentials(self):
        """It should create a token for valid user"""
        payload = {
            "email": "test@user.com",
            "password": "123123test",
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_for_invalid_credentials(self):
        """It should not create a token for invalid user"""
        create_user(
            email="test@user.com", password="123123test",
        )
        payload = {
            "email": "test@user.com",
            "password": "invalidpassword",
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """It should not create a token if user does not exist"""
        payload = {
            "email": "test@user.com",
            "password": "123123test",
        }
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """It should not create a token user and password are not provided"""
        response = self.client.post(
            TOKEN_URL, {"email": "test@user.com", "password": ""}
        )

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
