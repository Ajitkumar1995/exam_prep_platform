from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    CourseCategory,
    Course,
    Section,
    Lecture,
    Note,
    VideoLecture,
    EBook,
    CurrentAffair,
    UserEnrollment,
    UserLectureProgress,
    Bookmark,
)


class SectionInline(admin.TabularInline):
    model = Section
    extra = 1
    fields = ["title", "order", "is_active"]
    classes = ["collapse"]


class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1
    fields = [
        "title",
        "lecture_type",
        "duration",
        "order",
        "is_free_preview",
        "is_active",
    ]
    classes = ["collapse"]


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "order", "total_courses", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "description"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}

    def total_courses(self, obj):
        return obj.courses.filter(is_active=True).count()

    total_courses.short_description = "Courses"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "difficulty",
        "is_free",
        "is_featured",
        "is_active",
        "order",
    ]
    list_filter = ["category", "difficulty", "is_free", "is_featured", "is_active"]
    search_fields = ["title", "subtitle"]
    list_editable = ["order", "is_featured", "is_active"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SectionInline]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("category", "exam", "title", "slug", "subtitle", "difficulty")},
        ),
        (
            "Description",
            {
                "fields": ("description", "objectives", "requirements"),
            },
        ),
        ("Media", {"fields": ("thumbnail", "promo_video")}),
        ("Pricing", {"fields": ("is_free", "price", "discounted_price")}),
        (
            "Statistics",
            {
                "fields": (
                    "total_lectures",
                    "total_duration",
                    "total_enrollments",
                    "rating",
                ),
            },
        ),
        ("Status", {"fields": ("is_active", "is_featured", "order")}),
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["title", "course_link", "order", "total_lectures", "is_active"]
    list_filter = ["course", "is_active"]
    search_fields = ["title", "course__title"]
    list_editable = ["order", "is_active"]
    inlines = [LectureInline]

    def course_link(self, obj):
        url = reverse("admin:study_materials_course_change", args=[obj.course.id])
        return format_html('<a href="{}">{}</a>', url, obj.course.title)

    course_link.short_description = "Course"

    def total_lectures(self, obj):
        return obj.lectures.filter(is_active=True).count()

    total_lectures.short_description = "Lectures"


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "section_link",
        "lecture_type",
        "duration",
        "is_free_preview",
        "is_active",
        "order",
    ]
    list_filter = ["lecture_type", "is_free_preview", "is_active"]
    search_fields = ["title", "description"]
    list_editable = ["duration", "is_free_preview", "is_active", "order"]

    def section_link(self, obj):
        url = reverse("admin:study_materials_section_change", args=[obj.section.id])
        return format_html('<a href="{}">{}</a>', url, obj.section.title)

    section_link.short_description = "Section"


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "exam",
        "subject",
        "note_type",
        "views",
        "downloads",
        "is_free",
        "is_active",
        "order",
    ]
    list_filter = ["exam", "subject", "note_type", "is_free", "is_active"]
    search_fields = ["title", "description", "author"]
    list_editable = ["is_free", "is_active", "order"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(VideoLecture)
class VideoLectureAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "exam",
        "subject",
        "duration",
        "views",
        "is_free",
        "is_active",
        "order",
    ]
    list_filter = ["exam", "subject", "is_free", "is_active"]
    search_fields = ["title", "description"]
    list_editable = ["is_free", "is_active", "order"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(EBook)
class EBookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "exam",
        "author",
        "pages",
        "downloads",
        "is_free",
        "is_active",
        "order",
    ]
    list_filter = ["exam", "is_free", "is_active"]
    search_fields = ["title", "author"]
    list_editable = ["is_free", "is_active", "order"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(CurrentAffair)
class CurrentAffairAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "date", "source", "views", "is_active"]
    list_filter = ["category", "is_active", "date"]
    search_fields = ["title", "content", "source"]
    list_editable = ["is_active"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"


@admin.register(UserEnrollment)
class UserEnrollmentAdmin(admin.ModelAdmin):
    list_display = ["user", "course_link", "progress", "is_completed", "enrolled_at"]
    list_filter = ["is_completed", "course"]
    search_fields = ["user__email", "course__title"]

    def course_link(self, obj):
        url = reverse("admin:study_materials_course_change", args=[obj.course.id])
        return format_html('<a href="{}">{}</a>', url, obj.course.title)

    course_link.short_description = "Course"


@admin.register(UserLectureProgress)
class UserLectureProgressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "lecture_link",
        "is_completed",
        "watch_time",
        "last_watched",
    ]
    list_filter = ["is_completed"]
    search_fields = ["user__email", "lecture__title"]

    def lecture_link(self, obj):
        url = reverse("admin:study_materials_lecture_change", args=[obj.lecture.id])
        return format_html('<a href="{}">{}</a>', url, obj.lecture.title)

    lecture_link.short_description = "Lecture"


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "content_type", "content_id", "created_at"]
    list_filter = ["content_type"]
    search_fields = ["user__email"]
