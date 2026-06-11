from django.contrib import admin

from apps.venues.models import Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "sport_type", "city", "is_active")
    list_filter = ("sport_type", "city", "is_active")
    search_fields = ("name", "address", "city")

