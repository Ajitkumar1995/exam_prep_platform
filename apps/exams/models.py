from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class LiveTestCard(models.Model):
    """Live test cards displayed on homepage"""

    exam = models.ForeignKey(
        "Exam",
        on_delete=models.CASCADE,
        related_name="live_cards",
        null=True,
        blank=True,
    )

    # Card Content
    title = models.CharField(max_length=200)
    subtitle = models.CharField(
        max_length=200, blank=True, help_text="e.g., Mega Mock Test, Live Quiz, etc."
    )
    badge_text = models.CharField(
        max_length=50,
        default="Live Now",
        help_text="e.g., 🔥 Live Now, ⚡ Starting Soon",
    )
    badge_color = models.CharField(
        max_length=20, default="yellow", help_text="yellow, red, green, blue, purple"
    )

    # Statistics
    total_participants = models.IntegerField(default=0)
    enrolled_percentage = models.IntegerField(
        default=0, help_text="Percentage of seats filled (0-100)"
    )

    # Timer Settings
    has_timer = models.BooleanField(default=True)
    timer_hours = models.IntegerField(default=0)
    timer_minutes = models.IntegerField(default=15)
    timer_seconds = models.IntegerField(default=30)

    # Link
    button_text = models.CharField(max_length=100, default="Join Live Test Now →")
    button_url = models.URLField(blank=True, help_text="URL when button is clicked")

    # Display Settings
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False, help_text="Show in featured position"
    )

    # Schedule
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.subtitle}"

    def get_badge_color_class(self):
        colors = {
            "yellow": "bg-yellow-400/20 text-yellow-300",
            "red": "bg-red-400/20 text-red-300",
            "green": "bg-green-400/20 text-green-300",
            "blue": "bg-blue-400/20 text-blue-300",
            "purple": "bg-purple-400/20 text-purple-300",
            "orange": "bg-orange-400/20 text-orange-300",
            "pink": "bg-pink-400/20 text-pink-300",
        }
        return colors.get(self.badge_color, "bg-yellow-400/20 text-yellow-300")

    def get_progress_percentage(self):
        return self.enrolled_percentage

    def get_circumference_offset(self):
        circumference = 339.292
        percentage = self.enrolled_percentage
        return circumference - (percentage / 100) * circumference


class ExamCategory(models.Model):
    """Main category like Banking, SSC, Railway, UPSC, etc."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(
        max_length=50, default="fa-university", help_text="Font Awesome icon class"
    )
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Exam Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("exams:category_detail", args=[self.slug])

    def total_exams(self):
        return self.exams.filter(is_active=True).count()


class Exam(models.Model):
    """Specific exam like SBI PO, IBPS Clerk, SSC CGL, etc."""

    EXAM_LEVEL = (
        ("national", "National Level"),
        ("state", "State Level"),
        ("bank", "Bank Level"),
        ("other", "Other"),
    )

    category = models.ForeignKey(
        ExamCategory, on_delete=models.CASCADE, related_name="exams"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_name = models.CharField(
        max_length=50, blank=True, help_text="e.g., SBI PO, IBPS Clerk"
    )
    exam_level = models.CharField(max_length=20, choices=EXAM_LEVEL, default="national")
    description = RichTextField()
    eligibility = RichTextField(blank=True)
    exam_pattern = RichTextField(blank=True)
    syllabus = RichTextField(blank=True)
    important_dates = models.TextField(
        blank=True, help_text="JSON format for important dates"
    )
    official_website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="exam_logos/", null=True, blank=True)
    duration_minutes = models.IntegerField(default=180)
    total_marks = models.IntegerField(default=600)
    total_questions = models.IntegerField(default=100)
    negative_marking = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(
        default=False, help_text="If True, users need to pay to access this exam"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, help_text="Price in INR"
    )
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def get_absolute_url(self):
        return reverse("exams:detail", args=[self.slug])

    def total_subjects(self):
        return self.subjects.filter(is_active=True).count()

    def total_questions_count(self):
        return self.questions.filter(is_active=True).count()


class Subject(models.Model):
    """Subject within an exam e.g., Quantitative Aptitude, Reasoning, English"""

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    weightage = models.FloatField(default=0, help_text="Percentage weightage in exam")
    total_questions = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.exam.name} - {self.name}"

    def total_topics(self):
        return self.topics.filter(is_active=True).count()


class Topic(models.Model):
    """Topic within a subject e.g., Percentage, Time & Work, Algebra"""

    DIFFICULTY = (
        ("beginner", "Beginner"),
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("expert", "Expert"),
    )

    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="topics"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY, default="medium"
    )
    weightage = models.FloatField(
        default=0, help_text="Percentage weightage in subject"
    )
    total_questions = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class Question(models.Model):
    QUESTION_TYPE = (
        ("mcq", "Multiple Choice - Single Answer"),
        ("multiple_correct", "Multiple Choice - Multiple Answers"),
        ("numerical", "Numerical Value"),
        ("true_false", "True/False"),
        ("match", "Match the Following"),
        ("passage", "Passage Based"),
    )

    DIFFICULTY = (
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("expert", "Expert"),
    )

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="questions"
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="questions", null=True, blank=True
    )
    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPE, default="mcq"
    )
    question_text = RichTextField()
    question_text_hindi = RichTextField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default="medium")
    marks = models.FloatField(default=1)
    negative_marks = models.FloatField(default=0)
    estimated_time = models.IntegerField(default=60, help_text="Time in seconds")
    explanation = RichTextField(blank=True, help_text="Explanation for the answer")
    explanation_hindi = RichTextField(blank=True)
    image = models.ImageField(upload_to="questions/", null=True, blank=True)
    tags = models.CharField(
        max_length=500, blank=True, help_text="Comma separated tags"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.exam.name} - {self.question_text[:50]}"


class Option(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    option_text = models.TextField()
    option_text_hindi = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Option for {self.question.question_text[:30]}"


class ExamAnnouncement(models.Model):
    """Exam announcements and notifications"""

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="announcements"
    )
    title = models.CharField(max_length=200)
    content = RichTextField()
    announcement_date = models.DateTimeField()
    is_important = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-announcement_date"]

    def __str__(self):
        return self.title


class ExamFaq(models.Model):
    """Frequently asked questions about exam"""

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=300)
    answer = RichTextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


class StudyMaterial(models.Model):
    """Study material for specific exam"""

    MATERIAL_TYPE = (
        ("notes", "Notes"),
        ("video", "Video Lecture"),
        ("pdf", "PDF Document"),
        ("ebook", "E-Book"),
    )

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="study_materials"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="study_materials",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE)
    description = RichTextField()
    file = models.FileField(upload_to="study_materials/", null=True, blank=True)
    video_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True, help_text="For videos")
    downloads = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    is_free = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ============================================
# DAILY CHALLENGE MODELS
# ============================================


class DailyChallenge(models.Model):
    """Dynamic daily challenges - Admin controlled"""

    DIFFICULTY = (
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("expert", "Expert"),
    )

    CHALLENGE_TYPE = (
        ("quiz", "Quiz"),
        ("mock_test", "Mock Test"),
        ("practice", "Practice Set"),
        ("puzzle", "Puzzle"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    challenge_type = models.CharField(
        max_length=20, choices=CHALLENGE_TYPE, default="quiz"
    )
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY, default="medium")

    # Challenge details
    total_questions = models.IntegerField(default=10)
    duration_minutes = models.IntegerField(default=15)
    xp_reward = models.IntegerField(default=500)
    coin_reward = models.IntegerField(default=100)

    # Link to test
    test_url = models.URLField(blank=True, help_text="URL to the challenge test")
    mock_test = models.ForeignKey(
        "mocktests.MockTest", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Schedule
    challenge_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Statistics
    total_participants = models.IntegerField(default=0)
    total_completed = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-challenge_date", "-is_featured"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.challenge_date} - {self.title}"

    def get_completion_percentage(self):
        if self.total_participants > 0:
            return (self.total_completed / self.total_participants) * 100
        return 0


class ChallengeParticipant(models.Model):
    """Track user participation in daily challenges"""

    challenge = models.ForeignKey(
        DailyChallenge, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="challenge_participations",
    )
    score = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    time_taken = models.IntegerField(default=0, help_text="Time in seconds")
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    xp_earned = models.IntegerField(default=0)
    coins_earned = models.IntegerField(default=0)

    class Meta:
        unique_together = ["challenge", "user"]
        ordering = ["-score", "time_taken"]

    def __str__(self):
        return f"{self.user.email} - {self.challenge.title} - {self.score}%"


class LeaderboardEntry(models.Model):
    """Dynamic leaderboard based on exam performance"""

    PERIOD = (
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("all_time", "All Time"),
        ("exam_wise", "Exam Wise"),
    )

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="leaderboard_entries"
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="leaderboard_entries",
    )
    challenge = models.ForeignKey(
        DailyChallenge,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="leaderboard_entries",
    )

    period = models.CharField(max_length=20, choices=PERIOD)
    score = models.FloatField(default=0)
    rank = models.IntegerField()
    accuracy = models.FloatField(default=0)
    total_tests = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["rank"]
        indexes = [
            models.Index(fields=["period", "-score"]),
            models.Index(fields=["exam", "period"]),
        ]

    def __str__(self):
        return f"{self.user.email} - Rank {self.rank} - {self.period}"
