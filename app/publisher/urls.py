"""
URL mappings for the publisher app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from publisher import views

app_name = 'publisher'

router = DefaultRouter()
router.register(app_name, views.PublisherViewSet,
                basename=app_name)

urlpatterns = [
    path('', include(router.urls))
]
