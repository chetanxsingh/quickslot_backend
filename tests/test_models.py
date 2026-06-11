from datetime import date, time

import pytest
from django.db import IntegrityError, transaction

from apps.bookings.models import Booking, Slot
from apps.users.models import User
from apps.venues.models import Venue


@pytest.fixture
def venue():
    return Venue.objects.create(
        name="Test Arena",
        sport_type=Venue.SportType.BADMINTON,
        address="1 Test Street",
        city="Indore",
    )


@pytest.fixture
def slot(venue):
    return Slot.objects.create(
        venue=venue,
        date=date(2026, 7, 1),
        start_time=time(6),
        end_time=time(7),
    )


@pytest.mark.django_db
def test_user_display_name_prefers_full_name():
    user = User(username="aisha", first_name="Aisha", last_name="Khan")

    assert user.display_name == "Aisha Khan"


@pytest.mark.django_db
def test_slot_start_is_unique_per_venue_and_date(slot):
    with pytest.raises(IntegrityError), transaction.atomic():
        Slot.objects.create(
            venue=slot.venue,
            date=slot.date,
            start_time=slot.start_time,
            end_time=time(8),
        )


@pytest.mark.django_db
def test_slot_end_must_be_after_start(venue):
    with pytest.raises(IntegrityError), transaction.atomic():
        Slot.objects.create(
            venue=venue,
            date=date(2026, 7, 1),
            start_time=time(8),
            end_time=time(7),
        )


@pytest.mark.django_db
def test_slot_can_only_have_one_booking(slot):
    first_user = User.objects.create_user(username="first")
    second_user = User.objects.create_user(username="second")
    Booking.objects.create(user=first_user, slot=slot)

    with pytest.raises(IntegrityError), transaction.atomic():
        Booking.objects.create(user=second_user, slot=slot)

