from django.urls import path, include
from rest_framework.routers import DefaultRouter

from logbook import views

router = DefaultRouter()
router.register('wonders', views.WonderViewSet)

app_name = 'logbook'

urlpatterns = [
    path('', include(router.urls))
]
