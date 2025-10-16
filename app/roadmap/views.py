"""
ViewSets for managing roadmaps.
"""
from typing import Any, Type, cast

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.serializers import Serializer
from rest_framework.exceptions import APIException
from rest_framework.serializers import BaseSerializer


from django.db.models import QuerySet

from roadmap.serializers import RoadmapSerializer, RoadmapCreateSerializer
from roadmap import ai_service
from core.models import Roadmap


class RoadmapViewSet(viewsets.ModelViewSet):
    """View for managing roadmaps."""
    queryset = Roadmap.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Roadmap]:
        """Return only the roadmap of the current user."""
        user = self.request.user
        return self.queryset.filter(
            user=cast(Any, user)
        ).order_by('-created_at')

    def get_serializer_class(self) -> Type[Serializer]:
        """Choose serializer based on action."""
        if self.action == 'create':
            return RoadmapCreateSerializer
        return RoadmapSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Create a new roadmap and generate items based on AI call."""
        user = self.request.user

        existing_roadmap = self.queryset.filter(user=cast(Any, user)).first()
        if existing_roadmap:
            existing_roadmap.delete()

        roadmap = serializer.save(user=user)
        try:
            ai_response = ai_service.generate_roadmap(roadmap.career_goal)
        except ai_service.AIServiceError as e:
            raise APIException(detail=f"Failed to generate roadmap: {e}")

        roadmap.details = ai_response
        roadmap.save()
