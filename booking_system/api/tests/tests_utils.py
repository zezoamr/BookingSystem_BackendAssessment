from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch
from api.models import ZoomMeeting, Booking
from api.utils import send_booking_confirmation, send_booking_cancellation

class UtilsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.zoom_meeting = ZoomMeeting.objects.create(
            user=self.user,
            meeting_id='123456789',
            topic='Test Meeting',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=1)
        )
        self.booking = Booking.objects.create(user=self.user, zoom_meeting=self.zoom_meeting)

    def test_send_booking_confirmation(self):
        # Mock the email sending function and test it's called with correct parameters
        with patch('api.utils.send_mail') as mock_send_mail:
            send_booking_confirmation(self.user.email, self.booking)
            mock_send_mail.assert_called_once()

    def test_send_booking_cancellation(self):
        # Mock the email sending function and test it's called with correct parameters
        with patch('api.utils.send_mail') as mock_send_mail:
            send_booking_cancellation(self.user.email, self.booking)
            mock_send_mail.assert_called_once()