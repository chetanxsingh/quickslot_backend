from datetime import date, time

import pytest
from django.core.management import call_command

from apps.bookings.models import Slot
from apps.users.models import User
from apps.venues.models import Venue


@pytest.mark.django_db
def test_seed_demo_data_is_complete_and_idempotent():
    command_options = {"days": 2, "start_date": "2026-07-01", "verbosity": 0}

    call_command("seed_demo_data", **command_options)
    call_command("seed_demo_data", **command_options)

    assert User.objects.count() == 3
    assert Venue.objects.count() == 4
    assert Slot.objects.count() == 4 * 2 * 16

    first_slot = Slot.objects.order_by("date", "start_time").first()
    last_slot = Slot.objects.order_by("date", "start_time").last()

    assert first_slot.date == date(2026, 7, 1)
    assert first_slot.start_time == time(6)
    assert last_slot.date == date(2026, 7, 2)
    assert last_slot.end_time == time(22)

