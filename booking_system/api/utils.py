from django.core.mail import send_mail
from django.conf import settings

def send_booking_confirmation(user_email, booking):
    subject = 'Booking Confirmation'
    message = f'Your booking for {booking.zoom_meeting.topic} from {booking.zoom_meeting.start_time} to {booking.zoom_meeting.end_time} has been confirmed.'
    send_mail(subject, message, 'from@example.com', [user_email])

def send_booking_cancellation(user_email, booking):
    subject = 'Booking Cancellation'
    message = f'Your booking for {booking.zoom_meeting.topic} from {booking.zoom_meeting.start_time} to {booking.zoom_meeting.end_time} has been cancelled.'
    send_mail(subject, message, 'from@example.com', [user_email])

def send_zoom_meeting_creation(user_email, meeting):
    subject = 'Zoom Meeting Created'
    message = f'Your Zoom meeting "{meeting.topic}" has been created for {meeting.start_time}.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

def send_zoom_meeting_deletion(user_email, meeting):
    subject = 'Zoom Meeting Deleted'
    message = f'Your Zoom meeting "{meeting.topic}" scheduled for {meeting.start_time} has been deleted.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])