"""
Tests for the user API.
"""
from typing import Any, cast
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status

from core.models import User


CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


def create_user(**params: Any) -> User:
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests for unauthenticated user API requests."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self) -> None:
        payload = {
            'email': 'test@example.com',
            'password': 'strongpass123'
        }
        res = cast(
            Response,
            self.client.post(CREATE_USER_URL, payload)
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_token_created(self) -> None:
        user = create_user(
            email='test@example.com',
            password='strongpass123'
        )
        payload = {'email': user.email, 'password': 'strongpass123'}
        res = cast(
            Response,
            self.client.post(TOKEN_URL, payload)
        )
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_invalid_credentials(self) -> None:
        create_user(
            email='test@example.com',
            password='testpass'
        )
        payload = {'email': 'test@example.com', 'password': 'wrongpass'}
        res = cast(
            Response,
            self.client.post(TOKEN_URL, payload)
        )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Tests for authenticated requests."""

    def setUp(self) -> None:
        self.user = create_user(
            email='user@example.com',
            password='strongpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self) -> None:
        res = cast(
            Response,
            self.client.get(ME_URL)
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'email': self.user.email})
