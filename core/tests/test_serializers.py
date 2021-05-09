from rest_framework import status
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from .main import AppAPITestCase


User = get_user_model()


class MeetingTestCase(AppAPITestCase):
    valid_event_data = {
        "end": "2021-05-08T12:58:34Z",
        "start": "2021-05-08T12:58:33Z",
        "location": {
            "name": "First"
        },
        "event_name": "event",
        "meeting_agenda": "agenda",
        "participant_list": [
            "wp@wp.pl"
        ]
    }

    def test_user_can_create_events(self):

        url = reverse('calendar:token_obtain_pair')
        response = self.client.post(
            url, self.valid_event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['event_name'],
            self.valid_event_data['event_name'])


class LocationTestcase(AppAPITestCase):
    valid_location_data = {
        "name": "First Room",
        "address": "Gdansk"
    }

    def test_user_can_create_location(self):

        url = reverse('location:token_obtain_pair')
        response = self.client.post(
            url, {'username': 'user123',  'password': 'user123'}, format='json')
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=access)

        url = reverse('location')

        response = self.client.post(
            url, self.valid_location_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'],
                         self.valid_location_data['name'])


