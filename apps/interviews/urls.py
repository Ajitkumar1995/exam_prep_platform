from django.urls import path
from . import views

app_name = "interviews"

urlpatterns = [
    # Main pages
    path("", views.interview_home, name="home"),
    path("questions/", views.question_bank, name="questions"),
    path("practice/<int:pk>/", views.practice_question, name="practice"),
    path("mock-interview/", views.mock_interview, name="mock_interview"),
    path("tips/", views.interview_tips, name="tips"),
    path("my-progress/", views.my_progress, name="my_progress"),
    # Category pages
    path("category/<slug:slug>/", views.category_questions, name="category_questions"),
    # API endpoints
    path("submit-answer/", views.submit_answer, name="submit_answer"),
    path("save-progress/", views.save_progress, name="save_progress"),
]
