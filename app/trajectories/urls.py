"""
urls for the trajectories API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trajectories.views import TrajectoriesListForUser, TrajectoriesAdminViewSet

app_name = 'trajectories'

router = DefaultRouter()

router.register("admin", TrajectoriesAdminViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("user/", TrajectoriesListForUser.as_view(), name="trajectories-list-for-user"),
]
