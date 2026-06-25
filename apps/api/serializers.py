from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import User
from apps.exams.models import ExamCategory, Exam, Subject, Topic
from apps.mocktests.models import MockTest, TestAttempt

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "phone", "role"]
        read_only_fields = ["role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ExamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCategory
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Exam
        fields = "__all__"


class MockTestSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source="exam.name", read_only=True)

    class Meta:
        model = MockTest
        fields = "__all__"


class TestAttemptSerializer(serializers.ModelSerializer):
    mock_test_name = serializers.CharField(source="mock_test.name", read_only=True)

    class Meta:
        model = TestAttempt
        fields = [
            "id",
            "mock_test_name",
            "score",
            "percentage",
            "start_time",
            "end_time",
            "status",
        ]


class TopicPerformanceSerializer(serializers.Serializer):
    topic_name = serializers.CharField(source="topic.name")
    accuracy = serializers.FloatField()
    strength_score = serializers.FloatField()
