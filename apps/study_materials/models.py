from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from apps.exams.models import Exam, Subject

User = get_user_model()


class CourseCategory(models.Model):
    """Main category for courses"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default="fa-book")
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Course Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def total_courses(self):
        return self.courses.filter(is_active=True).count()


class Course(models.Model):
    """Main course model"""

    DIFFICULTY = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    )

    category = models.ForeignKey(
        CourseCategory, on_delete=models.CASCADE, related_name="courses"
    )
    exam = models.ForeignKey(
        Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses"
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    description = CKEditor5Field()
    objectives = CKEditor5Field(blank=True, help_text="What students will learn")
    requirements = CKEditor5Field(blank=True, help_text="Prerequisites")

    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY, default="intermediate"
    )

    thumbnail = models.ImageField(upload_to="course_thumbnails/", null=True, blank=True)
    promo_video = models.URLField(blank=True, help_text="YouTube or Vimeo URL")

    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    total_lectures = models.IntegerField(default=0)
    total_duration = models.IntegerField(
        default=0, help_text="Total duration in minutes"
    )
    total_enrollments = models.IntegerField(default=0)
    rating = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

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

    def get_absolute_url(self):
        return reverse("study_materials:course_detail", args=[self.slug])


class Section(models.Model):
    """Course sections/chapters"""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sections"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def total_lectures(self):
        return self.lectures.filter(is_active=True).count()


class Lecture(models.Model):
    """Individual video lectures"""

    LECTURE_TYPE = (
        ("video", "Video Lecture"),
        ("document", "Document"),
        ("quiz", "Quiz"),
        ("assignment", "Assignment"),
    )

    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="lectures"
    )
    title = models.CharField(max_length=200)
    description = CKEditor5Field(blank=True)

    lecture_type = models.CharField(
        max_length=20, choices=LECTURE_TYPE, default="video"
    )

    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL")
    video_embed_code = models.TextField(blank=True)
    document = models.FileField(upload_to="lecture_documents/", null=True, blank=True)
    content = CKEditor5Field(blank=True)

    duration = models.IntegerField(default=0, help_text="Duration in minutes")
    order = models.IntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.section.course.title} - {self.title}"

    def get_embed_url(self):
        if "youtube.com" in self.video_url or "youtu.be" in self.video_url:
            if "youtu.be" in self.video_url:
                video_id = self.video_url.split("/")[-1]
            else:
                video_id = self.video_url.split("v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url


class Note(models.Model):
    """Study notes/PDF materials"""

    NOTE_TYPE = (
        ("handwritten", "Handwritten Notes"),
        ("typed", "Typed Notes"),
        ("summary", "Chapter Summary"),
        ("formula", "Formula Sheet"),
    )

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="notes", null=True, blank=True
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="notes", null=True, blank=True
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    content = CKEditor5Field()
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE, default="typed")

    pdf_file = models.FileField(upload_to="notes/", null=True, blank=True)
    cover_image = models.ImageField(upload_to="note_covers/", null=True, blank=True)

    author = models.CharField(max_length=100, blank=True)
    pages = models.IntegerField(default=0)
    file_size = models.CharField(max_length=50, blank=True)

    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    tags = models.CharField(max_length=500, blank=True)

    is_free = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

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

    def get_absolute_url(self):
        return reverse("study_materials:note_detail", args=[self.slug])


class VideoLecture(models.Model):
    """Video lectures (standalone)"""

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="video_lectures",
        null=True,
        blank=True,
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="video_lectures",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field()

    video_url = models.URLField(help_text="YouTube or Vimeo URL")
    thumbnail = models.ImageField(upload_to="video_thumbnails/", null=True, blank=True)

    duration = models.CharField(max_length=50, help_text="e.g., 15:30")

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    tags = models.CharField(max_length=500, blank=True)

    is_free = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

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

    def get_embed_url(self):
        if "youtube.com" in self.video_url or "youtu.be" in self.video_url:
            if "youtu.be" in self.video_url:
                video_id = self.video_url.split("/")[-1]
            else:
                video_id = self.video_url.split("v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url


class EBook(models.Model):
    """E-Books and digital publications"""

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="ebooks", null=True, blank=True
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field()

    author = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)
    pages = models.IntegerField(default=0)

    cover_image = models.ImageField(upload_to="ebook_covers/", null=True, blank=True)
    pdf_file = models.FileField(upload_to="ebooks/")

    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    tags = models.CharField(max_length=500, blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

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


class CurrentAffair(models.Model):
    """Current affairs articles"""

    CATEGORY = (
        ("national", "National"),
        ("international", "International"),
        ("economy", "Economy"),
        ("science", "Science & Technology"),
        ("environment", "Environment"),
        ("sports", "Sports"),
        ("appointments", "Appointments"),
        ("awards", "Awards & Honors"),
        ("defence", "Defence"),
        ("other", "Other"),
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default="national")

    content = CKEditor5Field()
    summary = models.TextField(blank=True, help_text="Short summary for listing")

    date = models.DateField()
    source = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to="current_affairs/", null=True, blank=True)

    tags = models.CharField(max_length=500, blank=True)
    important_for = models.CharField(max_length=500, blank=True)

    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name_plural = "Current Affairs"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.title[:80]}"


class UserEnrollment(models.Model):
    """Track user course enrollments"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0, help_text="Completion percentage")
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "course"]
        ordering = ["-enrolled_at"]

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"


class UserLectureProgress(models.Model):
    """Track user's lecture progress"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lecture_progress"
    )
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="user_progress"
    )
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_watched = models.DateTimeField(auto_now=True)
    watch_time = models.IntegerField(default=0, help_text="Watch time in seconds")

    class Meta:
        unique_together = ["user", "lecture"]

    def __str__(self):
        return f"{self.user.email} - {self.lecture.title}"


class Bookmark(models.Model):
    """User bookmarks for notes, videos, etc."""

    CONTENT_TYPE = (
        ("note", "Note"),
        ("video", "Video Lecture"),
        ("ebook", "E-Book"),
        ("current_affair", "Current Affair"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE)
    content_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "content_type", "content_id"]

    def __str__(self):
        return f"{self.user.email} - {self.content_type} - {self.content_id}"
