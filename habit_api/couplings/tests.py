from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from habits.models import Habit
from couplings.models import Coupling

class CouplingTests(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Create two habits for user1
        self.habit1 = Habit.objects.create(owner=self.user1, name='Habit 1', frequency='Daily')
        self.habit2 = Habit.objects.create(owner=self.user1, name='Habit 2', frequency='Weekly')

        # Create habit for user2
        self.habit3 = Habit.objects.create(owner=self.user2, name='Habit 3', frequency='Monthly')
        
        # Create a coupling for user1
        self.coupling = Coupling.objects.create(owner=self.user1, habit1=self.habit1, habit2=self.habit2)

        # URLs for coupling operations
        self.coupling_list_url = '/couplings/'
        self.coupling_detail_url = f'/couplings/{self.coupling.id}/'

    def test_create_coupling(self):
        """
        Ensure that an authenticated user can create a coupling.
        """
        self.client.login(username='user1', password='password1')
        new_habit = Habit.objects.create(owner=self.user1, name='Meditate', frequency='Daily')
        data = {
            'habit1': self.habit1.id,
            'habit2': new_habit.id
        }
        response = self.client.post(self.coupling_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Coupling.objects.count(), 2)

    def test_cannot_create_coupling_unauthenticated(self):
        """
        Ensure that unauthenticated users cannot create a coupling.
        """
        data = {
            'habit1': self.habit1.id,
            'habit2': self.habit2.id
        }
        response = self.client.post(self.coupling_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_coupling_list(self):
        """
        Ensure that an authenticated user can retrieve a list of their couplings.
        """
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.coupling_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['habit1'], self.habit1.id)
        self.assertEqual(response.data[0]['habit2'], self.habit2.id)

    def test_get_coupling_detail(self):
        """
        Ensure that an authenticated user can retrieve a specific coupling.
        """
        self.client.login(username='user1', password='password1')
        response = self.client.get(self.coupling_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['habit1'], self.habit1.id)
        self.assertEqual(response.data['habit2'], self.habit2.id)

    def test_update_coupling(self):
        """
        Ensure that an authenticated user can update a coupling they own.
        """
        self.client.login(username='user1', password='password1')
        new_habit = Habit.objects.create(owner=self.user1, name='New Habit', frequency='Monthly')
        data = {
            'habit1': new_habit.id,
            'habit2': self.habit2.id
        }
        response = self.client.put(self.coupling_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.coupling.refresh_from_db()
        self.assertEqual(self.coupling.habit1.id, new_habit.id)

    def test_delete_coupling(self):
        """
        Ensure that an authenticated user can delete a coupling they own.
        """
        self.client.login(username='user1', password='password1')
        response = self.client.delete(self.coupling_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Coupling.objects.count(), 0)

    def test_cannot_modify_others_coupling(self):
        """
        Ensure that users cannot modify couplings owned by others.
        """
        # Log in as user2
        self.client.logout()
        self.client.login(username='user2', password='password2')

        # Attempt to update the coupling owned by user1 (self.coupling)
        update_data = {
            'habit1': self.habit1.id,
            'habit2': self.habit3.id
        }
        
        url = self.coupling_detail_url
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.coupling.refresh_from_db()
        self.assertEqual(self.coupling.habit1, self.habit1)
        self.assertEqual(self.coupling.habit2, self.habit2)

    def test_cannot_delete_others_coupling(self):
        """
        Ensure that users cannot delete couplings owned by others.
        """
        self.client.logout()
        self.client.login(username='user2', password='password2')

        # Create a coupling with user2
        user2_coupling = Coupling.objects.create(owner=self.user2, habit1=self.habit1, habit2=self.habit2)

        # Attempt to delete the coupling owned by user1
        url = f'{self.coupling_list_url}{self.coupling.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
