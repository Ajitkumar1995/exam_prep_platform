from django.urls import path
from . import views

app_name = "exams"

urlpatterns = [
    path("", views.exam_list, name="list"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("<slug:slug>/", views.exam_detail, name="detail"),
    path("<slug:slug>/coaching/", views.exam_coaching, name="coaching"),
    path("<slug:slug>/mock-tests/", views.exam_mock_tests, name="mock_tests"),
    path(
        "<slug:slug>/study-material/", views.exam_study_material, name="study_material"
    ),
    path(
        "<slug:exam_slug>/start-free-mock-test/",
        views.start_free_mock_test,
        name="start_free_mock_test",
    ),
    path("<slug:exam_slug>/enroll-now/", views.enroll_now, name="enroll_now"),
    path(
        "challenge/<slug:challenge_slug>/",
        views.take_daily_challenge,
        name="take_daily_challenge",
    ),
    path("live-test/<int:test_id>/", views.join_live_test, name="join_live_test"),
]
