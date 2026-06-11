from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=100)
    sport_type = models.CharField(max_length=50)
    location = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name