from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import HabitStacking

class HabitStackingTests(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # Create habit stacks for user1
        HabitStacking.objects.create(
            user=self.user1,
            habit1='Exercise',
            habit2='Meditation',
            goal='DAILY'
        )
        HabitStacking.objects.create(
            user=self.user1,
            habit1='Reading',
            habit2='Writing',
            goal='NO_GOAL'
        )
        
        # Create a habit stack for user2
        HabitStacking.objects.create(
            user=self.user2,
            habit1='Running',
            habit2='Cycling',
            goal='DAILY'
        )
        
        # Define the URLs
        self.list_create_url = reverse('habit-stacking-list-create')
        self.detail_url = reverse('habit-stacking-detail', kwargs={'pk': 1})

    def authenticate_user(self, user):
        self.client.login(username=user.username, password='password123')

    def test_list_habit_stacking_authenticated(self):
        self.authenticate_user(self.user1)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_habit_stacking_unauthenticated(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_stacking(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Swimming',
            'habit2': 'Jogging',
            'goal': 'DAILY'
        }
     
        initial_count = HabitStacking.objects.count()
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_count = HabitStacking.objects.count()
       
        # Verify the count
        self.assertEqual(final_count, initial_count + 1)
        self.assertEqual(HabitStacking.objects.get(id=response.data['id']).habit1, 'Swimming')

    def test_update_habit_stacking(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Updated Exercise',
            'habit2': 'Updated Meditation'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit_stack = HabitStacking.objects.get(id=1)
        self.assertEqual(habit_stack.habit1, 'Updated Exercise')

    def test_delete_habit_stacking(self):
        self.authenticate_user(self.user1)
        detail_url = reverse('habit-stacking-detail', kwargs={'pk': 1})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HabitStacking.objects.count(), 2)

    def test_cannot_access_other_users_habits(self):
        self.authenticate_user(self.user2)
        response = self.client.get(reverse('habit-stacking-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)