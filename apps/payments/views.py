import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from .models import (
    PaymentTransaction,
    UnlockedExam,
    UnlockedMockTest,
    Order,
    OrderItem,
    Cart,
    CartItem,
)
from .paytm_utils import paytm_gateway
from apps.exams.models import Exam
from apps.mocktests.models import MockTest
import logging

logger = logging.getLogger(__name__)


# ==================== PAYMENT PAGE ====================


@login_required
def payment_page(request, item_type, item_id):
    """Show payment page for exam or mock test"""

    if item_type == "exam":
        item = get_object_or_404(Exam, id=item_id, is_active=True)
        price = float(item.price)
        item_name = item.name
    elif item_type == "mock_test":
        item = get_object_or_404(MockTest, id=item_id, is_active=True)
        price = float(item.price)
        item_name = item.name
    else:
        messages.error(request, "Invalid item type")
        return redirect("home")

    # Check if already unlocked
    if has_payment_access(request.user, item_type, item.id):
        messages.info(request, f"You already have access to {item_name}")
        return redirect(get_redirect_url(item_type, item))

    # If free, grant access directly
    if price == 0:
        unlock_item(request.user, item_type, item)
        messages.success(request, f"{item_name} has been unlocked for free!")
        return redirect(get_redirect_url(item_type, item))

    # Create or get existing pending transaction
    transaction, created = PaymentTransaction.objects.get_or_create(
        user=request.user,
        item_type=item_type,
        exam=item if item_type == "exam" else None,
        mock_test=item if item_type == "mock_test" else None,
        amount=price,
        status="pending",
        defaults={"order_id": str(uuid.uuid4())},
    )

    context = {
        "item": item,
        "item_type": item_type,
        "item_name": item_name,
        "price": price,
        "transaction": transaction,
        "paytm_enabled": getattr(settings, "PAYTM_ENABLED", True),
    }
    return render(request, "payments/payment_page.html", context)


# ==================== PAYTM PAYMENT INITIATION ====================


@login_required
def initiate_payment(request, transaction_id):
    """Initiate PayTM payment"""
    transaction = get_object_or_404(
        PaymentTransaction, id=transaction_id, user=request.user
    )

    if transaction.status != "pending":
        messages.error(request, "This transaction is already processed")
        item_id = transaction.exam.id if transaction.exam else transaction.mock_test.id
        return redirect(
            "payments:payment_page", item_type=transaction.item_type, item_id=item_id
        )

    # Create payment request
    callback_url = request.build_absolute_uri(
        f"/payments/paytm-callback/{transaction.order_id}/"
    )
    user_phone = getattr(request.user, "phone", "7777777777")

    result = paytm_gateway.create_payment_request(
        order_id=transaction.order_id,
        amount=float(transaction.amount),
        user_id=request.user.id,
        user_email=request.user.email,
        user_phone=user_phone,
        callback_url=callback_url,
    )

    if result["success"]:
        # Update transaction
        transaction.merchant_transaction_id = result["merchant_transaction_id"]
        transaction.status = "processing"
        transaction.save()

        # For PayTM, we need to render a form that auto-submits or redirect to URL
        if result.get("payment_url"):
            # Direct redirect (new API)
            return redirect(result["payment_url"])
        else:
            # Form-based payment (old API)
            return render(
                request,
                "payments/paytm_redirect.html",
                {
                    "payment_params": result["form_params"],
                    "paytm_url": result["action_url"],
                },
            )
    else:
        messages.error(
            request,
            f'Failed to initiate PayTM payment: {result.get("error", "Unknown error")}',
        )
        item_id = transaction.exam.id if transaction.exam else transaction.mock_test.id
        return redirect(
            "payments:payment_page", item_type=transaction.item_type, item_id=item_id
        )


# ==================== PAYTM CALLBACKS ====================


@login_required
def paytm_callback(request, order_id):
    """Handle PayTM redirect callback"""
    transaction = get_object_or_404(PaymentTransaction, order_id=order_id)

    # Get response parameters from request
    response_params = (
        request.POST.dict() if request.method == "POST" else request.GET.dict()
    )

    # Verify payment with PayTM
    result = paytm_gateway.verify_callback(
        response_params, transaction.merchant_transaction_id
    )

    if result["success"]:
        if result["status"] == "TXN_SUCCESS":
            transaction.mark_success(
                phonepe_transaction_id=result.get("transaction_id"),
                phonepe_payment_id=result.get("bank_txn_id"),
            )
            messages.success(
                request,
                f"Payment successful! {transaction.get_item_name()} has been unlocked.",
            )

            # Update order if exists
            if hasattr(transaction, "order") and transaction.order:
                transaction.order.status = "paid"
                transaction.order.paid_at = timezone.now()
                transaction.order.save()
        else:
            transaction.mark_failed()
            messages.error(request, f'Payment failed: {result.get("status")}')
    else:
        messages.error(request, f'Payment verification failed: {result.get("error")}')

    return redirect(
        get_redirect_url(
            transaction.item_type, transaction.exam or transaction.mock_test
        )
    )


@login_required
def paytm_payment_status(request, order_id):
    """Check PayTM payment status via AJAX"""
    transaction = get_object_or_404(
        PaymentTransaction, order_id=order_id, user=request.user
    )

    if transaction.merchant_transaction_id:
        result = paytm_gateway.verify_payment(transaction.merchant_transaction_id)

        if result["success"]:
            if result["status"] == "TXN_SUCCESS" and transaction.status != "success":
                transaction.mark_success(
                    phonepe_transaction_id=result.get("transaction_id"),
                    phonepe_payment_id=result.get("bank_txn_id"),
                )

            return JsonResponse(
                {
                    "status": transaction.status,
                    "is_success": transaction.status == "success",
                    "transaction_id": result.get("transaction_id"),
                    "amount": result.get("amount"),
                }
            )

    return JsonResponse({"status": transaction.status, "is_success": False})


@csrf_exempt
@require_http_methods(["POST"])
def paytm_webhook(request):
    """Handle PayTM webhook for payment confirmation"""
    try:
        response_params = request.POST.dict()

        # Verify webhook signature
        if not paytm_gateway.verify_webhook_signature(response_params):
            logger.error("Invalid webhook signature")
            return JsonResponse({"error": "Invalid signature"}, status=400)

        # Extract transaction details
        order_id = response_params.get("ORDERID")
        transaction_status = response_params.get("STATUS")
        transaction_id = response_params.get("TXNID")

        # Find the transaction
        try:
            transaction = PaymentTransaction.objects.get(order_id=order_id)
        except PaymentTransaction.DoesNotExist:
            logger.error(f"Transaction not found: {order_id}")
            return JsonResponse({"error": "Transaction not found"}, status=404)

        # Mark webhook received
        transaction.webhook_received = True

        if transaction_status == "TXN_SUCCESS":
            # Double-check with PayTM API
            verify_result = paytm_gateway.verify_payment(
                transaction.merchant_transaction_id
            )

            if verify_result["success"] and verify_result["status"] == "TXN_SUCCESS":
                transaction.mark_success(
                    phonepe_transaction_id=transaction_id,
                    phonepe_payment_id=verify_result.get("bank_txn_id"),
                )
                transaction.webhook_verified = True
                transaction.save()

                logger.info(f"Payment verified successfully via webhook: {order_id}")
                return JsonResponse({"success": True, "message": "Payment verified"})
            else:
                transaction.mark_failed()
                transaction.save()
                return JsonResponse({"error": "Verification failed"}, status=400)
        else:
            transaction.mark_failed()
            transaction.save()
            return JsonResponse(
                {"error": f"Payment status: {transaction_status}"}, status=400
            )

    except Exception as e:
        logger.error(f"PayTM Webhook error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


# ==================== STATUS CHECK ====================


@login_required
def check_payment_status(request, transaction_id):
    """Check payment status via AJAX"""
    transaction = get_object_or_404(
        PaymentTransaction, id=transaction_id, user=request.user
    )

    if transaction.merchant_transaction_id:
        result = paytm_gateway.verify_payment(transaction.merchant_transaction_id)

        if result["success"]:
            if result["status"] == "TXN_SUCCESS" and transaction.status != "success":
                transaction.mark_success(
                    phonepe_transaction_id=result.get("transaction_id"),
                    phonepe_payment_id=result.get("bank_txn_id"),
                )

            return JsonResponse(
                {
                    "status": transaction.status,
                    "is_success": transaction.status == "success",
                }
            )

    return JsonResponse({"status": transaction.status, "is_success": False})


# ==================== TEST PAGE ====================


@login_required
def paytm_test(request):
    """Test PayTM integration page"""
    if request.method == "POST":
        amount = request.POST.get("amount", 100)

        # Create a test transaction
        order_id = f"TEST_{uuid.uuid4().hex[:10].upper()}"

        # Get or create a test exam
        test_exam = Exam.objects.filter(is_active=True, is_paid=True).first()

        if not test_exam:
            messages.error(request, "No test exam available. Please create one first.")
            return redirect("payments:paytm_test")

        transaction = PaymentTransaction.objects.create(
            user=request.user,
            item_type="exam",
            exam=test_exam,
            amount=float(amount),
            order_id=order_id,
            status="pending",
        )

        return redirect("payments:initiate_payment", transaction_id=transaction.id)

    context = {
        "test_credentials": {
            "card_number": "4111111111111111",
            "expiry_month": "12",
            "expiry_year": "25",
            "cvv": "123",
            "otp": "123456",
            "mobile": "7777777777",
        }
    }
    return render(request, "payments/paytm_test.html", context)


# ==================== USER PURCHASES ====================


@login_required
def my_purchases(request):
    """Show all purchases made by user"""
    exam_purchases = UnlockedExam.objects.filter(user=request.user).select_related(
        "exam"
    )
    mock_test_purchases = UnlockedMockTest.objects.filter(
        user=request.user
    ).select_related("mock_test")
    payments = PaymentTransaction.objects.filter(
        user=request.user, status="success"
    ).order_by("-created_at")

    # Get popular paid exams for recommendations (exclude already purchased)
    purchased_exam_ids = exam_purchases.values_list("exam_id", flat=True)
    popular_paid_exams = Exam.objects.filter(is_paid=True, is_active=True).exclude(
        id__in=purchased_exam_ids
    )[:3]

    context = {
        "exam_purchases": exam_purchases,
        "mock_test_purchases": mock_test_purchases,
        "payments": payments,
        "popular_paid_exams": popular_paid_exams,
    }
    return render(request, "payments/my_purchases.html", context)


# ==================== CART AND CHECKOUT ====================


@login_required
def cart_view(request):
    """Display user's cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("exam", "mock_test")
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_amount": sum(item.get_price() for item in cart_items),
    }
    return render(request, "payments/cart.html", context)


@login_required
def add_to_cart(request):
    """Add item to cart"""
    if request.method == "POST":
        item_type = request.POST.get("item_type")
        item_id = request.POST.get("item_id")

        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Check if already in cart
        existing_item = CartItem.objects.filter(
            cart=cart,
            item_type=item_type,
            exam_id=item_id if item_type == "exam" else None,
            mock_test_id=item_id if item_type == "mock_test" else None,
        ).first()

        if existing_item:
            messages.warning(request, "Item already in cart")
        else:
            if item_type == "exam":
                exam = get_object_or_404(Exam, id=item_id, is_active=True)
                CartItem.objects.create(cart=cart, item_type="exam", exam=exam)
                messages.success(request, f"Added {exam.name} to cart")
            elif item_type == "mock_test":
                mock_test = get_object_or_404(MockTest, id=item_id, is_active=True)
                CartItem.objects.create(
                    cart=cart, item_type="mock_test", mock_test=mock_test
                )
                messages.success(request, f"Added {mock_test.name} to cart")

        return redirect("payments:view_cart")

    return redirect("payments:view_cart")


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("payments:view_cart")


@login_required
def checkout_view(request):
    """Checkout page with payment method selection"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("exam", "mock_test")

    if not items:
        messages.warning(request, "Your cart is empty")
        return redirect("payments:view_cart")

    total_amount = sum(item.get_price() for item in items)

    if request.method == "POST":
        # Create order
        order_id = f"ORDER_{uuid.uuid4().hex[:12].upper()}"

        order = Order.objects.create(
            order_id=order_id,
            user=request.user,
            total_amount=total_amount,
            final_amount=total_amount,
            status="pending",
        )

        # Create order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                item_type=item.item_type,
                exam=item.exam,
                mock_test=item.mock_test,
                price=item.get_price(),
                quantity=1,
            )

        # Create transaction for first item
        first_item = items[0]
        transaction = PaymentTransaction.objects.create(
            user=request.user,
            item_type=first_item.item_type,
            exam=first_item.exam,
            mock_test=first_item.mock_test,
            amount=total_amount,
            order_id=order_id,
            status="pending",
        )

        # Store transaction reference in order
        order.payment_transaction = transaction
        order.save()

        # Clear cart
        cart.clear_cart()

        # Store order info in session
        request.session["current_order_id"] = str(order.order_id)

        # Redirect to payment initiation
        return redirect("payments:initiate_payment", transaction_id=transaction.id)

    context = {
        "cart": cart,
        "items": items,
        "total_amount": total_amount,
    }
    return render(request, "payments/checkout.html", context)


@login_required
def order_confirmation(request, order_id):
    """Show order confirmation page"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    context = {
        "order": order,
        "items": order.items.select_related("exam", "mock_test"),
    }
    return render(request, "payments/order_confirmation.html", context)


def payment_success(request):
    """Handle payment success"""
    messages.success(request, "Payment successful! Your items have been unlocked.")
    return redirect("payments:my_purchases")


def payment_failed(request):
    """Handle payment failure"""
    messages.error(request, "Payment failed. Please try again.")
    return redirect("payments:view_cart")


# ==================== ADMIN VIEWS ====================


@login_required
def admin_payments(request):
    """Admin view for managing payments"""
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect("home")

    payments = PaymentTransaction.objects.select_related(
        "user", "exam", "mock_test"
    ).order_by("-created_at")
    status_filter = request.GET.get("status", "")
    if status_filter:
        payments = payments.filter(status=status_filter)

    context = {
        "payments": payments,
        "status_filter": status_filter,
    }
    return render(request, "payments/admin_payments.html", context)


@login_required
def admin_manual_unlock(request, transaction_id):
    """Admin manually unlock content"""
    if not request.user.is_staff:
        messages.error(request, "Access denied")
        return redirect("home")

    transaction = get_object_or_404(
        PaymentTransaction.objects.select_related("user", "exam", "mock_test"),
        id=transaction_id,
    )

    if request.method == "POST":
        action = request.POST.get("action")
        admin_notes = request.POST.get("admin_notes", "")

        if action == "unlock":
            if transaction.exam:
                UnlockedExam.objects.get_or_create(
                    user=transaction.user, exam=transaction.exam
                )
            elif transaction.mock_test:
                UnlockedMockTest.objects.get_or_create(
                    user=transaction.user, mock_test=transaction.mock_test
                )

            transaction.status = "success"
            transaction.admin_notes = admin_notes
            transaction.paid_at = timezone.now()
            transaction.save()

            messages.success(request, f"Content unlocked for {transaction.user.email}")

        elif action == "reject":
            transaction.status = "failed"
            transaction.admin_notes = admin_notes
            transaction.save()
            messages.warning(request, f"Payment rejected for {transaction.user.email}")

        return redirect("payments:admin_payments")

    context = {
        "transaction": transaction,
        "item": transaction.exam or transaction.mock_test,
    }
    return render(request, "payments/admin_manual_unlock.html", context)


# ==================== HELPER FUNCTIONS ====================


def has_payment_access(user, item_type, item_id):
    """Check if user has access to paid content"""
    if not user.is_authenticated:
        return False

    if item_type == "exam":
        return UnlockedExam.objects.filter(user=user, exam_id=item_id).exists()
    elif item_type == "mock_test":
        return UnlockedMockTest.objects.filter(user=user, mock_test_id=item_id).exists()
    return False


def unlock_item(user, item_type, item):
    """Unlock item for user"""
    if item_type == "exam":
        UnlockedExam.objects.get_or_create(user=user, exam=item)
    elif item_type == "mock_test":
        UnlockedMockTest.objects.get_or_create(user=user, mock_test=item)


def get_redirect_url(item_type, item):
    """Get redirect URL after unlock"""
    if item_type == "exam":
        return f"/exams/{item.slug}/"
    elif item_type == "mock_test":
        return f"/mock-tests/{item.slug}/"
    return "/"


# ==================== CART HELPERS ====================


def get_cart_total(user):
    """Get total amount of items in user's cart"""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart.get_total_amount()


def get_cart_count(user):
    """Get number of items in user's cart"""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart.get_total_items()
