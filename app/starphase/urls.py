"""
urls for the starphase API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from starphase.views import StarPhaseAdminViewSet, StarPhaseListForUser

app_name = 'starphase'

router = DefaultRouter()

router.register("admin", StarPhaseAdminViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("user/", StarPhaseListForUser.as_view(),
         name="starphase-list-for-user"),
]
