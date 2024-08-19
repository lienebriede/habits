from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from profiles.models import Profile

class ProfileDetailTests(APITestCase):

    def setUp(self):
        # Create ans authenticate user
        self.user = User.objects.create_user(username='tuser', password='tpass')
        self.client.login(username='tuser', password='tpass')

    def test_get_profile_not_found(self):
        """
        Ensure that a 404 status code is returned when the profile does not exist.
        """
        Profile.objects.filter(owner=self.user).delete()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Profile not found')