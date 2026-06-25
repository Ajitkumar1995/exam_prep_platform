from django.urls import path
from . import views

app_name = "study_materials"

urlpatterns = [
    # Home
    path("", views.study_home, name="home"),
    path("search/", views.search, name="search"),
    # Courses
    path("courses/", views.course_list, name="course_list"),
    path("courses/<slug:slug>/", views.course_detail, name="course_detail"),
    path("courses/enroll/<int:course_id>/", views.enroll_course, name="enroll_course"),
    path(
        "courses/<slug:course_slug>/lecture/<int:lecture_id>/",
        views.lecture_watch,
        name="lecture_watch",
    ),
    path(
        "mark-lecture-complete/",
        views.mark_lecture_complete,
        name="mark_lecture_complete",
    ),
    path("my-courses/", views.my_courses, name="my_courses"),
    # Notes
    path("notes/", views.note_list, name="note_list"),
    path("notes/<slug:slug>/", views.note_detail, name="note_detail"),
    # Videos
    path("videos/", views.video_list, name="video_list"),
    path("videos/<slug:slug>/", views.video_detail, name="video_detail"),
    # Ebooks
    path("ebooks/", views.ebook_list, name="ebook_list"),
    path(
        "ebooks/download/<int:ebook_id>/", views.download_ebook, name="download_ebook"
    ),
    # Current Affairs
    path("current-affairs/", views.current_affairs_list, name="current_affairs_list"),
    path(
        "current-affairs/<slug:slug>/",
        views.current_affair_detail,
        name="current_affair_detail",
    ),
    # Bookmarks
    path("bookmarks/", views.my_bookmarks, name="bookmarks"),
    path("bookmark/", views.bookmark_content, name="bookmark_content"),
]
