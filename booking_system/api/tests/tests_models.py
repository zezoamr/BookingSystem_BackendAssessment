from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.test import TestCase
from api.models import ZoomMeeting, Booking

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.zoom_meeting = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='123456789',
            topic='Test Meeting',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )

    def test_zoom_meeting_creation(self):
        self.assertTrue(isinstance(self.zoom_meeting, ZoomMeeting))
        expected_str = f"{self.user.username} - Test Meeting - {self.zoom_meeting.start_time}"
        self.assertEqual(str(self.zoom_meeting), expected_str)

    def test_booking_creation(self):
        booking = Booking.objects.create(user=self.user, zoom_meeting=self.zoom_meeting)
        self.assertTrue(isinstance(booking, Booking))
        self.assertEqual(booking.__str__(), f"{self.user.username} - Test Meeting")

    def test_user_zoom_meetings(self):
        self.assertEqual(self.user.zoom_meetings.count(), 1)

    def test_user_bookings(self):
        Booking.objects.create(user=self.user, zoom_meeting=self.zoom_meeting)
        self.assertEqual(self.user.bookings.count(), 1)


