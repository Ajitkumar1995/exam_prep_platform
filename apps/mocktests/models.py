from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from apps.exams.models import Exam, Subject, Topic, Question

User = get_user_model()


class MockTest(models.Model):
    TEST_TYPES = (
        ("full", "Full Length Mock Test"),
        ("sectional", "Sectional Test"),
        ("topic", "Topic Wise Test"),
        ("practice", "Practice Test"),
    )

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="mock_tests")
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, blank=True
    )
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    test_type = models.CharField(max_length=20, choices=TEST_TYPES, default="full")

    description = models.TextField()
    instructions = models.TextField(blank=True)

    duration_minutes = models.IntegerField(default=60)
    total_questions = models.IntegerField(default=100)
    total_marks = models.IntegerField(default=200)
    passing_marks = models.IntegerField(default=80)

    negative_marking = models.BooleanField(default=True)
    negative_mark_value = models.FloatField(default=0.25)
    marks_per_question = models.FloatField(default=2)

    is_paid = models.BooleanField(
        default=False, help_text="If True, users need to pay to access this test"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, help_text="Price in INR"
    )

    shuffle_questions = models.BooleanField(default=True)
    shuffle_options = models.BooleanField(default=True)

    attempts_allowed = models.IntegerField(default=1)

    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.exam.name} - {self.name}"

    def get_absolute_url(self):
        return reverse("mocktests:detail", args=[self.slug])

    def get_questions(self):
        """Return test questions with related question/options loaded efficiently."""
        questions = (
            self.questions.all()
            .select_related("question", "question__subject", "question__topic")
            .prefetch_related("question__options")
        )
        if self.shuffle_questions:
            import random

            questions = list(questions)
            random.shuffle(questions)
        return questions


class MockTestQuestion(models.Model):
    mock_test = models.ForeignKey(
        MockTest, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    marks = models.FloatField(default=2)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        unique_together = ["mock_test", "question"]

    def __str__(self):
        return f"{self.mock_test.name} - Q{self.order}"


class TestAttempt(models.Model):
    STATUS_CHOICES = (
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("expired", "Expired"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="test_attempts",
    )
    session_id = models.CharField(max_length=100, blank=True, null=True)
    mock_test = models.ForeignKey(
        MockTest, on_delete=models.CASCADE, related_name="attempts"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="in_progress"
    )

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    score = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    percentile = models.FloatField(null=True, blank=True)

    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    skipped_answers = models.IntegerField(default=0)
    not_answered_count = models.IntegerField(default=0)

    total_time_taken = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status", "-end_time"]),
            models.Index(fields=["mock_test", "status"]),
            models.Index(fields=["session_id", "mock_test", "status"]),
        ]

    def __str__(self):
        """Return a readable label for registered and guest attempts."""
        if self.user:
            return f"{self.user.email} - {self.mock_test.name}"
        elif self.session_id:
            return f"Guest ({self.session_id[:8]}) - {self.mock_test.name}"
        else:
            return f"Anonymous - {self.mock_test.name}"

    def time_remaining(self):
        """Return remaining attempt time in seconds."""
        if self.end_time:
            remaining = (self.end_time - timezone.now()).total_seconds()
            return max(0, int(remaining))
        return self.mock_test.duration_minutes * 60

    def is_expired(self):
        """Return whether the attempt end time has passed."""
        if self.end_time:
            return timezone.now() > self.end_time
        return False


class TestAnswer(models.Model):
    attempt = models.ForeignKey(
        TestAttempt, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    is_skipped = models.BooleanField(default=False)
    is_marked_for_review = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0)
    time_taken = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["attempt", "question"]

    def __str__(self):
        """Return a readable label for registered and guest answers."""
        if self.attempt and self.attempt.user:
            return f"{self.attempt.user.email} - Q{self.question.id}"
        elif self.attempt and self.attempt.session_id:
            return f"Guest ({self.attempt.session_id[:8]}) - Q{self.question.id}"
        else:
            return f"Answer for Q{self.question.id}"
