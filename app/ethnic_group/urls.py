"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from ethnic_group import views
from rest_framework.routers import DefaultRouter

app_name = 'ethnic_group'

router = DefaultRouter()
router.register(r'ethnic_groups', views.EthnicGroupViewSet,
                basename='ethnic_group')

urlpatterns = [
    path('', include(router.urls)),
]
