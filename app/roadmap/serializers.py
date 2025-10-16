from rest_framework import serializers
from core.models import Roadmap


class RoadmapSerializer(serializers.ModelSerializer):
    """Serializer for Roadmap with nested items (read-only)."""
    class Meta:
        model = Roadmap
        fields = ['id', 'career_goal', 'details', 'created_at',]
        read_only_fields = ['id', 'career_goal', 'details', 'created_at']


class RoadmapCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Roadmap (write-only)."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    career_goal = serializers.CharField(max_length=255)

    class Meta:
        model = Roadmap
        fields = ['id', 'user', 'career_goal']
        read_only_fields = ['id']
