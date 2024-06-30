from rest_framework import generics, permissions
from api.models import Booking, ZoomMeeting
from .serializers import UserSerializer, BookingSerializer, ZoomMeetingSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from .utils import send_booking_confirmation, send_booking_cancellation
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone

class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    This view allows users to register by creating a new User instance.
    It uses the UserSerializer to validate and serialize the user data.
    The permission class is set to AllowAny, allowing anyone to access it.
    """
    queryset = User.objects.all()  
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=UserSerializer,
        responses={201: UserSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BookingListCreateView(generics.ListCreateAPIView):
    """
    View that lists and creates bookings for the authenticated user.
    GET: Lists all bookings for the authenticated user,
    filtered by `start_time`, `end_time`, and `user__username`.
    Can be ordered by `start_time`,`end_time`, and `created_at`.
    POST: Creates a new booking for the authenticated user and sends a booking confirmation email.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_fields = ['zoom_meeting__start_time', 'zoom_meeting__end_time']
    search_fields = ['user__username', 'zoom_meeting__topic']
    ordering_fields = ['zoom_meeting__start_time', 'zoom_meeting__end_time', 'created_at']

    @swagger_auto_schema(
        operation_description="List all bookings for the authenticated user.",
        responses={200: BookingSerializer(many=True)},
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new booking for the authenticated user.",
        request_body=BookingSerializer,
        responses={201: BookingSerializer()},
        security=[{'Bearer': []}]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns a queryset of bookings for the authenticated user.
        """
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        else:
            return Booking.objects.none()

    def perform_create(self, serializer):
        """
        Creates a new booking for the authenticated user and sends a booking confirmation email.
        """
        booking = serializer.save(user=self.request.user)
        send_booking_confirmation(self.request.user.email, booking)

class BookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View that retrieves, updates, and deletes bookings for the authenticated user.
    GET: Retrieves the booking with the given ID for the authenticated user.
    PUT: Updates the booking with the given ID for the authenticated user.
    DELETE: Deletes the booking with the given ID for the authenticated user and sends a cancellation email.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a specific booking for the authenticated user.",
        responses={200: BookingSerializer()},
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific booking for the authenticated user.",
        request_body=BookingSerializer,
        responses={200: BookingSerializer()},
        security=[{'Bearer': []}]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific booking for the authenticated user.",
        responses={204: "No Content"},
        security=[{'Bearer': []}]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns a queryset of the bookings for the authenticated user.
        """
        if self.request.user.is_authenticated:
            return Booking.objects.filter(user=self.request.user)
        else:
            return Booking.objects.none()
   
    def perform_destroy(self, instance):
        """
        Deletes the booking and sends a cancellation email to the user.
        """
        send_booking_cancellation(self.request.user.email, instance)
        instance.delete()

class AvailableSlotsView(generics.ListAPIView):
    serializer_class = ZoomMeetingSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="List available booking slots.",
        responses={200: ZoomMeetingSerializer(many=True)},
        security=[{'Bearer': []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # get all available meetings that have a date in the future and not belong to the authenticated user and the user hasn't booked them already
        return ZoomMeeting.objects.filter(start_time__gte=timezone.now()).exclude(bookings__user=self.request.user)