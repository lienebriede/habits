from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import HabitStacking, HabitStackingLog, Weekday

class HabitStackingTests(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # Create weekdays for goal-specific tests
        self.monday = Weekday.objects.create(name='Monday')
        self.tuesday = Weekday.objects.create(name='Tuesday')
        
        # Create habit stacks for user1
        self.habit_stack1 = HabitStacking.objects.create(
            user=self.user1,
            habit1='Exercise',
            habit2='Meditation',
            goal='DAILY'
        )
        self.habit_stack2 = HabitStacking.objects.create(
            user=self.user1,
            habit1='Reading',
            habit2='Writing',
            goal='NO_GOAL'
        )
        
        # Create a habit stack for user2
        self.habit_stack3 = HabitStacking.objects.create(
            user=self.user2,
            habit1='Running',
            habit2='Cycling',
            goal='DAILY'
        )
        
        # Define the URLs
        self.habit_stack_list_create_url = reverse('habit-stacking-list-create')
        self.habit_stack_detail_url = reverse('habit-stacking-detail', kwargs={'pk': self.habit_stack1.id})
        self.habit_stack_log_list_create_url = reverse('habit-stacking-log-list-create')
    
    def authenticate_user(self, user):
        self.client.login(username=user.username, password='password123')

    # Tests for HabitStacking
    def test_list_habit_stacking_authenticated(self):
        self.authenticate_user(self.user1)
        response = self.client.get(self.habit_stack_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_habit_stacking_unauthenticated(self):
        response = self.client.get(self.habit_stack_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_habit_stacking(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Swimming',
            'habit2': 'Jogging',
            'goal': 'DAILY'
        }
        initial_count = HabitStacking.objects.count()
        response = self.client.post(self.habit_stack_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_count = HabitStacking.objects.count()
        self.assertEqual(final_count, initial_count + 1)
        self.assertEqual(HabitStacking.objects.get(id=response.data['id']).habit1, 'Swimming')

    def test_update_habit_stacking(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Updated Exercise',
            'habit2': 'Updated Meditation',
            'goal': 'DAILY',
        }
        response = self.client.put(self.habit_stack_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit_stack = HabitStacking.objects.get(id=self.habit_stack1.id)
        self.assertEqual(habit_stack.habit1, 'Updated Exercise')

    def test_delete_habit_stacking(self):
        self.authenticate_user(self.user1)
        detail_url = reverse('habit-stacking-detail', kwargs={'pk': self.habit_stack1.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HabitStacking.objects.count(), 2)

    def test_cannot_access_other_users_habits(self):
        self.authenticate_user(self.user2)
        response = self.client.get(reverse('habit-stacking-detail', kwargs={'pk': self.habit_stack1.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_duplicate_habit_stacking(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Exercise',
            'habit2': 'Meditation',
            'goal': 'DAILY'
        }
        response = self.client.post(self.habit_stack_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A habit stack with these details already exists.", response.data['non_field_errors'])

    # Tests for HabitStacking with Goals
    def test_create_habit_stacking_with_daily_goal(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Exercise',
            'habit2': 'Read',
            'goal': 'DAILY',
            'specific_days': []
        }
        response = self.client.post(self.habit_stack_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit_stack = HabitStacking.objects.get(id=response.data['id'])
        self.assertEqual(habit_stack.goal, 'DAILY')
        self.assertEqual(habit_stack.specific_days.count(), 0)

    def test_create_habit_stacking_with_specific_days_goal(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Exercise',
            'habit2': 'Read',
            'goal': 'SPECIFIC_DAYS',
            'specific_days': [self.monday.id, self.tuesday.id]
        }
        response = self.client.post(self.habit_stack_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit_stack = HabitStacking.objects.get(id=response.data['id'])
        self.assertEqual(habit_stack.goal, 'SPECIFIC_DAYS')
        self.assertEqual(habit_stack.specific_days.count(), 2)

    def test_create_habit_stacking_with_no_goal(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Exercise',
            'habit2': 'Read',
            'goal': 'NO_GOAL',
            'specific_days': []
        }
        response = self.client.post(self.habit_stack_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit_stack = HabitStacking.objects.get(id=response.data['id'])
        self.assertEqual(habit_stack.goal, 'NO_GOAL')
        self.assertEqual(habit_stack.specific_days.count(), 0)

    def test_create_habit_stacking_with_no_goal_and_specific_days(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Exercise',
            'habit2': 'Read',
            'goal': 'NO_GOAL',
            'specific_days': [self.monday.id, self.tuesday.id]
        }
        response = self.client.post(self.habit_stack_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Specific days should not be provided when the goal is 'DAILY' or 'NO_GOAL'", str(response.data))

    def test_create_habit_stacking_with_daily_goal_and_specific_days(self):
        self.authenticate_user(self.user1)
        data = {
            'habit1': 'Exercise',
            'habit2': 'Read',
            'goal': 'DAILY',
            'specific_days': [self.monday.id]
        }
        response = self.client.post(self.habit_stack_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Specific days should not be provided when the goal is 'DAILY'", str(response.data))

    # Tests for HabitStackingLog
    def test_create_habit_stack_log(self):
        self.authenticate_user(self.user1)
        data = {
            'habit_stack': self.habit_stack1.id,
            'date': '2024-08-25',
            'completed': True
        }
        initial_count = HabitStackingLog.objects.count()
        response = self.client.post(self.habit_stack_log_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_count = HabitStackingLog.objects.count()
        self.assertEqual(final_count, initial_count + 1)
        self.assertTrue(HabitStackingLog.objects.get().completed)

    def test_create_habit_stack_log_invalid_user(self):
        self.authenticate_user(self.user2)
        data = {
            'habit_stack': self.habit_stack1.id,
            'date': '2024-08-25',
            'completed': True
        }
        response = self.client.post(self.habit_stack_log_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot log habits that don't belong to you.", response.data['non_field_errors'])

    def test_create_habit_stack_log_no_goal(self):
        self.authenticate_user(self.user1)
        data = {
            'habit_stack': self.habit_stack2.id,
            'date': '2024-08-25',
            'completed': True
        }
        response = self.client.post(self.habit_stack_log_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HabitStackingLog.objects.get().completed)

    def test_create_habit_stack_log_duplicate(self):
        self.authenticate_user(self.user1)
        data = {
            'habit_stack': self.habit_stack1.id,
            'date': '2024-08-25',
            'completed': True
        }

        self.client.post(self.habit_stack_log_list_create_url, data, format='json')
        response = self.client.post(self.habit_stack_log_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Log entry already exists", str(response.data))

    def test_get_habit_stack_logs(self):
        HabitStackingLog.objects.create(
            habit_stack=self.habit_stack1,
            user=self.user1,
            date='2024-08-25',
            completed=True
        )
        self.authenticate_user(self.user1)
        response = self.client.get(self.habit_stack_log_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_habit_stack_logs_other_user(self):
        self.authenticate_user(self.user2)
        HabitStackingLog.objects.create(
            habit_stack=self.habit_stack3,
            user=self.user2,
            date='2024-08-25',
            completed=True
        )
        response = self.client.get(self.habit_stack_log_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)