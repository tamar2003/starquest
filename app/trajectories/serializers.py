"""
Trajectories Serializer
"""
from rest_framework import serializers
from core.models import Trajectories


class TrajectoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trajectories
        fields = ['id', 'name', 'description', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
