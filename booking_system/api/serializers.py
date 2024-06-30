from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Booking, ZoomMeeting

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ZoomMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeeting
        fields = ['id', 'user', 'meeting_id', 'topic', 'start_time', 'end_time', 'created_at']
        read_only_fields = ['user', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    zoom_meeting = ZoomMeetingSerializer(read_only=True)
    zoom_meeting_id = serializers.PrimaryKeyRelatedField(
        queryset=ZoomMeeting.objects.all(),
        source='zoom_meeting',
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'user', 'zoom_meeting', 'zoom_meeting_id', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        # Check if the user has already booked this meeting
        user = self.context['request'].user
        zoom_meeting = data['zoom_meeting']
        if Booking.objects.filter(user=user, zoom_meeting=zoom_meeting).exists():
            raise serializers.ValidationError("You have already booked this meeting.")
        return data