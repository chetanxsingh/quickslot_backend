from rest_framework import serializers

from apps.bookings.models import Booking, Slot
from apps.users.serializers import UserSerializer
from apps.venues.serializers import VenueSerializer


class SlotSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ("id", "date", "start_time", "end_time", "status")

    def get_status(self, obj) -> str:
        return "booked" if obj.is_booked else "available"


class BookingSlotSerializer(serializers.ModelSerializer):
    venue = VenueSerializer(read_only=True)

    class Meta:
        model = Slot
        fields = ("id", "date", "start_time", "end_time", "venue")


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    slot = BookingSlotSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "user", "slot", "created_at")


class CreateBookingSerializer(serializers.Serializer):
    slot_id = serializers.IntegerField(min_value=1)


class SlotQuerySerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
