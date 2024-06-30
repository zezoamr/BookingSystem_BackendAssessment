from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import ZoomMeeting, Booking
from django.utils import timezone
from datetime import timedelta

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_user_invalid_data(self):
        data = {
            'username': 'testuser',
            'email': 'invalid_email',
            'password': 'short'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BookingListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.zoom_meeting = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='123456789',
            topic='Test Meeting',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )
        self.booking_list_create_url = reverse('booking_list_create')

    def test_list_bookings(self):
        Booking.objects.create(user=self.user, zoom_meeting=self.zoom_meeting)
        response = self.client.get(self.booking_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        self.client.force_authenticate(user=self.user)
        data = {'zoom_meeting_id': self.zoom_meeting.id}
        response = self.client.post(self.booking_list_create_url, data)
        #print(f"Create Booking Response: {response.status_code}")
        #print(f"Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_create_booking_invalid_data(self):
        data = {'zoom_meeting': 9999}  # Non-existent meeting ID
        response = self.client.post(self.booking_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BookingRetrieveUpdateDestroyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.zoom_meeting = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='123456789',
            topic='Test Meeting',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )
        self.booking = Booking.objects.create(user=self.user, zoom_meeting=self.zoom_meeting)
        self.booking_detail_url = reverse('booking_detail', kwargs={'pk': self.booking.id})

    def test_retrieve_booking(self):
        response = self.client.get(self.booking_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.booking.id)

    def test_update_booking(self):
        self.client.force_authenticate(user=self.user)
        new_zoom_meeting = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='987654321',
            topic='New Test Meeting',
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=2, hours=1)
        )
        data = {'zoom_meeting_id': new_zoom_meeting.id}
        response = self.client.put(self.booking_detail_url, data)
        #print(f"Update Booking Response: {response.status_code}")
        #print(f"Response Data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.zoom_meeting, new_zoom_meeting)


    def test_delete_booking(self):
        response = self.client.delete(self.booking_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)

class AvailableSlotsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.zoom_meeting1 = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='123456789',
            topic='Test Meeting 1',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )
        self.zoom_meeting2 = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='987654321',
            topic='Test Meeting 2',
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=2, hours=1)
        )
        self.available_slots_url = reverse('available_slots')

    def test_list_available_slots(self):
        response = self.client.get(self.available_slots_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_booked_slot_not_listed(self):
        Booking.objects.create(user=self.user, zoom_meeting=self.zoom_meeting1)
        response = self.client.get(self.available_slots_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.zoom_meeting2.id)

    def test_past_meetings_not_listed(self):
        past_meeting = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='111222333',
            topic='Past Meeting',
            start_time=timezone.now() - timedelta(days=1),
            end_time=timezone.now() - timedelta(hours=23)
        )
        response = self.client.get(self.available_slots_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertNotIn(past_meeting.id, [meeting['id'] for meeting in response.data])

    def test_unauthenticated_user_can_access(self):
        response = self.client.get(self.available_slots_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)