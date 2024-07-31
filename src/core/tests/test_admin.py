from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import admin


class AdminSiteTests(TestCase):

    def setUp(self):
        self.email = "admin@londonapp.com"
        self.password = "Testpass123"
        self.client = Client()
        self.admin_user = AdminSiteTests.create_admin_user()
        self.client.force_login(self.admin_user)
        self.user = AdminSiteTests.create_user()
        return super().setUp()

    @staticmethod
    def create_admin_user():
        """This creates an admin user."""
        email = "admin@londonapp.com"
        password = "Testpass123"
        return get_user_model().objects.create_superuser(email, password)

    @staticmethod
    def create_user():
        """This creates an admin user."""
        email = "user@londonapp.com"
        password = "Testpass123"
        name = "Full name"
        return get_user_model().objects.create_user(email, password, name=name)

    def test_users_list(self):
        """Test that users are created on user page"""
        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse("admin:core_user_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
