"""
URL mappings for the event app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from event import views

app_name = 'event'

router = DefaultRouter()
router.register(app_name, views.EventViewSet,
                basename=app_name)

urlpatterns = [
    path('', include(router.urls))
]
