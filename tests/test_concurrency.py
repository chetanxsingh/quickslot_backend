from concurrent.futures import ThreadPoolExecutor
from datetime import date, time
from threading import Barrier

import pytest
from django.db import close_old_connections, connection, connections

from apps.bookings.exceptions import SlotAlreadyBooked
from apps.bookings.models import Booking, Slot
from apps.bookings.services import create_booking
from apps.users.models import User
from apps.venues.models import Venue


@pytest.mark.django_db(transaction=True)
def test_two_simultaneous_bookings_create_exactly_one_booking():
    if connection.vendor != "postgresql":
        pytest.skip("Row-lock concurrency behavior requires PostgreSQL.")

    first_user = User.objects.create_user(username="first")
    second_user = User.objects.create_user(username="second")
    venue = Venue.objects.create(
        name="Concurrency Arena",
        sport_type=Venue.SportType.BADMINTON,
        address="1 Locking Lane",
        city="Indore",
    )
    slot = Slot.objects.create(
        venue=venue,
        date=date(2026, 7, 1),
        start_time=time(6),
        end_time=time(7),
    )
    barrier = Barrier(2)

    def attempt_booking(user_id):
        close_old_connections()
        try:
            user = User.objects.get(id=user_id)
            barrier.wait(timeout=5)
            create_booking(user=user, slot_id=slot.id)
            return "created"
        except SlotAlreadyBooked:
            return "conflict"
        finally:
            connections.close_all()

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(
            executor.map(
                attempt_booking,
                (first_user.id, second_user.id),
            )
        )

    assert sorted(outcomes) == ["conflict", "created"]
    assert Booking.objects.filter(slot=slot).count() == 1
