from django.db import models
from django.utils import timezone
from apps.accounts.models import User
from apps.exams.models import Exam
from apps.mocktests.models import MockTest
import uuid


class Cart(models.Model):
    """Shopping Cart for user"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return f"Cart - {self.user.email}"
        return f"Cart - {self.user.email if self.user else 'Deleted User'}"

    def get_total_amount(self):
        """Calculate total amount of all items in cart"""
        total = 0
        for item in self.items.all():
            total += item.get_price()
        return total

    def get_total_items(self):
        """Get total number of items in cart"""
        return self.items.count()

    def clear_cart(self):
        """Clear all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """Individual item in cart"""

    ITEM_TYPES = (
        ("exam", "Exam Course"),
        ("mock_test", "Mock Test"),
    )

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    mock_test = models.ForeignKey(
        MockTest, on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["cart", "item_type", "exam", "mock_test"]

    def __str__(self):
        user_email = (
            self.cart.user.email if self.cart and self.cart.user else "Deleted User"
        )
        return f"{user_email} - {self.get_item_name()}"
        # return f"{self.cart.user.email} - {self.get_item_name()}"

    def get_item_name(self):
        if self.exam:
            return self.exam.name
        elif self.mock_test:
            return self.mock_test.name
        return "Unknown"

    def get_price(self):
        if self.exam and self.exam.is_paid:
            return float(self.exam.price)
        elif self.mock_test and self.mock_test.is_paid:
            return float(self.mock_test.price)
        return 0


class Order(models.Model):
    """Order after checkout"""

    ORDER_STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    # Order Information
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    # Order Details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Status
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")

    # Payment Details
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):

        user_email = self.user.email if self.user else "Deleted User"
        return f"Order {self.order_id} - {user_email} - {self.status}"
        # return f"Order {self.order_id} - {self.user.email} - {self.status}"

    def mark_as_paid(self, payment_id, signature):
        self.status = "paid"
        self.razorpay_payment_id = payment_id
        self.razorpay_signature = signature
        self.paid_at = timezone.now()
        self.save()

        # Unlock all items in this order
        for item in self.items.all():
            if item.item_type == "exam":
                UnlockedExam.objects.get_or_create(user=self.user, exam=item.exam)
            elif item.item_type == "mock_test":
                UnlockedMockTest.objects.get_or_create(
                    user=self.user, mock_test=item.mock_test
                )


class OrderItem(models.Model):
    """Items in an order"""

    ITEM_TYPES = (
        ("exam", "Exam Course"),
        ("mock_test", "Mock Test"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    mock_test = models.ForeignKey(
        MockTest, on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.order.order_id if self.order else 'No Order'} - {self.get_item_name()}"
        # return f"{self.order.order_id} - {self.get_item_name()}"

    def get_item_name(self):
        if self.exam:
            return self.exam.name
        elif self.mock_test:
            return self.mock_test.name
        return "Unknown"


class UnlockedExam(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="unlocked_exams"
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="unlocked_by")
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "exam"]

    def __str__(self):
        return f"{self.user.email if self.user else 'Deleted User'} - {self.exam.name}"
        # return f"{self.user.email} - {self.exam.name}"


class UnlockedMockTest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="unlocked_mock_tests"
    )
    mock_test = models.ForeignKey(
        MockTest, on_delete=models.CASCADE, related_name="unlocked_by"
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "mock_test"]

    def __str__(self):
        return f"{self.user.email if self.user else 'Deleted User'} - {self.mock_test.name}"
        # return f"{self.user.email} - {self.mock_test.name}"


class PaymentTransaction(models.Model):
    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )

    # Unique order ID
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    merchant_transaction_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    item_type = models.CharField(
        max_length=20,
        choices=(
            ("exam", "Exam Course"),
            ("mock_test", "Mock Test"),
        ),
    )
    exam = models.ForeignKey(
        Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments"
    )
    mock_test = models.ForeignKey(
        MockTest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )

    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # PhonePe specific fields
    phonepe_merchant_id = models.CharField(max_length=50, blank=True, null=True)
    phonepe_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    phonepe_payment_id = models.CharField(max_length=100, blank=True, null=True)

    # QR Code
    qr_code_url = models.URLField(blank=True, null=True)
    qr_code_base64 = models.TextField(blank=True, null=True)

    # Status
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")

    # Webhook data
    webhook_received = models.BooleanField(default=False)
    webhook_verified = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    # Admin notes
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        user_email = self.user.email if self.user else "Deleted User"
        return f"{self.order_id} - {user_email} - {self.status}"
        # return f"{self.order_id} - {self.user.email} - {self.status}"

    def get_item_name(self):
        if self.exam:
            return f"Exam: {self.exam.name}"
        elif self.mock_test:
            return f"Mock Test: {self.mock_test.name}"
        return "Unknown"

    def mark_success(self, phonepe_transaction_id=None, phonepe_payment_id=None):
        """Mark payment as successful and unlock content"""
        self.status = "success"
        self.paid_at = timezone.now()
        if phonepe_transaction_id:
            self.phonepe_transaction_id = phonepe_transaction_id
        if phonepe_payment_id:
            self.phonepe_payment_id = phonepe_payment_id
        self.save()

        # Auto unlock content
        if self.exam:
            UnlockedExam.objects.get_or_create(user=self.user, exam=self.exam)
        elif self.mock_test:
            UnlockedMockTest.objects.get_or_create(
                user=self.user, mock_test=self.mock_test
            )

    def mark_failed(self):
        self.status = "failed"
        self.save()


# from django.db import models
# from django.utils import timezone
# from apps.accounts.models import User
# from apps.exams.models import Exam
# from apps.mocktests.models import MockTest
# import uuid

# class PaymentTransaction(models.Model):
#     PAYMENT_STATUS = (
#         ('pending', 'Pending'),
#         ('processing', 'Processing'),
#         ('success', 'Success'),
#         ('failed', 'Failed'),
#         ('refunded', 'Refunded'),
#     )

#     # Unique order ID
#     order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
#     merchant_transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
#     item_type = models.CharField(max_length=20, choices=(
#         ('exam', 'Exam Course'),
#         ('mock_test', 'Mock Test'),
#     ))
#     exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
#     mock_test = models.ForeignKey(MockTest, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

#     # Payment details
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     # PhonePe specific fields
#     phonepe_merchant_id = models.CharField(max_length=50, blank=True, null=True)
#     phonepe_transaction_id = models.CharField(max_length=100, blank=True, null=True)
#     phonepe_payment_id = models.CharField(max_length=100, blank=True, null=True)

#     # QR Code
#     qr_code_url = models.URLField(blank=True, null=True)
#     qr_code_base64 = models.TextField(blank=True, null=True)

#     # Status
#     status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

#     # Webhook data
#     webhook_received = models.BooleanField(default=False)
#     webhook_verified = models.BooleanField(default=False)

#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     paid_at = models.DateTimeField(null=True, blank=True)

#     # Admin notes
#     admin_notes = models.TextField(blank=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.order_id} - {self.user.email} - {self.status}"

#     def get_item_name(self):
#         if self.exam:
#             return f"Exam: {self.exam.name}"
#         elif self.mock_test:
#             return f"Mock Test: {self.mock_test.name}"
#         return "Unknown"

#     def mark_success(self, phonepe_transaction_id=None, phonepe_payment_id=None):
#         """Mark payment as successful and unlock content"""
#         self.status = 'success'
#         self.paid_at = timezone.now()
#         if phonepe_transaction_id:
#             self.phonepe_transaction_id = phonepe_transaction_id
#         if phonepe_payment_id:
#             self.phonepe_payment_id = phonepe_payment_id
#         self.save()

#         # Auto unlock content
#         if self.exam:
#             UnlockedExam.objects.get_or_create(user=self.user, exam=self.exam)
#         elif self.mock_test:
#             UnlockedMockTest.objects.get_or_create(user=self.user, mock_test=self.mock_test)

#     def mark_failed(self):
#         self.status = 'failed'
#         self.save()


# class UnlockedExam(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_exams')
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='unlocked_by')
#     unlocked_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'exam']

#     def __str__(self):
#         return f"{self.user.email} - {self.exam.name}"


# class UnlockedMockTest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_mock_tests')
#     mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='unlocked_by')
#     unlocked_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'mock_test']

#     def __str__(self):
#         return f"{self.user.email} - {self.mock_test.name}"
