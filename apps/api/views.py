from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models

# Import from correct apps
from apps.accounts.models import User
from apps.exams.models import ExamCategory, Exam
from apps.mocktests.models import MockTest, TestAttempt, TestAnswer

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ExamCategorySerializer,
    ExamSerializer,
    MockTestSerializer,
    TestAttemptSerializer,
)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "user": UserSerializer(user).data,
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }
                )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ExamCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExamCategory.objects.filter(is_active=True)
    serializer_class = ExamCategorySerializer
    permission_classes = [AllowAny]


class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]


class MockTestViewSet(viewsets.ModelViewSet):
    queryset = MockTest.objects.filter(is_active=True).select_related(
        "exam", "subject", "topic"
    )
    serializer_class = MockTestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        mock_test = self.get_object()

        attempt = TestAttempt.objects.filter(
            user=request.user, mock_test=mock_test, status="in_progress"
        ).first()

        if not attempt:
            attempt = TestAttempt.objects.create(
                user=request.user, mock_test=mock_test, start_time=timezone.now()
            )

        return Response(
            {
                "attempt_id": attempt.id,
                "mock_test": MockTestSerializer(mock_test).data,
                "start_time": attempt.start_time,
                "duration_minutes": mock_test.duration_minutes,
            }
        )

    @action(detail=False, methods=["post"])
    def submit_answer(self, request):
        attempt_id = request.data.get("attempt_id")
        question_id = request.data.get("question_id")
        selected_option = request.data.get("selected_option")
        time_taken = request.data.get("time_taken", 0)

        attempt = get_object_or_404(
            TestAttempt.objects.select_related("mock_test"),
            id=attempt_id,
            user=request.user,
        )

        answer, created = TestAnswer.objects.get_or_create(
            attempt=attempt,
            question_id=question_id,
            defaults={"selected_option": selected_option, "time_taken": time_taken},
        )

        if not created:
            answer.selected_option = selected_option
            answer.time_taken = time_taken
            answer.save()

        return Response({"message": "Answer saved successfully"})

    @action(detail=False, methods=["post"])
    def complete(self, request):
        attempt_id = request.data.get("attempt_id")
        attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)

        attempt.status = "completed"
        attempt.end_time = timezone.now()

        answers = list(
            TestAnswer.objects.filter(attempt=attempt)
            .select_related("question")
            .prefetch_related("question__options")
        )
        total_score = 0
        correct_count = 0

        for answer in answers:
            question = answer.question
            if answer.selected_option:
                is_correct = any(
                    option.is_correct and str(option.id) == str(answer.selected_option)
                    for option in question.options.all()
                )
                if is_correct:
                    total_score += question.marks
                    correct_count += 1
                else:
                    total_score -= question.negative_marks

        attempt.score = total_score
        attempt.percentage = (
            (total_score / attempt.mock_test.total_marks) * 100
            if attempt.mock_test.total_marks > 0
            else 0
        )
        attempt.save()

        return Response(
            {
                "score": attempt.score,
                "percentage": attempt.percentage,
                "correct_answers": correct_count,
                "total_questions": len(answers),
            }
        )


class AnalyticsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        recent_attempts = TestAttempt.objects.filter(
            user=request.user, status="completed"
        ).select_related("mock_test", "mock_test__exam").order_by("-end_time")[:5]

        return Response(
            {
                "total_tests_taken": TestAttempt.objects.filter(
                    user=request.user, status="completed"
                ).count(),
                "recent_attempts": TestAttemptSerializer(
                    recent_attempts, many=True
                ).data,
            }
        )
