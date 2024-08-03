from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")


class Base(TestCase):
    """The base class for the public and private test cases"""

    def setUp(self):
        self.client = APIClient()


class PublicIngredientApiTests(Base):
    """Test the publicly available ingredients API"""

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(Base):
    """Test private ingredients API"""

    def setUp(self):
        super().setUp()
        user_data = {"email": "test@retepsystemsltd.com", "password": "testPassword"}
        self.user = get_user_model().objects.create_user(**user_data)
        self._authenticate()

    def _authenticate(self):
        if hasattr(self, "client"):
            self.client.force_authenticate(self.user)
        else:
            self.client = APIClient()
            self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name="Kale")
        Ingredient.objects.create(user=self.user, name="Salt")

        response = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only ingredients for the authenticated user are returned."""

        temp_user = get_user_model().objects.create_user(
            email="temp@retepsystemsltd.com", password="password"
        )

        Ingredient.objects.create(user=temp_user, name="Maggi")
        ingredients = Ingredient.objects.create(user=self.user, name="Onion")

        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], ingredients.name)
