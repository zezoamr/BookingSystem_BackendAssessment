from zoomus import ZoomClient
from django.conf import settings

client = ZoomClient(settings.ZOOM_API_KEY, settings.ZOOM_API_SECRET, settings.ZOOM_API_ACCOUNT_ID)

def create_zoom_meeting(topic, start_time, duration):
    response = client.meeting.create(
        user_id='me',
        topic=topic,
        type=2,  # Scheduled meeting
        start_time=start_time,
        duration=duration,
        timezone='UTC'
    )
    return response

def delete_zoom_meeting(meeting_id):
    response = client.meeting.delete(id=meeting_id)
    return response

def get_zoom_meeting(meeting_id):
    response = client.meeting.get(id=meeting_id)
    return response