from .views import MeetingViewSet, LocationViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('calendar', MeetingViewSet)
router.register('location', LocationViewSet)

