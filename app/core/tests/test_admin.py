from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email="test@user.com", password="123test"
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="common@user.com", password="123common", name="User Name"
        )

    def test_users_listed(self):
        """it should list users on user page"""

        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """It should test if user edit page works"""

        url = reverse("admin:core_user_change", args=[self.user.id])
        response = self.client.get(url)  # /admin/core/user/1

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """It should test if user page works"""

        url = reverse("admin:core_user_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
