from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


@admin.register(User)
class QuickSlotUserAdmin(UserAdmin):
    list_display = ("id", "username", "display_name", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")

    @admin.display(description="Name")
    def display_name(self, obj):
        return obj.display_name

