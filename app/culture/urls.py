"""
URL mappings for the culture app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from culture import views

app_name = 'culture'

router = DefaultRouter()
router.register('culture', views.CultureViewSet,
                basename='culture')
router.register('tags', views.TagsViewSet,)

urlpatterns = [
    path('', include(router.urls))
]
