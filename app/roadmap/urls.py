"""
urls for the roadmap API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from roadmap.views import RoadmapViewSet

app_name = 'roadmap'

router = DefaultRouter()

router.register('', RoadmapViewSet, basename='roadmap')

urlpatterns = [
    path('', include(router.urls)),
]
