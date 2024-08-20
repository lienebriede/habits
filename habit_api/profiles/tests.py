from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from profiles.models import Profile


class ProfileCreationTests(APITestCase):
    def test_profile_creation_on_user_registration(self):
        """
        Ensure that a profile is created when a new user is registered.
        """
        user = User.objects.create_user(username='tuser', password='tpass')

        profile_exists = Profile.objects.filter(owner=user).exists()
        self.assertTrue(profile_exists)


class ProfileDetailTests(APITestCase):

    def setUp(self):
        # Create and authenticate user
        self.user = User.objects.create_user(username='tuser', password='tpass')
        self.client.login(username='tuser', password='tpass')
        self.profile_url = '/profile/'

    def test_get_profile_not_found(self):
        """
        Ensure that a 404 status code is returned when the profile does not exist.
        """
        Profile.objects.filter(owner=self.user).delete()
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Profile not found')

    def test_delete_profile(self):
        """
        Ensure that the profile is corectly deleted and resposnse is 204 status code.
        """
        response = self.client.delete('/profile/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(owner=self.user).exists())