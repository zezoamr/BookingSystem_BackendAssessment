from django.db import models
from django.contrib.auth.models import User

class ZoomMeeting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zoom_meetings')
    meeting_id = models.CharField(max_length=255, unique=True)
    topic = models.CharField(max_length=255)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['user', 'end_time']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.topic} - {self.start_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    zoom_meeting = models.ForeignKey(ZoomMeeting, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'zoom_meeting')

    def __str__(self):
        return f"{self.user.username} - {self.zoom_meeting.topic}"