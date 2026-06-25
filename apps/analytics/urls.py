from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    # Main dashboard
    path("", views.analytics_dashboard, name="dashboard"),
    # Exam-specific analytics
    path("exam/<slug:exam_slug>/", views.exam_analytics, name="exam_analytics"),
    # API endpoints for charts and real-time data
    path("api/performance/", views.get_performance_data, name="performance_data"),
    path(
        "api/attempt/<int:attempt_id>/",
        views.get_attempt_details,
        name="attempt_details",
    ),
    path("api/update-stats/", views.update_all_stats, name="update_stats"),
    path("api/recommendations/", views.get_recommendations, name="recommendations"),
    path("api/leaderboard/", views.get_leaderboard, name="leaderboard"),
    path("api/weekly-progress/", views.get_weekly_progress, name="weekly_progress"),
]

# from django.urls import path
# from . import views

# app_name = 'analytics'

# urlpatterns = [
#     # Main dashboard
#     path('', views.analytics_dashboard, name='dashboard'),

#     # Exam-specific analytics
#     path('exam/<slug:exam_slug>/', views.exam_analytics, name='exam_analytics'),

#     # API endpoints
#     path('api/performance/', views.get_performance_data, name='performance_data'),
#     path('api/attempt/<int:attempt_id>/', views.get_attempt_details, name='attempt_details'),
#     path('api/update-stats/', views.update_all_stats, name='update_stats'),
#     path('api/recommendations/', views.get_recommendations, name='recommendations'),
# ]
