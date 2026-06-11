from django.urls import path

from apps.bookings.views import (
    BookingDetailView,
    BookingListCreateView,
    UserBookingListView,
    VenueSlotListView,
)


urlpatterns = [
    path(
        "venues/<int:venue_id>/slots/",
        VenueSlotListView.as_view(),
        name="venue-slot-list",
    ),
    path("bookings/", BookingListCreateView.as_view(), name="booking-create"),
    path(
        "users/<int:user_id>/bookings/",
        UserBookingListView.as_view(),
        name="user-booking-list",
    ),
    path(
        "bookings/<int:booking_id>/",
        BookingDetailView.as_view(),
        name="booking-detail",
    ),
]

