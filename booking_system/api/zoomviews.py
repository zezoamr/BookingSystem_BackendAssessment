from rest_framework import generics, permissions
from api.zoom_utils import create_zoom_meeting, delete_zoom_meeting
from .models import ZoomMeeting
from .serializers import ZoomMeetingSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from .utils import send_zoom_meeting_creation, send_zoom_meeting_deletion, send_booking_cancellation
from api import serializers
from drf_yasg.utils import swagger_auto_schema


class ZoomMeetingListCreateView(generics.ListCreateAPIView):
    """
    Lists and creates Zoom meetings for authenticated users.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_fields = ['start_time', 'end_time']
    search_fields = ['topic']
    ordering_fields = ['start_time', 'end_time', 'created_at']

    @swagger_auto_schema(
        operation_description="Retrieves the list of Zoom meetings for the authenticated user.",
        responses={200: ZoomMeetingSerializer(many=True)},
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Creates a new Zoom meeting for the authenticated user.",
        request_body=ZoomMeetingSerializer,
        responses={201: ZoomMeetingSerializer()},
        security=[{'Bearer': []}]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        """
        Retrieves the Zoom meetings for the authenticated user.
        """
        if self.request.user.is_authenticated:
            return ZoomMeeting.objects.filter(user=self.request.user)
        else:
            return ZoomMeeting.objects.none()

    def perform_create(self, serializer):
        """
        Creates a Zoom meeting and sends a notification email to the user.
        """
        # Create the Zoom meeting
        zoom_response = create_zoom_meeting(
            topic=serializer.validated_data['topic'],
            start_time=serializer.validated_data['start_time'],
            end_time=serializer.validated_data['end_time']
        )
        # Check if the Zoom meeting was created successfully
        if zoom_response.get('id'):
            # Save the Zoom meeting to the database
            meeting = serializer.save(
                user=self.request.user,
                meeting_id=zoom_response['id']
            )
            # Send a notification email to the user
            send_zoom_meeting_creation(self.request.user.email, meeting)
        else:
            # Raise an error if the Zoom meeting creation failed
            raise serializers.ValidationError("Failed to create Zoom meeting")

class ZoomMeetingRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """
    Retrieve and destroy Zoom meetings for authenticated users.
    """
    serializer_class = ZoomMeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieves a specific Zoom meeting for the authenticated user.",
        responses={200: ZoomMeetingSerializer()},
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Deletes a specific Zoom meeting for the authenticated user.",
        responses={204: "No Content"},
        security=[{'Bearer': []}]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        """
        Retrieves the Zoom meetings for the authenticated user.
        """
        if self.request.user.is_authenticated:
            return ZoomMeeting.objects.filter(user=self.request.user)
        else:
            return ZoomMeeting.objects.none()

    def perform_destroy(self, instance):
        """
        Deletes the Zoom meeting and sends a notification email to the user.
        and sends cancellation emails to the booked users
        """
        zoom_response = delete_zoom_meeting(instance.meeting_id)
        if zoom_response.get('status') == 204:
            # Send a notification email to the user
            send_zoom_meeting_deletion(self.request.user.email, instance)
            # Send cancellation emails to the booked users
            booked_users = instance.bookings.all().select_related('user')
            for booking in booked_users:
                send_booking_cancellation(booking.user.email, instance)
                
            # Delete the Zoom meeting from the database
            instance.delete()
        else:
            # Raise an error if the Zoom meeting deletion failed
            raise serializers.ValidationError("Failed to delete Zoom meeting")