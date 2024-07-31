from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager


class ModelTests(TestCase):

    def setUp(self):
        self.email = "test@LONDONAPPDEV.COM"
        self.password = "Testpass123"
        return super().setUp()

    def normalize_email(self, email):
        return BaseUserManager.normalize_email(email)

    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful.
        """
        user = get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        self.assertEqual(user.email, self.normalize_email(self.email))
        self.assertTrue(user.check_password(self.password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        user = get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        self.assertEqual(user.email, self.normalize_email(self.email))

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, self.password)

    def test_create_super_user(self):
        """Test custom user model can create super user"""

        user = get_user_model().objects.create_superuser(self.email, self.password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
