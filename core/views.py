from .models import Meeting, Location
from .serializers import MeetingSerializer, LocationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated


class DayFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        day = request.query_params.get('day')
        if day:
            day = queryset.filter(start__date=day)
            return day
        return queryset


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend, DayFilter)
    search_fields = ['event_name', 'meeting_agenda']
    permission_classes = (IsAuthenticated,)

    filter_fields = {'start': ['icontains']}
    filterset_fields = {
        'id',
        'location',
    }

    def get_queryset(self):
        # Filtering users from the same company
        meeting = Meeting.objects.filter(
            owner__company_id=self.request.user.company)
        # Filtering currently logged user in participant_list
        participants = meeting.filter(
            participant_list__id=self.request.user.id)
        # Filtering currently logged user in Meeting.location.manager
        manager = meeting.filter(
            location__manager=self.request.user)

        return participants | manager


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Filtering users from the same company
        location = Location.objects.filter(
            manager__company_id=self.request.user.company)

        return location
