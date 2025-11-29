"""
urls for the stages API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stages.views import StageAdminViewSet, StageListForUser

app_name = 'stages'

router = DefaultRouter()

router.register("admin", StageAdminViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("user/", StageListForUser.as_view(), name="stage-list-for-user"),
]
