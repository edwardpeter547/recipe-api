from urllib import response
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse("recipe:tag-list")


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        user_data = {"email": "test@retepsystemsltd.com", "password": "testPassword"}
        self.user = get_user_model().objects.create_user(**user_data)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags."""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")
        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        new_user = get_user_model().objects.create_user(
            email="other@retepsystemsltd.com", password="testPassword"
        )
        Tag.objects.create(user=new_user, name="Comfort Food")
        tag = Tag.objects.create(user=self.user, name="Dessert")

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], tag.name)
