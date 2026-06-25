from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import json
import os
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


def study_home(request):
    """Study materials home page"""
    categories = CourseCategory.objects.filter(is_active=True)

    # Get featured courses
    featured_courses = Course.objects.filter(is_active=True, is_featured=True)[:6]

    # Get popular notes
    popular_notes = Note.objects.filter(is_active=True).order_by(
        "-views", "-downloads"
    )[:6]

    # Get recent videos
    recent_videos = VideoLecture.objects.filter(is_active=True).order_by("-created_at")[
        :6
    ]

    # Get recent current affairs
    recent_affairs = CurrentAffair.objects.filter(is_active=True).order_by("-date")[:6]

    # Get featured ebooks
    featured_ebooks = EBook.objects.filter(is_active=True, is_featured=True)[:4]

    context = {
        "categories": categories,
        "featured_courses": featured_courses,
        "popular_notes": popular_notes,
        "recent_videos": recent_videos,
        "recent_affairs": recent_affairs,
        "featured_ebooks": featured_ebooks,
    }
    return render(request, "study_materials/home.html", context)


def course_list(request):
    """List all courses"""
    courses = Course.objects.filter(is_active=True).select_related("category")

    # Filter by category
    category_slug = request.GET.get("category")
    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    # Filter by difficulty
    difficulty = request.GET.get("difficulty")
    if difficulty:
        courses = courses.filter(difficulty=difficulty)

    # Filter by price
    price = request.GET.get("price")
    if price == "free":
        courses = courses.filter(is_free=True)
    elif price == "paid":
        courses = courses.filter(is_free=False)

    # Search
    search_query = request.GET.get("q")
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query)
            | Q(subtitle__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    paginator = Paginator(courses, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = CourseCategory.objects.filter(is_active=True)

    context = {
        "courses": page_obj,
        "categories": categories,
        "selected_category": category_slug,
        "selected_difficulty": difficulty,
        "selected_price": price,
        "search_query": search_query,
    }
    return render(request, "study_materials/course_list.html", context)


@login_required
def course_detail(request, slug):
    """Course detail page"""
    course = get_object_or_404(Course, slug=slug, is_active=True)

    # Check if user is enrolled
    is_enrolled = UserEnrollment.objects.filter(
        user=request.user, course=course
    ).exists()

    # Get sections and lectures
    sections = course.sections.filter(is_active=True).prefetch_related("lectures")

    # Get user's lecture progress
    lecture_progress = {}
    if is_enrolled:
        completed_lectures = UserLectureProgress.objects.filter(
            user=request.user, lecture__section__course=course, is_completed=True
        ).values_list("lecture_id", flat=True)
        lecture_progress = {lecture_id: True for lecture_id in completed_lectures}

    # Calculate total progress
    total_lectures = sum(
        section.lectures.filter(is_active=True).count() for section in sections
    )
    completed_count = len(lecture_progress)
    progress_percentage = (
        (completed_count / total_lectures * 100) if total_lectures > 0 else 0
    )

    context = {
        "course": course,
        "sections": sections,
        "is_enrolled": is_enrolled,
        "lecture_progress": lecture_progress,
        "progress_percentage": progress_percentage,
        "completed_count": completed_count,
        "total_lectures": total_lectures,
    }
    return render(request, "study_materials/course_detail.html", context)


@login_required
def enroll_course(request, course_id):
    """Enroll user in a course"""
    course = get_object_or_404(Course, id=course_id, is_active=True)

    enrollment, created = UserEnrollment.objects.get_or_create(
        user=request.user, course=course
    )

    if created:
        course.total_enrollments += 1
        course.save()
        messages.success(request, f"You have successfully enrolled in {course.title}!")
    else:
        messages.info(request, f"You are already enrolled in {course.title}")

    return redirect("study_materials:course_detail", slug=course.slug)


@login_required
def lecture_watch(request, course_slug, lecture_id):
    """Watch lecture video"""
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    lecture = get_object_or_404(
        Lecture, id=lecture_id, section__course=course, is_active=True
    )

    # Check if user is enrolled
    is_enrolled = UserEnrollment.objects.filter(
        user=request.user, course=course
    ).exists()

    if not is_enrolled and not lecture.is_free_preview:
        messages.error(request, "Please enroll in the course to access this lecture.")
        return redirect("study_materials:course_detail", slug=course.slug)

    # Get next and previous lectures
    all_lectures = Lecture.objects.filter(
        section__course=course, is_active=True
    ).order_by("section__order", "order")

    lecture_ids = list(all_lectures.values_list("id", flat=True))
    current_index = lecture_ids.index(lecture.id) if lecture.id in lecture_ids else -1

    next_lecture = None
    prev_lecture = None

    if current_index != -1:
        if current_index + 1 < len(lecture_ids):
            next_lecture = Lecture.objects.get(id=lecture_ids[current_index + 1])
        if current_index - 1 >= 0:
            prev_lecture = Lecture.objects.get(id=lecture_ids[current_index - 1])

    context = {
        "course": course,
        "lecture": lecture,
        "next_lecture": next_lecture,
        "prev_lecture": prev_lecture,
    }
    return render(request, "study_materials/lecture_watch.html", context)


@login_required
def mark_lecture_complete(request):
    """Mark lecture as completed (AJAX)"""
    if request.method == "POST":
        data = json.loads(request.body)
        lecture_id = data.get("lecture_id")
        watch_time = data.get("watch_time", 0)

        lecture = get_object_or_404(Lecture, id=lecture_id)
        course = lecture.section.course

        # Check enrollment
        enrollment = get_object_or_404(UserEnrollment, user=request.user, course=course)

        # Update or create progress
        progress, created = UserLectureProgress.objects.get_or_create(
            user=request.user, lecture=lecture
        )

        if not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = timezone.now()
            progress.watch_time = watch_time
            progress.save()

            # Update overall course progress
            total_lectures = Lecture.objects.filter(
                section__course=course, is_active=True
            ).count()
            completed_lectures = UserLectureProgress.objects.filter(
                user=request.user, lecture__section__course=course, is_completed=True
            ).count()

            enrollment.progress = (
                (completed_lectures / total_lectures * 100) if total_lectures > 0 else 0
            )
            if enrollment.progress == 100:
                enrollment.is_completed = True
                enrollment.completed_at = timezone.now()
            enrollment.save()

        return JsonResponse({"success": True, "progress": enrollment.progress})

    return JsonResponse({"error": "Invalid request"}, status=400)


def note_list(request):
    """List all study notes"""
    notes = Note.objects.filter(is_active=True).select_related("exam", "subject")

    # Filter by exam
    exam_slug = request.GET.get("exam")
    if exam_slug:
        notes = notes.filter(exam__slug=exam_slug)

    # Filter by note type
    note_type = request.GET.get("type")
    if note_type:
        notes = notes.filter(note_type=note_type)

    # Search
    search_query = request.GET.get("q")
    if search_query:
        notes = notes.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(tags__icontains=search_query)
        )

    paginator = Paginator(notes, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "notes": page_obj,
        "search_query": search_query,
    }
    return render(request, "study_materials/note_list.html", context)


def note_detail(request, slug):
    """Note detail page"""
    note = get_object_or_404(Note, slug=slug, is_active=True)

    # Increment views
    note.views += 1
    note.save()

    # Check if bookmarked
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(
            user=request.user, content_type="note", content_id=note.id
        ).exists()

    context = {
        "note": note,
        "is_bookmarked": is_bookmarked,
    }
    return render(request, "study_materials/note_detail.html", context)


def video_list(request):
    """List all video lectures"""
    videos = VideoLecture.objects.filter(is_active=True).select_related(
        "exam", "subject"
    )

    # Filter by exam
    exam_slug = request.GET.get("exam")
    if exam_slug:
        videos = videos.filter(exam__slug=exam_slug)

    # Search
    search_query = request.GET.get("q")
    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(tags__icontains=search_query)
        )

    paginator = Paginator(videos, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "videos": page_obj,
        "search_query": search_query,
    }
    return render(request, "study_materials/video_list.html", context)


def video_detail(request, slug):
    """Video detail page"""
    video = get_object_or_404(VideoLecture, slug=slug, is_active=True)

    # Increment views
    video.views += 1
    video.save()

    # Check if bookmarked
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(
            user=request.user, content_type="video", content_id=video.id
        ).exists()

    context = {
        "video": video,
        "is_bookmarked": is_bookmarked,
    }
    return render(request, "study_materials/video_detail.html", context)


def ebook_list(request):
    """List all ebooks"""
    ebooks = EBook.objects.filter(is_active=True).select_related("exam")

    # Filter by exam
    exam_slug = request.GET.get("exam")
    if exam_slug:
        ebooks = ebooks.filter(exam__slug=exam_slug)

    # Search
    search_query = request.GET.get("q")
    if search_query:
        ebooks = ebooks.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(author__icontains=search_query)
            | Q(tags__icontains=search_query)
        )

    paginator = Paginator(ebooks, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "ebooks": page_obj,
        "search_query": search_query,
    }
    return render(request, "study_materials/ebook_list.html", context)


@login_required
def download_ebook(request, ebook_id):
    """Download ebook file"""
    ebook = get_object_or_404(EBook, id=ebook_id, is_active=True)

    # Increment downloads
    ebook.downloads += 1
    ebook.save()

    if ebook.pdf_file:
        file_path = ebook.pdf_file.path
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="{ebook.title}.pdf"'
            )
            return response

    messages.error(request, "File not found")
    return redirect("study_materials:ebook_list")


def current_affairs_list(request):
    """List all current affairs"""
    affairs = CurrentAffair.objects.filter(is_active=True)

    # Filter by category
    category = request.GET.get("category")
    if category:
        affairs = affairs.filter(category=category)

    # Filter by month/year
    month = request.GET.get("month")
    if month:
        affairs = affairs.filter(date__month=month)

    year = request.GET.get("year")
    if year:
        affairs = affairs.filter(date__year=year)

    # Search
    search_query = request.GET.get("q")
    if search_query:
        affairs = affairs.filter(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(tags__icontains=search_query)
        )

    paginator = Paginator(affairs, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "affairs": page_obj,
        "selected_category": category,
        "search_query": search_query,
    }
    return render(request, "study_materials/current_affairs_list.html", context)


def current_affair_detail(request, slug):
    """Current affair detail page"""
    affair = get_object_or_404(CurrentAffair, slug=slug, is_active=True)

    # Increment views
    affair.views += 1
    affair.save()

    # Get related affairs
    related_affairs = CurrentAffair.objects.filter(
        is_active=True, category=affair.category
    ).exclude(id=affair.id)[:5]

    context = {
        "affair": affair,
        "related_affairs": related_affairs,
    }
    return render(request, "study_materials/current_affair_detail.html", context)


@login_required
def bookmark_content(request):
    """Bookmark or unbookmark content (AJAX)"""
    if request.method == "POST":
        data = json.loads(request.body)
        content_type = data.get("content_type")
        content_id = data.get("content_id")

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user, content_type=content_type, content_id=content_id
        )

        if not created:
            bookmark.delete()
            return JsonResponse(
                {"bookmarked": False, "message": "Removed from bookmarks"}
            )

        return JsonResponse({"bookmarked": True, "message": "Added to bookmarks"})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def my_bookmarks(request):
    """View user's bookmarks"""
    bookmarks = Bookmark.objects.filter(user=request.user).order_by("-created_at")

    # Group by content type
    notes = []
    videos = []
    ebooks = []
    affairs = []

    for bookmark in bookmarks:
        if bookmark.content_type == "note":
            try:
                note = Note.objects.get(id=bookmark.content_id, is_active=True)
                notes.append(note)
            except Note.DoesNotExist:
                pass
        elif bookmark.content_type == "video":
            try:
                video = VideoLecture.objects.get(id=bookmark.content_id, is_active=True)
                videos.append(video)
            except VideoLecture.DoesNotExist:
                pass
        elif bookmark.content_type == "ebook":
            try:
                ebook = EBook.objects.get(id=bookmark.content_id, is_active=True)
                ebooks.append(ebook)
            except EBook.DoesNotExist:
                pass
        elif bookmark.content_type == "current_affair":
            try:
                affair = CurrentAffair.objects.get(
                    id=bookmark.content_id, is_active=True
                )
                affairs.append(affair)
            except CurrentAffair.DoesNotExist:
                pass

    context = {
        "notes": notes,
        "videos": videos,
        "ebooks": ebooks,
        "affairs": affairs,
    }
    return render(request, "study_materials/bookmarks.html", context)


@login_required
def my_courses(request):
    """View user's enrolled courses"""
    enrollments = (
        UserEnrollment.objects.filter(user=request.user)
        .select_related("course")
        .order_by("-enrolled_at")
    )

    context = {
        "enrollments": enrollments,
    }
    return render(request, "study_materials/my_courses.html", context)


def search(request):
    """Search across all study materials"""
    query = request.GET.get("q", "")

    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(description__icontains=query),
            is_active=True,
        )[:5]

        notes = Note.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query),
            is_active=True,
        )[:5]

        videos = VideoLecture.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tags__icontains=query),
            is_active=True,
        )[:5]

        ebooks = EBook.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(author__icontains=query)
            | Q(tags__icontains=query),
            is_active=True,
        )[:5]

        affairs = CurrentAffair.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__icontains=query),
            is_active=True,
        )[:5]
    else:
        courses = notes = videos = ebooks = affairs = []

    context = {
        "query": query,
        "courses": courses,
        "notes": notes,
        "videos": videos,
        "ebooks": ebooks,
        "affairs": affairs,
        "total_results": courses.count()
        + notes.count()
        + videos.count()
        + ebooks.count()
        + affairs.count(),
    }
    return render(request, "study_materials/search_results.html", context)
