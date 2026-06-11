from django.db import IntegrityError, transaction

from apps.bookings.exceptions import SlotAlreadyBooked
from apps.bookings.models import Booking, Slot


@transaction.atomic
def create_booking(*, user, slot_id):
    slot = Slot.objects.select_for_update().filter(id=slot_id).first()
    if slot is None:
        return None

    if Booking.objects.filter(slot=slot).exists():
        raise SlotAlreadyBooked()

    try:
        return Booking.objects.create(user=user, slot=slot)
    except IntegrityError as exc:
        raise SlotAlreadyBooked() from exc

