"""
StarPhase Serializers
"""
from rest_framework import serializers
from core.models import StarPhase


class StarPhaseSerializer(serializers.ModelSerializer):
    """
    Serializer for StarPhase model
    """
    class Meta:
        model = StarPhase
        fields = [
            'id', 'name', 'description', 'order',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
