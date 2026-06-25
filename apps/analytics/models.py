from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.exams.models import Exam, Subject, Topic
from apps.mocktests.models import MockTest

User = get_user_model()


class UserPerformance(models.Model):
    """Overall user performance tracking"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="performance"
    )
    total_tests_taken = models.IntegerField(default=0)
    total_questions_attempted = models.IntegerField(default=0)
    total_correct_answers = models.IntegerField(default=0)
    total_wrong_answers = models.IntegerField(default=0)
    total_skipped_answers = models.IntegerField(default=0)
    overall_accuracy = models.FloatField(default=0)
    average_score = models.FloatField(default=0)
    total_time_spent = models.IntegerField(default=0)  # in seconds
    rank = models.IntegerField(default=0)
    percentile = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    # New fields for gamification and engagement
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    total_xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    coins = models.IntegerField(default=0)
    badges = models.JSONField(default=list, blank=True)

    def update_stats(self):
        """Update user statistics based on all attempts"""
        from apps.mocktests.models import TestAttempt, TestAnswer

        attempts = TestAttempt.objects.filter(user=self.user, status="completed")
        self.total_tests_taken = attempts.count()

        answers = TestAnswer.objects.filter(attempt__user=self.user)
        self.total_questions_attempted = answers.count()
        self.total_correct_answers = answers.filter(is_correct=True).count()
        self.total_wrong_answers = answers.filter(
            is_correct=False, is_skipped=False
        ).count()
        self.total_skipped_answers = answers.filter(is_skipped=True).count()

        if self.total_questions_attempted > 0:
            self.overall_accuracy = (
                self.total_correct_answers / self.total_questions_attempted
            ) * 100

        self.average_score = (
            attempts.aggregate(models.Avg("percentage"))["percentage__avg"] or 0
        )
        self.total_time_spent = (
            attempts.aggregate(models.Sum("total_time_taken"))["total_time_taken__sum"]
            or 0
        )

        # Update streak
        self.update_streak()

        # Update XP and level
        self.update_xp_and_level()

        # Update rank
        self.update_rank()

        self.save()

    def update_streak(self):
        """Update user's daily streak"""
        from apps.mocktests.models import TestAttempt

        today = timezone.now().date()

        # Get all dates with test attempts
        attempt_dates = TestAttempt.objects.filter(
            user=self.user, status="completed", end_time__isnull=False
        ).dates("end_time", "day")

        if not attempt_dates:
            self.current_streak = 0
            self.last_activity_date = None
            return

        dates = sorted(attempt_dates)

        # Check if today has activity
        has_activity_today = today in dates

        if has_activity_today:
            streak = 1
            current_date = today - timedelta(days=1)
            while current_date in dates:
                streak += 1
                current_date -= timedelta(days=1)
            self.current_streak = streak
            self.last_activity_date = today
        else:
            yesterday = today - timedelta(days=1)
            if yesterday in dates:
                streak = 1
                current_date = yesterday - timedelta(days=1)
                while current_date in dates:
                    streak += 1
                    current_date -= timedelta(days=1)
                self.current_streak = streak
                self.last_activity_date = yesterday
            else:
                self.current_streak = 0

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

    def update_xp_and_level(self):
        """Update XP and level based on activity"""
        xp_from_questions = self.total_questions_attempted * 10
        xp_from_correct = self.total_correct_answers * 5
        xp_from_streak = self.current_streak * 20
        xp_from_tests = self.total_tests_taken * 50

        self.total_xp = (
            xp_from_questions + xp_from_correct + xp_from_streak + xp_from_tests
        )
        self.level = max(1, self.total_xp // 1000 + 1)
        self.coins = self.total_xp // 10

    def update_rank(self):
        """Update user's rank and percentile"""
        from apps.mocktests.models import TestAttempt

        all_users = User.objects.filter(test_attempts__status="completed").distinct()

        user_scores = {}
        for user in all_users:
            avg_score = (
                TestAttempt.objects.filter(user=user, status="completed").aggregate(
                    avg=models.Avg("percentage")
                )["avg"]
                or 0
            )
            user_scores[user.id] = avg_score

        sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)

        for idx, (user_id, score) in enumerate(sorted_users, 1):
            if user_id == self.user.id:
                self.rank = idx
                self.percentile = (
                    ((len(sorted_users) - idx) / len(sorted_users)) * 100
                    if sorted_users
                    else 0
                )
                break

        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.overall_accuracy:.1f}%"


class ExamPerformance(models.Model):
    """User performance for specific exam"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="exam_performances"
    )
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="user_performances"
    )
    total_attempts = models.IntegerField(default=0)
    total_correct = models.IntegerField(default=0)
    total_wrong = models.IntegerField(default=0)
    total_skipped = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    average_score = models.FloatField(default=0)
    best_score = models.FloatField(default=0)
    last_attempt_date = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "exam"]

    def update_stats(self):
        from apps.mocktests.models import TestAttempt, TestAnswer

        attempts = TestAttempt.objects.filter(
            user=self.user, mock_test__exam=self.exam, status="completed"
        )

        self.total_attempts = attempts.count()

        answers = TestAnswer.objects.filter(
            attempt__user=self.user, attempt__mock_test__exam=self.exam
        )

        self.total_correct = answers.filter(is_correct=True).count()
        self.total_wrong = answers.filter(is_correct=False, is_skipped=False).count()
        self.total_skipped = answers.filter(is_skipped=True).count()

        total_answered = self.total_correct + self.total_wrong
        if total_answered > 0:
            self.accuracy = (self.total_correct / total_answered) * 100

        self.average_score = (
            attempts.aggregate(models.Avg("percentage"))["percentage__avg"] or 0
        )
        self.best_score = (
            attempts.aggregate(models.Max("percentage"))["percentage__max"] or 0
        )

        last_attempt = attempts.order_by("-end_time").first()
        if last_attempt:
            self.last_attempt_date = last_attempt.end_time

        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.exam.name} - {self.accuracy:.1f}%"


class SubjectPerformance(models.Model):
    """User performance for specific subject"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subject_performances"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="user_performances"
    )
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    average_time = models.FloatField(default=0)  # in seconds
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "subject"]

    def update_stats(self):
        from apps.mocktests.models import TestAnswer

        answers = TestAnswer.objects.filter(
            attempt__user=self.user, question__subject=self.subject
        )

        self.total_questions = answers.count()
        self.correct_answers = answers.filter(is_correct=True).count()
        self.wrong_answers = answers.filter(is_correct=False, is_skipped=False).count()

        if self.total_questions > 0:
            self.accuracy = (self.correct_answers / self.total_questions) * 100

        self.average_time = (
            answers.aggregate(models.Avg("time_taken"))["time_taken__avg"] or 0
        )

        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.subject.name} - {self.accuracy:.1f}%"


class TopicPerformance(models.Model):
    """User performance for specific topic"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="topic_performances"
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="user_performances"
    )
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    average_time = models.FloatField(default=0)
    is_weak = models.BooleanField(default=False)
    is_strong = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "topic"]
        ordering = ["-accuracy"]

    def update_stats(self):
        from apps.mocktests.models import TestAnswer

        answers = TestAnswer.objects.filter(
            attempt__user=self.user, question__topic=self.topic
        )

        self.total_questions = answers.count()
        self.correct_answers = answers.filter(is_correct=True).count()
        self.wrong_answers = answers.filter(is_correct=False, is_skipped=False).count()

        if self.total_questions > 0:
            self.accuracy = (self.correct_answers / self.total_questions) * 100
            self.is_weak = self.accuracy < 50
            self.is_strong = self.accuracy > 75

        self.average_time = (
            answers.aggregate(models.Avg("time_taken"))["time_taken__avg"] or 0
        )

        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.topic.name} - {self.accuracy:.1f}%"


class DailyActivity(models.Model):
    """Track daily user activity"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="daily_activities"
    )
    date = models.DateField()
    tests_taken = models.IntegerField(default=0)
    questions_attempted = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)  # in seconds
    streak = models.IntegerField(default=0)

    class Meta:
        unique_together = ["user", "date"]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.tests_taken} tests"


# from django.db import models
# from django.contrib.auth import get_user_model
# from apps.exams.models import Exam, Subject, Topic
# from apps.mocktests.models import MockTest

# User = get_user_model()

# class UserPerformance(models.Model):
#     """Overall user performance tracking"""
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='performance')
#     total_tests_taken = models.IntegerField(default=0)
#     total_questions_attempted = models.IntegerField(default=0)
#     total_correct_answers = models.IntegerField(default=0)
#     total_wrong_answers = models.IntegerField(default=0)
#     total_skipped_answers = models.IntegerField(default=0)
#     overall_accuracy = models.FloatField(default=0)
#     average_score = models.FloatField(default=0)
#     total_time_spent = models.IntegerField(default=0)  # in seconds
#     rank = models.IntegerField(default=0)
#     percentile = models.FloatField(default=0)
#     last_updated = models.DateTimeField(auto_now=True)
#     current_streak = models.IntegerField(default=0)  # Add this
#     longest_streak = models.IntegerField(default=0)  # Add this
#     last_activity_date = models.DateField(null=True, blank=True)  # Add this
#     total_xp = models.IntegerField(default=0)  # Add this
#     level = models.IntegerField(default=1)  # Add this
#     coins = models.IntegerField(default=0)  # Add this
#     badges = models.JSONField(default=list, blank=True)  # Add this

#     def update_stats(self):
#         """Update user statistics based on all attempts"""
#         from apps.mocktests.models import TestAttempt, TestAnswer

#         attempts = TestAttempt.objects.filter(user=self.user, status='completed')
#         self.total_tests_taken = attempts.count()

#         answers = TestAnswer.objects.filter(attempt__user=self.user)
#         self.total_questions_attempted = answers.count()
#         self.total_correct_answers = answers.filter(is_correct=True).count()
#         self.total_wrong_answers = answers.filter(is_correct=False, is_skipped=False).count()
#         self.total_skipped_answers = answers.filter(is_skipped=True).count()

#         if self.total_questions_attempted > 0:
#             self.overall_accuracy = (self.total_correct_answers / self.total_questions_attempted) * 100

#         self.average_score = attempts.aggregate(models.Avg('percentage'))['percentage__avg'] or 0
#         self.total_time_spent = attempts.aggregate(models.Sum('total_time_taken'))['total_time_taken__sum'] or 0

#         self.save()

#     def __str__(self):
#         return f"{self.user.email} - {self.overall_accuracy:.1f}%"


# class ExamPerformance(models.Model):
#     """User performance for specific exam"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_performances')
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='user_performances')
#     total_attempts = models.IntegerField(default=0)
#     total_correct = models.IntegerField(default=0)
#     total_wrong = models.IntegerField(default=0)
#     total_skipped = models.IntegerField(default=0)
#     accuracy = models.FloatField(default=0)
#     average_score = models.FloatField(default=0)
#     best_score = models.FloatField(default=0)
#     last_attempt_date = models.DateTimeField(null=True, blank=True)
#     last_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ['user', 'exam']

#     def update_stats(self):
#         from apps.mocktests.models import TestAttempt, TestAnswer

#         attempts = TestAttempt.objects.filter(
#             user=self.user,
#             mock_test__exam=self.exam,
#             status='completed'
#         )

#         self.total_attempts = attempts.count()

#         answers = TestAnswer.objects.filter(
#             attempt__user=self.user,
#             attempt__mock_test__exam=self.exam
#         )

#         self.total_correct = answers.filter(is_correct=True).count()
#         self.total_wrong = answers.filter(is_correct=False, is_skipped=False).count()
#         self.total_skipped = answers.filter(is_skipped=True).count()

#         total_answered = self.total_correct + self.total_wrong
#         if total_answered > 0:
#             self.accuracy = (self.total_correct / total_answered) * 100

#         self.average_score = attempts.aggregate(models.Avg('percentage'))['percentage__avg'] or 0
#         self.best_score = attempts.aggregate(models.Max('percentage'))['percentage__max'] or 0

#         last_attempt = attempts.order_by('-end_time').first()
#         if last_attempt:
#             self.last_attempt_date = last_attempt.end_time

#         self.save()

#     def __str__(self):
#         return f"{self.user.email} - {self.exam.name} - {self.accuracy:.1f}%"


# class SubjectPerformance(models.Model):
#     """User performance for specific subject"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_performances')
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='user_performances')
#     total_questions = models.IntegerField(default=0)
#     correct_answers = models.IntegerField(default=0)
#     wrong_answers = models.IntegerField(default=0)
#     accuracy = models.FloatField(default=0)
#     average_time = models.FloatField(default=0)  # in seconds
#     last_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ['user', 'subject']

#     def update_stats(self):
#         from apps.mocktests.models import TestAnswer

#         answers = TestAnswer.objects.filter(
#             attempt__user=self.user,
#             question__subject=self.subject
#         )

#         self.total_questions = answers.count()
#         self.correct_answers = answers.filter(is_correct=True).count()
#         self.wrong_answers = answers.filter(is_correct=False, is_skipped=False).count()

#         if self.total_questions > 0:
#             self.accuracy = (self.correct_answers / self.total_questions) * 100

#         self.average_time = answers.aggregate(models.Avg('time_taken'))['time_taken__avg'] or 0

#         self.save()

#     def __str__(self):
#         return f"{self.user.email} - {self.subject.name} - {self.accuracy:.1f}%"


# class TopicPerformance(models.Model):
#     """User performance for specific topic"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_performances')
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_performances')
#     total_questions = models.IntegerField(default=0)
#     correct_answers = models.IntegerField(default=0)
#     wrong_answers = models.IntegerField(default=0)
#     accuracy = models.FloatField(default=0)
#     average_time = models.FloatField(default=0)
#     is_weak = models.BooleanField(default=False)
#     is_strong = models.BooleanField(default=False)
#     last_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ['user', 'topic']
#         ordering = ['-accuracy']

#     def update_stats(self):
#         from apps.mocktests.models import TestAnswer

#         answers = TestAnswer.objects.filter(
#             attempt__user=self.user,
#             question__topic=self.topic
#         )

#         self.total_questions = answers.count()
#         self.correct_answers = answers.filter(is_correct=True).count()
#         self.wrong_answers = answers.filter(is_correct=False, is_skipped=False).count()

#         if self.total_questions > 0:
#             self.accuracy = (self.correct_answers / self.total_questions) * 100
#             self.is_weak = self.accuracy < 50
#             self.is_strong = self.accuracy > 75

#         self.average_time = answers.aggregate(models.Avg('time_taken'))['time_taken__avg'] or 0

#         self.save()

#     def __str__(self):
#         return f"{self.user.email} - {self.topic.name} - {self.accuracy:.1f}%"


# class DailyActivity(models.Model):
#     """Track daily user activity"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_activities')
#     date = models.DateField()
#     tests_taken = models.IntegerField(default=0)
#     questions_attempted = models.IntegerField(default=0)
#     correct_answers = models.IntegerField(default=0)
#     wrong_answers = models.IntegerField(default=0)
#     time_spent = models.IntegerField(default=0)  # in seconds
#     streak = models.IntegerField(default=0)

#     class Meta:
#         unique_together = ['user', 'date']
#         ordering = ['-date']

#     def __str__(self):
#         return f"{self.user.email} - {self.date} - {self.tests_taken} tests"
