# problem/admin.py

from django.contrib import admin
from .models import Problem

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Problem model.
    Allows viewing and managing problem submissions in the Django admin,
    now including the 'submitter' field that references the CustomUser model.
    """

    # Fields to display in the list view
    list_display = (
        "problem_title",
        "submitter",       # <-- Display which user (if any) submitted this Problem
        "category",
        "urgency",
        "country",
        "city",
        "contact_email",
        "date_created",
    )

    # Fields to enable searching by keyword
    search_fields = (
        "problem_title",
        "description",
        "category",
        "contact_name",
        "contact_email",
        "contact_phone",
        # Also allow searching by the submitter's email via the related model:
        "submitter__email",
        # If you wish to also search by username, you can add:
        # "submitter__username",
    )

    # Fields to enable filtering
    list_filter = (
        "category",
        "urgency",
        "country",
        "city",
        "date_created",
        # You can also filter by submitter if desired:
        "submitter",
    )

    # Make certain fields read-only if you do not want them edited in admin
    readonly_fields = ("date_created",)

    # Organize the admin form with fieldsets
    fieldsets = (
        ("Problem Details", {
            "fields": (
                "submitter",        # <-- Show the submitter (if any) in the first section
                "problem_title",
                "description",
                "category",
                "urgency",
            )
        }),
        ("Location Info", {
            "fields": (
                "country",
                "city",
                "latitude",
                "longitude",
            )
        }),
        ("Media", {
            "fields": (
                "media_files",
                "submitter_photo",
            )
        }),
        ("Contact Info", {
            "fields": (
                "contact_name",
                "contact_email",
                "contact_phone",
            )
        }),
        ("Timestamps", {
            "fields": (
                "date_created",
            )
        }),
    )
