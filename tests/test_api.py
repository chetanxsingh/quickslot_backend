from datetime import date, time

import pytest
from django.urls import reverse

from apps.bookings.models import Booking, Slot
from apps.users.models import User
from apps.venues.models import Venue


@pytest.fixture
def api_data():
    user = User.objects.create_user(
        username="aisha",
        first_name="Aisha",
        last_name="Khan",
    )
    other_user = User.objects.create_user(username="rohan")
    venue = Venue.objects.create(
        name="Test Arena",
        sport_type=Venue.SportType.BADMINTON,
        address="1 Test Street",
        city="Indore",
    )
    slot = Slot.objects.create(
        venue=venue,
        date=date(2026, 7, 1),
        start_time=time(6),
        end_time=time(7),
    )
    return {
        "user": user,
        "other_user": other_user,
        "venue": venue,
        "slot": slot,
    }


@pytest.mark.django_db
def test_lists_users_and_venues(client, api_data):
    users_response = client.get(reverse("user-list"))
    venues_response = client.get(reverse("venue-list"))

    assert users_response.status_code == 200
    assert users_response.json()[0]["name"] == "Aisha Khan"
    assert venues_response.status_code == 200
    assert venues_response.json()[0]["sport_type"] == "badminton"


@pytest.mark.django_db
def test_lists_slots_for_date_with_status(client, api_data):
    url = reverse("venue-slot-list", args=[api_data["venue"].id])

    response = client.get(url, {"date": "2026-07-01"})

    assert response.status_code == 200
    assert response.json()[0]["status"] == "available"


@pytest.mark.django_db
def test_slot_date_is_required(client, api_data):
    url = reverse("venue-slot-list", args=[api_data["venue"].id])

    response = client.get(url)

    assert response.status_code == 400
    assert "date" in response.json()


@pytest.mark.django_db
def test_creates_and_lists_booking(client, api_data):
    headers = {"HTTP_X_USER_ID": str(api_data["user"].id)}

    create_response = client.post(
        reverse("booking-create"),
        {"slot_id": api_data["slot"].id},
        content_type="application/json",
        **headers,
    )
    list_response = client.get(
        reverse("user-booking-list", args=[api_data["user"].id]),
        **headers,
    )

    assert create_response.status_code == 201
    assert create_response.json()["slot"]["venue"]["name"] == "Test Arena"
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


@pytest.mark.django_db
def test_rejects_second_booking_with_conflict(client, api_data):
    Booking.objects.create(user=api_data["other_user"], slot=api_data["slot"])

    response = client.post(
        reverse("booking-create"),
        {"slot_id": api_data["slot"].id},
        content_type="application/json",
        HTTP_X_USER_ID=str(api_data["user"].id),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "This slot has already been booked."


@pytest.mark.django_db
def test_booking_requires_valid_user_header(client, api_data):
    response = client.post(
        reverse("booking-create"),
        {"slot_id": api_data["slot"].id},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "X-User-Id" in response.json()


@pytest.mark.django_db
def test_user_cannot_access_another_users_bookings(client, api_data):
    response = client.get(
        reverse("user-booking-list", args=[api_data["other_user"].id]),
        HTTP_X_USER_ID=str(api_data["user"].id),
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_owner_can_cancel_booking(client, api_data):
    booking = Booking.objects.create(user=api_data["user"], slot=api_data["slot"])

    response = client.delete(
        reverse("booking-detail", args=[booking.id]),
        HTTP_X_USER_ID=str(api_data["user"].id),
    )

    assert response.status_code == 204
    assert not Booking.objects.filter(id=booking.id).exists()

