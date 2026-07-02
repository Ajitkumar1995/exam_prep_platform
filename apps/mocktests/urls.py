from django.urls import path
from . import views
from apps.payments import cart_views

app_name = "mocktests"

urlpatterns = [
    path("", views.mock_test_list, name="list"),
    path("cart/", cart_views.view_cart, name="cart"),
    path(
        "add-to-cart/<int:mock_test_id>/",
        views.add_to_cart_redirect,
        name="add_to_cart",
    ),
    path("checkout/", cart_views.checkout, name="checkout"),
    path("take/<int:test_id>/", views.take_mock_test, name="take_mock_test"),
    path("save-answer/", views.save_answer, name="save_answer"),
    path(
        "save-answer/<int:attempt_id>/", views.save_answer_ajax, name="save_answer_ajax"
    ),
    path("submit/<int:attempt_id>/", views.submit_test, name="submit"),
    path(
        "submit-alternate/<int:attempt_id>/",
        views.submit_mock_test,
        name="submit_mock_test",
    ),
    path("results/<int:attempt_id>/", views.test_results, name="results"),
    path(
        "api/question/<int:attempt_id>/<int:question_id>/",
        views.get_question_data,
        name="get_question_data",
    ),
    path("<slug:slug>/", views.mock_test_detail, name="detail"),
    path("<slug:slug>/start/", views.start_test, name="start"),
]
