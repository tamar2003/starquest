"""
Tests for models.
"""
from typing import Any, cast
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError


from core.models import Roadmap, Stage


class ModelTests(TestCase):
    """Test models."""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='pass123'
        )

    def test_create_user_with_email_successful(self) -> None:
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name='Test User'
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, "Test User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalized(self) -> None:
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self) -> None:
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='test123'
            )

    def test_create_superuser(self) -> None:
        """Test creating a superuser."""
        superuser = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='Adminpass123',
            name='Admin User'
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_roadmap_successful(self) -> None:
        """Test creating a roadmap is successful."""
        career_goal = "Become a Data Scientist"
        details = (
            "Essential Learning:...\n"
            "Industry Essential Learning:...\n"
            "UpSkill Learning:..."
        )
        roadmap = Roadmap.objects.create(
            user=self.user,
            career_goal=career_goal,
            details=details
        )
        self.assertEqual(roadmap.user, self.user)
        self.assertEqual(roadmap.career_goal, career_goal)
        self.assertEqual(roadmap.details, details)
        self.assertIsNotNone(roadmap.created_at)

    def test_create_roadmap_without_user_raises_error(self) -> None:
        """Test that creating a roadmap without a user raises an Error."""
        with self.assertRaises(IntegrityError):
            Roadmap.objects.create(
                user=cast(Any, None),
                career_goal="Become a Data Scientist",
                details="Some details"
            )

    def test_create_stage_successful(self) -> None:
        """Test creating a stage is successful."""

        stage = Stage.objects.create(
            name="Stage 1",
            description="Description for Stage 1",
            order=1,
            is_active=True
        )
        self.assertEqual(stage.name, "Stage 1")
        self.assertEqual(stage.description, "Description for Stage 1")
        self.assertEqual(stage.order, 1)
        self.assertTrue(stage.is_active)
        self.assertIsNotNone(stage.created_at)
        self.assertIsNotNone(stage.updated_at)

    def test_create_stage_with_duplicate_order_raises_error(self) -> None:
        """Test that creating a stage with duplicate order raises an IntegrityError."""

        Stage.objects.create(
            name="Stage 1",
            description="Description for Stage 1",
            order=1,
            is_active=True
        )
        with self.assertRaises(IntegrityError):
            Stage.objects.create(
                name="Stage 2",
                description="Description for Stage 2",
                order=1,
                is_active=True
            )

    def test_stage_string_representation(self) -> None:
        """Test the string representation of a Stage."""
        stage = Stage.objects.create(
            name="Nabula",
            description="Description for Stage 1",
            order=1,
            is_active=True
        )
        self.assertEqual(str(stage), "1. Nabula Stage")