from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="list"),
    path("<slug:slug>/", views.notification_detail, name="detail"),
    path("track-click/<int:notification_id>/", views.track_click, name="track_click"),
    path("api/navbar/", views.get_navbar_notifications, name="api_navbar"),
]
