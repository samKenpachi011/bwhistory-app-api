"""
Url mapping for sites
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sites import views

app_name = 'sites'
router = DefaultRouter()
router.register(app_name, views.SiteViewSet,
                basename=app_name)

urlpatterns = [
    path('', include(router.urls)),
]
