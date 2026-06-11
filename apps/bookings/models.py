from django.db import models


class Slot(models.Model):
    venue = models.ForeignKey(
        "venues.Venue",
        on_delete=models.CASCADE,
        related_name="slots",
    )

    date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = (
            "venue",
            "date",
            "start_time",
        )

    def __str__(self):
        return (
            f"{self.venue.name} "
            f"{self.date} "
            f"{self.start_time}"
        )


class Booking(models.Model):
    user_id = models.IntegerField()

    slot = models.OneToOneField(
        Slot,
        on_delete=models.CASCADE,
        related_name="booking",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )