from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Notification(models.Model):
    """System notifications - visible to all users, no login required"""

    PRIORITY = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    )

    DISPLAY_LOCATION = (
        ("navbar", "Navbar Bell Icon Only"),
        ("homepage", "Homepage Section Only"),
        ("both", "Both Navbar and Homepage"),
        ("popup", "Popup Modal"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    message = CKEditor5Field()
    priority = models.CharField(max_length=20, choices=PRIORITY, default="medium")

    # Display settings
    display_location = models.CharField(
        max_length=20, choices=DISPLAY_LOCATION, default="both"
    )
    show_bell_icon = models.BooleanField(
        default=True, help_text="Show in navbar bell icon"
    )
    show_on_homepage = models.BooleanField(
        default=True, help_text="Show in homepage notifications section"
    )
    show_as_popup = models.BooleanField(
        default=False, help_text="Show as popup modal on page load"
    )

    # Links and actions
    action_url = models.URLField(blank=True, help_text="URL to redirect when clicked")
    button_text = models.CharField(max_length=50, blank=True, default="View Details")
    image = models.ImageField(upload_to="notification_images/", null=True, blank=True)

    # Scheduling
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Order
    order = models.IntegerField(default=0)

    # Statistics
    views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def is_valid(self):
        """Check if notification is currently valid based on dates"""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True


class Announcement(models.Model):
    """Important announcements (displayed prominently)"""

    ANNOUNCEMENT_TYPE = (
        ("banner", "Top Banner"),
        ("card", "Card"),
        ("marquee", "Marquee/Ticker"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = CKEditor5Field()
    summary = models.CharField(max_length=300, blank=True)

    announcement_type = models.CharField(
        max_length=20, choices=ANNOUNCEMENT_TYPE, default="card"
    )

    # Colors
    bg_color = models.CharField(
        max_length=20, default="bg-blue-500", help_text="Tailwind background color"
    )
    text_color = models.CharField(
        max_length=20, default="text-white", help_text="Tailwind text color"
    )

    # Scheduling
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Priority
    is_urgent = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False, help_text="Always show at top")

    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_sticky", "order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True


class NotificationView(models.Model):
    """Track notification views (no login required)"""

    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="views_log"
    )
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["notification", "session_key"]

    def __str__(self):
        return f"{self.notification.title} - {self.session_key}"


class NotificationClick(models.Model):
    """Track notification clicks"""

    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name="clicks_log"
    )
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification.title} - {self.session_key}"
