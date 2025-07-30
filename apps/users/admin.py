from django.contrib import admin
from apps.users.models import AppUser

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AppUser model, including ordering by email and displaying specific fields in the admin list view.
    """
    ordering = ("email",)
    list_display = [
        "uuid",
        "email",
        "first_name",
        "last_name",
    ]
