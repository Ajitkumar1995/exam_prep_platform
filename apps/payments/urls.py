from django.urls import path
from . import views
from . import cart_views

app_name = "payments"

urlpatterns = [
    # ==================== CART & CHECKOUT ROUTES ====================
    path("cart/", cart_views.view_cart, name="view_cart"),
    path(
        "add-to-cart/<str:item_type>/<int:item_id>/",
        cart_views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "cart/remove/<int:item_id>/",
        cart_views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", cart_views.checkout, name="checkout"),
    path("place-order/", cart_views.place_order, name="place_order"),
    path(
        "order-confirmation/<int:order_id>/",
        cart_views.order_confirmation,
        name="order_confirmation",
    ),
    path("my-orders/", cart_views.my_orders, name="my_orders"),
    # ==================== DIRECT PAYMENT ROUTES ====================
    path("pay/<str:item_type>/<int:item_id>/", views.payment_page, name="payment_page"),
    path(
        "initiate/<int:transaction_id>/",
        views.initiate_payment,
        name="initiate_payment",
    ),
    # ==================== PAYTM PAYMENT ROUTES ====================
    path("paytm-callback/<str:order_id>/", views.paytm_callback, name="paytm_callback"),
    path("paytm-webhook/", views.paytm_webhook, name="paytm_webhook"),
    path("paytm-test/", views.paytm_test, name="paytm_test"),
    path(
        "paytm-status/<str:order_id>/",
        views.paytm_payment_status,
        name="paytm_payment_status",
    ),
    # ==================== GENERAL PAYMENT STATUS ====================
    path(
        "check-status/<int:transaction_id>/",
        views.check_payment_status,
        name="check_status",
    ),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
    # ==================== USER PURCHASES ====================
    path("my-purchases/", views.my_purchases, name="my_purchases"),
    # ==================== ADMIN ROUTES ====================
    path("admin/payments/", views.admin_payments, name="admin_payments"),
    path(
        "admin/manual-unlock/<int:transaction_id>/",
        views.admin_manual_unlock,
        name="admin_manual_unlock",
    ),
]
