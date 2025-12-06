"""
Database models.
"""
from typing import Any, Optional, cast
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.conf import settings


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> "User":
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        user = cast(User, self.model(email=email, **extra_fields))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any
    ) -> "User":
        """Create and return a new superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return f"{self.name} : {self.email}"


class Roadmap(models.Model):
    """roadmap for a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roadmaps'
    )
    career_goal = models.CharField(max_length=255)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"Roadmap for {self.user.email} - "
            f"Career Goal: {self.career_goal}"
        )


class StarPhase(models.Model):
    """Represents a phase in the trajectory."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.order}. {self.name} Phase"
