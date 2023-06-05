"""
URL mappings for the chief app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chief import views

app_name = 'chief'

router = DefaultRouter()
router.register(app_name, views.ChiefViewSet,
                basename=app_name)

urlpatterns = [
    path('', include(router.urls))
]
