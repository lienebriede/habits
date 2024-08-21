from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Habit

class HabitTests(APITestCase):

    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='tuser', password='tpass')
        self.client.login(username='tuser', password='tpass')
        self.habit_url = '/habits/'

    def test_create_habit(self):
        """
        Ensure creates a habit.
        """
        data = {
            'name': 'Running',
            'description': '',
            'frequency': 'Once a week',
        }
        response = self.client.post(self.habit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().name, 'Running')

    def test_get_habit_list(self):
        """
        Ensure retrieves a list of habits.
        """
        Habit.objects.create(owner=self.user, name='Read Book', description='Read 20 pages', frequency='Daily')
        response = self.client.get(self.habit_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Read Book')

    def test_update_habit(self):
        """
        Ensure updates an existing habit.
        """
        habit = Habit.objects.create(owner=self.user, name='Meditation', description='', frequency='4 times a week')
        update_data = {
            'name': 'Meditation',
            'description': 'Meditate every evening for 10 minutes',
            'frequency': 'Daily',
        }
        url = f'{self.habit_url}{habit.id}/'
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.description, 'Meditate every evening for 10 minutes')

    def test_delete_habit(self):
        """
        Ensure deletes a habit.
        """
        habit = Habit.objects.create(owner=self.user, name='Yoga', description='Yoga for 30 minutes', frequency='Daily')
        url = f'{self.habit_url}{habit.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_unauthenticated_user_cannot_create_habit(self):
        """
        Ensure unauthenticated users cannot create habits.
        """
        self.client.logout()
        data = {
            'name': 'Running',
            'description': 'Running every morning',
            'frequency': 'Daily',
        }
        response = self.client.post(self.habit_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)