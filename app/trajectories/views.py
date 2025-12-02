"""
Trajectories ViewSets
"""
from rest_framework import viewsets, generics, permissions, serializers, authentication
from core.models import Trajectories
from trajectories.serializers import TrajectoriesSerializer


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class TrajectoriesAdminViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD - full control over trajectories EXCEPT editing order after creation
    """
    queryset = Trajectories.objects.all()
    serializer_class = TrajectoriesSerializer
    permission_classes = [IsAdmin]

    def perform_update(self, serializer):
        instance = self.get_object()

        if "order" in serializer.validated_data and serializer.validated_data["order"] != instance.order:
            raise serializers.ValidationError(
                {"order": "Changing trajectory order after creation is not allowed."}
            )

        serializer.save()


class TrajectoriesListForUser(generics.ListAPIView):
    """
    Returns all active trajectories in correct order for users.
    """
    queryset = Trajectories.objects.filter(is_active=True).order_by("order")
    serializer_class = TrajectoriesSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
