from datetime import date, datetime, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.bookings.models import Slot
from apps.users.models import User
from apps.venues.models import Venue


DEMO_USERS = (
    {"username": "aisha", "first_name": "Aisha", "last_name": "Khan"},
    {"username": "rohan", "first_name": "Rohan", "last_name": "Mehta"},
    {"username": "maya", "first_name": "Maya", "last_name": "Patel"},
)

DEMO_VENUES = (
    {
        "name": "SmashPoint Badminton Arena",
        "sport_type": Venue.SportType.BADMINTON,
        "address": "12 Vijay Nagar Main Road",
        "city": "Indore",
    },
    {
        "name": "GreenField Turf",
        "sport_type": Venue.SportType.FOOTBALL,
        "address": "44 Scheme No. 78",
        "city": "Indore",
    },
    {
        "name": "Ace Tennis Centre",
        "sport_type": Venue.SportType.TENNIS,
        "address": "8 Race Course Road",
        "city": "Indore",
    },
    {
        "name": "Boundary Box Cricket Ground",
        "sport_type": Venue.SportType.CRICKET,
        "address": "21 Super Corridor",
        "city": "Indore",
    },
)


class Command(BaseCommand):
    help = "Seed demo users, venues, and hourly slots from 6 AM to 10 PM."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=14,
            help="Number of consecutive days to generate. Defaults to 14.",
        )
        parser.add_argument(
            "--start-date",
            type=str,
            help="First slot date in YYYY-MM-DD format. Defaults to today.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        days = options["days"]
        if days < 1:
            raise CommandError("--days must be at least 1.")

        start_date = self.parse_start_date(options.get("start_date"))

        for user_data in DEMO_USERS:
            user, _ = User.objects.update_or_create(
                username=user_data["username"],
                defaults={
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "is_active": True,
                },
            )
            user.set_unusable_password()
            user.save(update_fields=("password",))

        venues = []
        for venue_data in DEMO_VENUES:
            venue, _ = Venue.objects.update_or_create(
                name=venue_data["name"],
                defaults={
                    "sport_type": venue_data["sport_type"],
                    "address": venue_data["address"],
                    "city": venue_data["city"],
                    "is_active": True,
                },
            )
            venues.append(venue)

        slots_to_create = []
        for venue in venues:
            for day_offset in range(days):
                slot_date = start_date + timedelta(days=day_offset)
                for hour in range(6, 22):
                    slots_to_create.append(
                        Slot(
                            venue=venue,
                            date=slot_date,
                            start_time=time(hour=hour),
                            end_time=time(hour=hour + 1),
                        )
                    )

        Slot.objects.bulk_create(slots_to_create, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(DEMO_USERS)} users, {len(venues)} venues, and "
                f"{days} days of hourly slots starting {start_date.isoformat()}."
            )
        )

    @staticmethod
    def parse_start_date(value):
        if not value:
            return date.today()

        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise CommandError("--start-date must use YYYY-MM-DD format.") from exc

