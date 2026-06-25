from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from apps.exams.models import Exam
from apps.mocktests.models import MockTest
import uuid


@login_required
def add_to_cart(request, item_type, item_id):
    """Add item to cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)

    if item_type == "exam":
        item = get_object_or_404(Exam, id=item_id, is_active=True)
    elif item_type == "mock_test":
        item = get_object_or_404(MockTest, id=item_id, is_active=True)
    else:
        messages.error(request, "Invalid item type")
        return redirect("home")

    # Check if already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item_type=item_type,
        exam=item if item_type == "exam" else None,
        mock_test=item if item_type == "mock_test" else None,
    )

    if created:
        messages.success(request, f"{item.name} added to cart!")
    else:
        messages.info(request, f"{item.name} is already in your cart.")

    return redirect("payments:view_cart")


@login_required
def view_cart(request):
    """View cart page"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total_amount = 0
    for item in items:
        total_amount += item.get_price()

    context = {
        "items": items,
        "total_amount": total_amount,
        "total_items": items.count(),
    }
    return render(request, "payments/cart.html", context)


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item_name = cart_item.get_item_name()
    cart_item.delete()
    messages.success(request, f"{item_name} removed from cart.")
    return redirect("payments:view_cart")


@login_required
def checkout(request):
    """Checkout page - Review order before payment"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    if not items:
        messages.warning(request, "Your cart is empty. Please add items to checkout.")
        return redirect("payments:view_cart")

    total_amount = 0
    for item in items:
        total_amount += item.get_price()

    context = {
        "items": items,
        "total_amount": total_amount,
    }
    return render(request, "payments/checkout.html", context)


@login_required
def place_order(request):
    """Place order and create payment transaction"""
    if request.method == "POST":
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()

        if not items:
            messages.warning(request, "Your cart is empty.")
            return redirect("payments:view_cart")

        total_amount = 0
        for item in items:
            total_amount += item.get_price()

        # Create order
        order = Order.objects.create(
            user=request.user,
            order_id=str(uuid.uuid4()),
            total_amount=total_amount,
            discount_amount=0,
            final_amount=total_amount,
            status="pending",
        )

        # Create order items
        for cart_item in items:
            OrderItem.objects.create(
                order=order,
                item_type=cart_item.item_type,
                exam=cart_item.exam,
                mock_test=cart_item.mock_test,
                price=cart_item.get_price(),
                quantity=cart_item.quantity,
            )

        # Clear cart
        cart.clear_cart()

        # Store order ID in session to link payment with order
        request.session["current_order_id"] = order.id

        # Get first item for payment page
        first_item = order.items.first()

        if first_item.item_type == "exam":
            item_id = first_item.exam.id
            item_type = "exam"
        else:
            item_id = first_item.mock_test.id
            item_type = "mock_test"

        # Redirect to payment page
        return redirect("payments:payment_page", item_type=item_type, item_id=item_id)

    return redirect("payments:view_cart")


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "payments/order_confirmation.html", {"order": order})


@login_required
def my_orders(request):
    """View all user orders"""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payments/my_orders.html", {"orders": orders})
