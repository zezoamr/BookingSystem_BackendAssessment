from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .bookingviews import (
    RegisterView, BookingListCreateView, BookingRetrieveUpdateDestroyView,
    AvailableSlotsView
)
from .zoomviews import (
    ZoomMeetingListCreateView, ZoomMeetingRetrieveDestroyView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('slots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
    path('bookings/<int:pk>/', BookingRetrieveUpdateDestroyView.as_view(), name='booking_detail'),
    path('zoom/meetings/', ZoomMeetingListCreateView.as_view(), name='zoom_meeting_list_create'),
    path('zoom/meetings/<int:pk>/', ZoomMeetingRetrieveDestroyView.as_view(), name='zoom_meeting_detail'),
]