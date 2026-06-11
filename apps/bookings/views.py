from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bookings.models import Booking, Slot
from apps.bookings.serializers import (
    BookingSerializer,
    CreateBookingSerializer,
    SlotQuerySerializer,
    SlotSerializer,
)
from apps.bookings.services import create_booking
from apps.users.models import User
from apps.venues.models import Venue


USER_HEADER = OpenApiParameter(
    name="X-User-Id",
    type=int,
    location=OpenApiParameter.HEADER,
    required=True,
    description="ID of the selected demo user.",
)


def get_request_user(request):
    raw_user_id = request.headers.get("X-User-Id")
    if not raw_user_id:
        raise ValidationError({"X-User-Id": "This header is required."})

    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError) as exc:
        raise ValidationError({"X-User-Id": "Enter a valid integer user ID."}) from exc

    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist as exc:
        raise NotFound("User not found.") from exc


class VenueSlotListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="date",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Slot date in YYYY-MM-DD format.",
            )
        ],
        responses=SlotSerializer(many=True),
    )
    def get(self, request, venue_id):
        venue = get_object_or_404(Venue, id=venue_id, is_active=True)
        query = SlotQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)

        slots = (
            Slot.objects.filter(venue=venue, date=query.validated_data["date"])
            .select_related("booking")
            .order_by("start_time")
        )
        return Response(SlotSerializer(slots, many=True).data)


class BookingListCreateView(APIView):
    @extend_schema(
        parameters=[USER_HEADER],
        request=CreateBookingSerializer,
        responses={201: BookingSerializer},
    )
    def post(self, request):
        user = get_request_user(request)
        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = create_booking(
            user=user,
            slot_id=serializer.validated_data["slot_id"],
        )
        if booking is None:
            raise NotFound("Slot not found.")

        booking = Booking.objects.select_related("user", "slot__venue").get(id=booking.id)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class UserBookingListView(APIView):
    @extend_schema(parameters=[USER_HEADER], responses=BookingSerializer(many=True))
    def get(self, request, user_id):
        user = get_request_user(request)
        if user.id != user_id:
            raise PermissionDenied("You can only view your own bookings.")

        bookings = Booking.objects.filter(user=user).select_related("user", "slot__venue")
        return Response(BookingSerializer(bookings, many=True).data)


class BookingDetailView(APIView):
    @extend_schema(parameters=[USER_HEADER], responses={204: None})
    def delete(self, request, booking_id):
        user = get_request_user(request)
        booking = get_object_or_404(Booking, id=booking_id)
        if booking.user_id != user.id:
            raise PermissionDenied("You can only cancel your own bookings.")

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

