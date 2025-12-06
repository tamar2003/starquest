"""
StarPhase ViewSets
"""
from typing import Any

from rest_framework import (
    viewsets, generics, permissions, serializers, authentication
)
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer

from core.models import StarPhase
from starphase.serializers import StarPhaseSerializer


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the viewset.
    """
    def has_permission(self, request: Request, view: Any) -> bool:
        return request.user.is_staff


class StarPhaseAdminViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD - full control over phases EXCEPT editing order after creation
    """
    queryset = StarPhase.objects.all()
    serializer_class = StarPhaseSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer: BaseSerializer[Any]) -> None:
        instance = self.get_object()
        data = serializer.validated_data

        if "order" in data and data["order"] != instance.order:
            raise serializers.ValidationError({
                "order": "Changing phase order after creation is not allowed."
            })

        serializer.save()


class StarPhaseListForUser(generics.ListAPIView):
    """
    Returns all active starphases in correct order for users.
    """
    queryset = StarPhase.objects.filter(is_active=True).order_by("order")
    serializer_class = StarPhaseSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
