"""
Stage ViewSets
"""
from rest_framework import viewsets, generics, permissions, serializers
from core.models import Stage
from stages.serializers import StageSerializer


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class StageAdminViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD - full control over stages EXCEPT editing order after creation
    """
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        instance = self.get_object()

        if "order" in serializer.validated_data and serializer.validated_data["order"] != instance.order:
            raise serializers.ValidationError(
                {"order": "Changing stage order after creation is not allowed."}
            )

        serializer.save()


class StageListForUser(generics.ListAPIView):
    """
    Returns all active stages in correct order for users.
    """
    queryset = Stage.objects.filter(is_active=True).order_by("order")
    serializer_class = StageSerializer
    permission_classes = [permissions.IsAuthenticated]
