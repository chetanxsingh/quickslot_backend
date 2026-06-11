from django.conf import settings
from django.db import models
from django.db.models import F, Q


class Slot(models.Model):
    venue = models.ForeignKey(
        "venues.Venue",
        on_delete=models.CASCADE,
        related_name="slots",
    )
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date", "start_time")
        constraints = [
            models.UniqueConstraint(
                fields=("venue", "date", "start_time"),
                name="unique_venue_slot_start",
            ),
            models.CheckConstraint(
                condition=Q(end_time__gt=F("start_time")),
                name="slot_end_after_start",
            ),
        ]

    @property
    def is_booked(self):
        return hasattr(self, "booking")

    def __str__(self):
        return (
            f"{self.venue.name} on {self.date.isoformat()} "
            f"at {self.start_time.strftime('%H:%M')}"
        )


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    slot = models.OneToOneField(
        Slot,
        on_delete=models.PROTECT,
        related_name="booking",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} booked {self.slot}"

