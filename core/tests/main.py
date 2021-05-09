from rest_framework.test import APITestCase
from django.apps import apps
from django.shortcuts import reverse

Company = apps.get_model('core', 'Company')
Meeting = apps.get_model('core', 'Meeting')
User = apps.get_model('core', 'User')
Location = apps.get_model('core', 'Location')


class AppAPITestCase(APITestCase):
    @classmethod
    def setUpClass(cls):

        company = Company.objects.create(name='Company')
        user = User.objects.create_user(
            username='user123', email='wp@wp.pl', password='user123', company=company)

        user.save()

    def setUp(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(
            url, {'username': 'user123',  'password': 'user123'}, format='json')
        access = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=access)

    def tearDown(self):
        self.client.credentials()

