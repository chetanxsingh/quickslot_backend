from django.db import models


class Venue(models.Model):
    class SportType(models.TextChoices):
        BADMINTON = "badminton", "Badminton"
        FOOTBALL = "football", "Football"
        CRICKET = "cricket", "Cricket"
        TENNIS = "tennis", "Tennis"

    name = models.CharField(max_length=120, unique=True)
    sport_type = models.CharField(max_length=20, choices=SportType.choices)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

