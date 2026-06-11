from django.contrib import admin

from apps.bookings.models import Booking, Slot


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("venue", "date", "start_time", "end_time", "is_booked")
    list_filter = ("date", "venue__sport_type")
    search_fields = ("venue__name",)
    date_hierarchy = "date"

    @admin.display(boolean=True)
    def is_booked(self, obj):
        return hasattr(obj, "booking")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "slot", "created_at")
    list_filter = ("slot__date", "slot__venue")
    search_fields = ("user__username", "slot__venue__name")
    date_hierarchy = "created_at"

