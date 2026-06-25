from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Notification, Announcement, NotificationView, NotificationClick


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "priority",
        "show_bell_icon",
        "show_on_homepage",
        "is_active",
        "start_date",
        "views",
        "clicks",
    ]
    list_filter = ["priority", "show_bell_icon", "show_on_homepage", "is_active"]
    search_fields = ["title", "message"]
    list_editable = ["is_active", "show_bell_icon", "show_on_homepage"]
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("Basic Information", {"fields": ("title", "slug", "message", "priority")}),
        (
            "Display Settings",
            {
                "fields": (
                    "show_bell_icon",
                    "show_on_homepage",
                    "show_as_popup",
                    "order",
                )
            },
        ),
        (
            "Action Button",
            {
                "fields": ("action_url", "button_text", "image"),
                "classes": ("collapse",),
            },
        ),
        ("Schedule", {"fields": ("start_date", "end_date", "is_active")}),
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "announcement_type",
        "is_urgent",
        "is_active",
        "start_date",
    ]
    list_filter = ["announcement_type", "is_urgent", "is_active"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(NotificationView)
class NotificationViewAdmin(admin.ModelAdmin):
    list_display = ["notification", "session_key", "viewed_at"]
    list_filter = ["viewed_at"]
    readonly_fields = ["viewed_at"]

    def has_add_permission(self, request):
        return False


@admin.register(NotificationClick)
class NotificationClickAdmin(admin.ModelAdmin):
    list_display = ["notification", "session_key", "clicked_at"]
    list_filter = ["clicked_at"]
    readonly_fields = ["clicked_at"]

    def has_add_permission(self, request):
        return False
