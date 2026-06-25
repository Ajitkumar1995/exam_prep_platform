from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()


class InterviewCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="fa-comments")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Interview Categories"

    def __str__(self):
        return self.name

    def question_count(self):
        """Return the number of active questions in this category"""
        return self.questions.filter(is_active=True).count()


class InterviewQuestion(models.Model):
    DIFFICULTY = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    )

    QUESTION_TYPE = (
        ("hr", "HR Interview"),
        ("technical", "Technical Interview"),
        ("behavioral", "Behavioral"),
        ("situational", "Situational"),
        ("government", "Government Interview"),
    )

    category = models.ForeignKey(
        InterviewCategory, on_delete=models.CASCADE, related_name="questions"
    )
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE)
    question_text = models.TextField()
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY, default="intermediate"
    )
    sample_answer = RichTextField()
    keywords = models.CharField(
        max_length=500, blank=True, help_text="Comma-separated keywords for evaluation"
    )
    tips = models.TextField(blank=True, help_text="Tips for answering this question")
    time_limit = models.IntegerField(default=120, help_text="Time limit in seconds")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:100]


class UserInterviewProgress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interview_progress"
    )
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField(blank=True)
    score = models.FloatField(default=0)
    feedback = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "question"]
        ordering = ["-attempted_at"]

    def __str__(self):
        return f"{self.user.email} - {self.question.question_text[:50]}"
