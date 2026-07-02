"""
Centralized cache key generation.

All cache keys MUST be generated from this class.
Never hardcode cache keys inside views or services.

Example:
    CacheKeys.exam_detail("ssc-cgl")
    CacheKeys.homepage_categories()
"""

from typing import Optional


class CacheKeys:
    """
    Generates standardized Redis cache keys.

    Format:
        govtexamwala:v1:<resource>
    """

    PREFIX = "govtexamwala"
    VERSION = "v1"

    @classmethod
    def _base(cls) -> str:
        return f"{cls.PREFIX}:{cls.VERSION}"

    @classmethod
    def make(cls, *parts) -> str:
        """
        Generic key generator.

        Example:
            CacheKeys.make("exam", "ssc-cgl")
            -> govtexamwala:v1:exam:ssc-cgl
        """
        return ":".join([cls._base(), *map(str, parts)])

    # ------------------------------------------------------------------
    # Homepage
    # ------------------------------------------------------------------

    @classmethod
    def homepage(cls):
        return cls.make("homepage")

    @classmethod
    def homepage_categories(cls):
        return cls.make("homepage", "categories")

    @classmethod
    def homepage_live_cards(cls):
        return cls.make("homepage", "live_cards")

    @classmethod
    def homepage_notifications(cls):
        return cls.make("homepage", "notifications")

    @classmethod
    def homepage_daily_challenge(cls):
        return cls.make("homepage", "daily_challenge")

    @classmethod
    def homepage_leaderboard(cls):
        return cls.make("homepage", "leaderboard")

    # ------------------------------------------------------------------
    # Exams
    # ------------------------------------------------------------------

    @classmethod
    def exam_list(cls):
        return cls.make("exam", "list")

    @classmethod
    def exam_categories(cls):
        return cls.make("exam", "categories")

    @classmethod
    def exam_detail(cls, slug):
        return cls.make("exam", slug)

    @classmethod
    def exam_mock_tests(cls, slug):
        return cls.make("exam", slug, "mock_tests")

    @classmethod
    def exam_study_material(cls, slug):
        return cls.make("exam", slug, "study_material")

    # ------------------------------------------------------------------
    # Mock Tests
    # ------------------------------------------------------------------

    @classmethod
    def mock_test_list(cls):
        return cls.make("mock_test", "list")

    @classmethod
    def mock_test_detail(cls, slug):
        return cls.make("mock_test", slug)

    @classmethod
    def mock_test_questions(cls, slug):
        return cls.make("mock_test", slug, "questions")

    # ------------------------------------------------------------------
    # Current Affairs
    # ------------------------------------------------------------------

    @classmethod
    def current_affairs_list(cls):
        return cls.make("current_affairs", "list")

    @classmethod
    def current_affair(cls, slug):
        return cls.make("current_affairs", slug)

    # ------------------------------------------------------------------
    # Study Materials
    # ------------------------------------------------------------------

    @classmethod
    def notes_list(cls):
        return cls.make("notes", "list")

    @classmethod
    def note_detail(cls, slug):
        return cls.make("note", slug)

    @classmethod
    def video_list(cls):
        return cls.make("videos", "list")

    @classmethod
    def video_detail(cls, slug):
        return cls.make("video", slug)

    @classmethod
    def ebook_list(cls):
        return cls.make("ebooks", "list")

    @classmethod
    def course_list(cls):
        return cls.make("courses", "list")

    @classmethod
    def course_detail(cls, slug):
        return cls.make("course", slug)

    # ------------------------------------------------------------------
    # Interviews
    # ------------------------------------------------------------------

    @classmethod
    def interview_home(cls):
        return cls.make("interview", "home")

    @classmethod
    def interview_questions(cls):
        return cls.make("interview", "questions")

    @classmethod
    def interview_category(cls, slug):
        return cls.make("interview", "category", slug)

    # ------------------------------------------------------------------
    # Notifications
    # ------------------------------------------------------------------

    @classmethod
    def notifications(cls):
        return cls.make("notifications")

    # ------------------------------------------------------------------
    # Leaderboard
    # ------------------------------------------------------------------

    @classmethod
    def leaderboard(cls):
        return cls.make("leaderboard")

    # ------------------------------------------------------------------
    # Daily Challenge
    # ------------------------------------------------------------------

    @classmethod
    def daily_challenge(cls):
        return cls.make("daily_challenge")

    # ------------------------------------------------------------------
    # User Specific
    # ------------------------------------------------------------------

    @classmethod
    def user_dashboard(cls, user_id):
        return cls.make("user", user_id, "dashboard")

    @classmethod
    def user_profile(cls, user_id):
        return cls.make("user", user_id, "profile")

    @classmethod
    def user_bookmarks(cls, user_id):
        return cls.make("user", user_id, "bookmarks")

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    @classmethod
    def search(cls, query):
        return cls.make("search", query.lower())

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @classmethod
    def statistics(cls):
        return cls.make("statistics")

    # ------------------------------------------------------------------
    # Cache Version
    # ------------------------------------------------------------------

    @classmethod
    def version(cls):
        return cls.VERSION