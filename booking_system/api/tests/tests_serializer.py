from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from api.models import ZoomMeeting, Booking
from api.serializers import UserSerializer, ZoomMeetingSerializer, BookingSerializer

class SerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.zoom_meeting = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='123456789',
            topic='Test Meeting',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(set(serializer.data.keys()), set(['id', 'username', 'email']))

    def test_zoom_meeting_serializer(self):
        serializer = ZoomMeetingSerializer(instance=self.zoom_meeting)
        self.assertEqual(set(serializer.data.keys()), set(['id', 'user', 'meeting_id', 'topic', 'start_time', 'end_time', 'created_at']))

    def test_booking_serializer(self):
        booking = Booking.objects.create(user=self.user, zoom_meeting=self.zoom_meeting)
        serializer = BookingSerializer(instance=booking)
        self.assertEqual(set(serializer.data.keys()), set(['id', 'user', 'zoom_meeting', 'created_at']))
