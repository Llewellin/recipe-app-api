from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Wonder
from logbook.serializers import WonderSerializer

WONDER_URL = reverse('logbook:wonder-list')


class PublicWonderApiTests(TestCase):
    """Test Wonder API for public users"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving wonders"""
        res = self.client.get(WONDER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWonderApiTests(TestCase):
    """Test Wonder API for authorized users"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test123@gmail.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_wonders(self):
        """Test retrieve wonders"""
        Wonder.objects.create(
            user=self.user,
            name='gray whale',
            category='animal'
        )
        Wonder.objects.create(
            user=self.user,
            name='akitsushima',
            category='wreck'
        )

        res = self.client.get(WONDER_URL)
        wonders = Wonder.objects.all().order_by('-name')
        serializer = WonderSerializer(wonders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_wonders_to_limited_user(self):
        """Test Retrieve Wonders To Limited User"""
        user2 = get_user_model().objects.create_user(
            'test456@gmail.com',
            'password456'
        )
        wonder = Wonder.objects.create(
            user=self.user,
            name='sperm whale',
            category='animal'
        )
        Wonder.objects.create(
            user=user2,
            name='turtle',
            category='animal'
        )

        res = self.client.get(WONDER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        # res.data[0].name doesn't work
        self.assertEqual(res.data[0]['name'], wonder.name)

    def test_create_wonder_successful(self):
        """Test create wonder successful"""
        payload = {
            'name': 'eel',
            'category': 'animal'
        }
        res = self.client.post(WONDER_URL, payload)

        wonder = Wonder.objects.filter(
            user=self.user,
            name=payload['name']
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(wonder.exists())

    def test_create_wonder_failed(self):
        """Test create wonder failed"""
        payload = {
            'name': ''
        }
        res = self.client.post(WONDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
