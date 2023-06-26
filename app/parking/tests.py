from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from parking.models import Parking

PARKING_ENDPOINT = '/api/tickets/'


def create_parking(**params):
    """ Create and return a sample parking """
    defaults = {
        'name' : 'Test Parking',
        'address' : 'Test Parking',
        'latitude' : '36.108920',
        'longitude' : '-81.899730',
        'capacity' : 30,
    }
    defaults.update(params)
    return Parking.objects.create(**defaults)


def create_user(**params):
    """ Create and return a sample user """
    password = params.pop('password')
    user = get_user_model().objects.create(
        first_name='Test',
        last_name='Name',
        **params,
    )
    user.set_password(password)
    user.save()
    return user


class UnauthorizedAdminEventApiTest(TestCase):
    """ Test Admin Event API is accessible to unauthorized user """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='admin@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)


class ParkingApiTest(TestCase):
    """ Test Parking Event API is available """
    """ NOTE: Uncomment the following code to test authenticated user  """
    def setUp(self):
        self.client = APIClient()
        # self.user = create_user(email='admin@example.com', password='testpass')
        # self.client.force_authenticate(user=self.user)

    # def test_unauthorized_user(self):
    #     """ Test unauthenticated request """
    #     self.client.logout()
    #     response = self.client.get(PARKING_ENDPOINT)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_auth_required(self):
    #     """ Test unauthenticated request """
    #     self.client.logout()
    #     response = self.client.get(PARKING_ENDPOINT)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)