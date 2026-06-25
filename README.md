# 📚 GovtExamWala - Exam Preparation Platform

A comprehensive Django-based exam preparation platform designed for government job aspirants. This platform provides mock tests, study materials, daily challenges, interview preparation, and payment integration for premium content.

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [🛠 Technology Stack](#-technology-stack)
- [📁 Project Structure](#-project-structure)
- [💻 Installation](#-installation)
- [⚙️ Configuration](#-configuration)
- [🗄️ Database Setup](#-database-setup)
- [🚀 Running the Application](#-running-the-application)
- [📚 Features in Detail](#-features-in-detail)
- [💳 Payment Integration](#-payment-integration)
- [📧 Email Configuration](#-email-configuration)
- [🎨 Admin Panel](#-admin-panel)
- [🧪 Testing](#-testing)
- [🚢 Deployment](#-deployment)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📞 Support](#-support)

---

## ✨ Features

### 👤 User Management
- ✅ User registration with email/username and password
- ✅ OTP-based authentication (passwordless login)
- ✅ Email verification
- ✅ Forgot password with reset link
- ✅ User profile management
- ✅ Role-based access (Admin, Student)

### 📖 Exam Management
- ✅ Exam categories (Banking, SSC, Railway, UPSC)
- ✅ Exam creation with detailed information
- ✅ Subject and topic management
- ✅ Question bank with multiple question types
- ✅ Difficulty levels (Easy, Medium, Hard, Advanced)
- ✅ Rich text questions with images
- ✅ MCQ options with correct answer marking
- ✅ Negative marking system

### 🎯 Mock Tests
- ✅ Create mock tests with selected questions
- ✅ Timer-based tests
- ✅ Attempt tracking
- ✅ Score calculation with percentage
- ✅ Performance analytics
- ✅ Leaderboard functionality
- ✅ Section-wise mock tests
- ✅ Paid and free mock tests

### 📄 Study Materials
- ✅ Notes and PDF uploads
- ✅ Video lectures
- ✅ eBooks
- ✅ Course structure with sections
- ✅ Current affairs
- ✅ Bookmarking feature
- ✅ Progress tracking

### ⭐ Daily Challenges
- ✅ Daily quiz challenges
- ✅ XP and coin rewards
- ✅ Leaderboard
- ✅ Streak tracking

### 💼 Interview Preparation
- ✅ Interview categories
- ✅ Common interview questions
- ✅ Sample answers
- ✅ Keywords and tips
- ✅ Time-limited practice
- ✅ Progress tracking

### 💳 Payment Integration
- ✅ PayTM payment gateway
- ✅ Shopping cart
- ✅ Order management
- ✅ Unlock premium content
- ✅ Payment history
- ✅ QR code payments

### 📊 Analytics & Reporting
- ✅ User performance tracking
- ✅ Exam performance analytics
- ✅ Subject-wise performance
- ✅ Topic-wise strength/weakness analysis
- ✅ Daily activity tracking
- ✅ Progress reports

### 🔔 Notifications
- ✅ In-app notifications
- ✅ Announcements
- ✅ Email notifications
- ✅ Click and view tracking

### 🎨 Admin Panel
- ✅ Colorful, modern admin interface
- ✅ Complete CRUD operations
- ✅ User management
- ✅ Content management
- ✅ Payment management
- ✅ Analytics dashboard

---

## 🛠 Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | Core programming language |
| Django | 4.2 | Web framework |
| Django REST Framework | 3.14 | API development |
| Celery | 5.3 | Task queue for async operations |
| Redis | 7.0 | Cache and message broker |
| SQLite/PostgreSQL | - | Database |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| HTML5 | - | Structure |
| CSS3 | - | Styling |
| Tailwind CSS | 3.4 | Utility-first CSS framework |
| JavaScript | ES6 | Interactivity |
| Font Awesome | 6.5 | Icons |
| Chart.js | 4.4 | Charts for analytics |

### Libraries & Tools
| Library | Purpose |
|---------|---------|
| django-allauth | Social authentication |
| django-cors-headers | CORS handling |
| django-ckeditor | Rich text editing |
| django-import-export | Data import/export |
| django-filter | Filtering |
| simple-jwt | JWT authentication |
| whitenoise | Static file serving |
| django-celery-beat | Scheduled tasks |
| djangorestframework-simplejwt | JWT for REST API |

---

## 📁 Project Structure

```
govt_exam_platform/
├── apps/                    # All applications
│   ├── accounts/                    # User authentication
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── forms.py                  # Form definitions
│   │   ├── models.py                 # Database models
│   │   ├── urls.py                   # URL routing
│   │   ├── utils.py                  # Utility functions
│   │   └── views.py                  # Views and logic
│   ├── analytics/                    # Analytics
│   │   ├── templatetags/
│   │   │   ├── __init__.py               # Python package marker
│   │   │   └── analytics_filters.py
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── signals.py                # Django signals
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   ├── api/                    # REST API
│   │   ├── __init__.py               # Python package marker
│   │   ├── apps.py                   # App configuration
│   │   ├── serializers.py            # DRF serializers
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   ├── contact/
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   ├── exams/                    # Exam management
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   ├── interviews/                    # Interview preparation
│   │   ├── templatetags/
│   │   │   ├── __init__.py               # Python package marker
│   │   │   └── interview_extras.py
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   ├── mocktests/                    # Mock test management
│   │   ├── templatetags/
│   │   │   ├── __init__.py               # Python package marker
│   │   │   └── mocktest_filters.py
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   ├── notifications/                    # Notifications
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   ├── payments/                    # Payment processing
│   │   ├── __init__.py               # Python package marker
│   │   ├── admin.py                  # Admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── cart_views.py
│   │   ├── models.py                 # Database models
│   │   ├── paytm_config.py
│   │   ├── paytm_utils.py            # PayTM integration
│   │   ├── phonepe_utils.py
│   │   ├── services_paytm.py
│   │   ├── tests.py                  # Test cases
│   │   ├── urls.py                   # URL routing
│   │   └── views.py                  # Views and logic
│   └── study_materials/                    # Study material uploads
│       ├── templatetags/
│       │   └── study_extras.py
│       ├── __init__.py               # Python package marker
│       ├── admin.py                  # Admin configuration
│       ├── apps.py                   # App configuration
│       ├── models.py                 # Database models
│       ├── urls.py                   # URL routing
│       └── views.py                  # Views and logic
├── exam_prep/                    # Project configuration
│   ├── __init__.py               # Python package marker
│   ├── asgi.py                   # ASGI entry point
│   ├── celery.py                 # Celery configuration
│   ├── local_settings.py
│   ├── settings.py               # Django settings
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI entry point
├── static/                    # Static files
│   ├── admin/                    # Admin templates/CSS
│   │   └── css/                    # CSS stylesheets
│   │       └── custom_admin.css
│   ├── css/                    # CSS stylesheets
│   ├── images/                    # Image files
│   ├── js/                    # JavaScript files
│   │   └── homepage.js
│   └── vendor/
├── templates/                    # HTML templates
│   ├── accounts/                    # User authentication
│   │   ├── change_password.html
│   │   ├── dashboard.html
│   │   ├── forgot_password.html
│   │   ├── login_signup.html
│   │   ├── password_reset_form.html
│   │   ├── profile.html
│   │   ├── reset_password.html
│   │   ├── set_password.html
│   │   └── verify_otp.html
│   ├── admin/                    # Admin templates/CSS
│   │   ├── base_site.html
│   │   ├── index.html
│   │   └── login.html
│   ├── analytics/                    # Analytics
│   │   └── dashboard.html
│   ├── contact/
│   │   └── contact_us.html
│   ├── dashboard/
│   ├── exams/                    # Exam management
│   │   ├── categories.html
│   │   ├── category_detail.html
│   │   ├── exam_coaching.html
│   │   ├── exam_detail.html
│   │   ├── exam_mock_tests.html
│   │   └── list.html
│   ├── interviews/                    # Interview preparation
│   │   ├── category_questions.html
│   │   ├── home.html
│   │   ├── mock_interview.html
│   │   ├── mock_results.html
│   │   ├── practice.html
│   │   ├── progress.html
│   │   ├── question_bank.html
│   │   └── tips.html
│   ├── mocktests/                    # Mock test management
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── detail.html
│   │   ├── list.html
│   │   ├── results.html
│   │   └── test_window.html
│   ├── notifications/                    # Notifications
│   │   ├── list.html
│   │   └── preferences.html
│   ├── payments/                    # Payment processing
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── my_orders.html
│   │   ├── my_purchases.html
│   │   ├── order_confirmation.html
│   │   ├── payment_page.html
│   │   ├── paytm_checkout.html
│   │   ├── paytm_redirect.html
│   │   ├── paytm_test.html
│   │   ├── qr_payment.html
│   │   └── verify_payment.html
│   ├── study_materials/                    # Study material uploads
│   │   ├── bookmarks.html
│   │   ├── course_list.html
│   │   ├── current_affair_detail.html
│   │   ├── current_affairs_list.html
│   │   ├── ebook_list.html
│   │   ├── home.html
│   │   ├── my_courses.html
│   │   ├── note_detail.html
│   │   ├── note_list.html
│   │   ├── video_detail.html
│   │   └── video_list.html
│   ├── about.html
│   ├── base.html
│   ├── faq.html
│   ├── index.html
│   └── privacy_policy.html
├── Dockerfile             # Docker configuration
├── README.md             # Project documentation
├── create_all_current_affairs_mock_tests.py
├── create_current_affairs_mock_test_1_to_100.py
├── docker-compose.yml             # Docker compose configuration
├── generate_structure.py
├── manage.py             # Django management script
├── nginx.conf
├── requirements.txt             # Python dependencies
├── schema_export_20260625_122749.json
├── schema_markdown_20260625_122749.md
└── schema_summary_20260625_122749.txt
```

---

## 💻 Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Redis (for Celery)
- Node.js (for Tailwind CSS compilation)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/govt-exam-platform.git
cd govt-exam-platform
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.0
django-allauth==0.57.0
django-ckeditor==6.7.0
django-import-export==3.3.6
django-filter==23.5
djangorestframework-simplejwt==5.3.0
whitenoise==6.6.0
celery==5.3.4
django-celery-beat==2.5.0
redis==5.0.1
Pillow==10.1.0
psycopg2-binary==2.9.9  # For PostgreSQL
django-environ==0.11.2
django-debug-toolbar==4.2.0
pytest-django==4.7.0
requests==2.31.0
pycryptodome==3.19.0
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```bash
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: postgres://user:password@localhost:5432/dbname

# Email (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# PayTM
PAYTM_MID=your-merchant-id
PAYTM_MERCHANT_KEY=your-merchant-key
PAYTM_ENABLED=True

# Redis
REDIS_URL=redis://localhost:6379/1

# Base URL
BASE_URL=http://localhost:8000
```

### Step 5: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 8: Load Sample Data (Optional)
```bash
python manage.py create_sample_data
```

---

## ⚙️ Configuration

### Settings Configuration (`settings.py`)

#### Database Setup
```python
# For SQLite (Development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For PostgreSQL (Production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'exam_db',
        'USER': 'exam_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Email Configuration
```python
# Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'GovtExamWala <noreply@govtexamwala.com>'

# For development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### Celery Configuration
```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
```

#### PayTM Configuration
```python
PAYTM_ENABLED = True
PAYTM_DEBUG = True
PAYTM_MID = os.getenv('PAYTM_MID')
PAYTM_MERCHANT_KEY = os.getenv('PAYTM_MERCHANT_KEY')
PAYTM_WEBSITE_NAME = 'WEBSTAGING'
PAYTM_INDUSTRY_TYPE = 'Retail'
PAYTM_CHANNEL_ID = 'WEB'
```

---

## 🗄️ Database Setup

### SQLite (Development)
```bash
# Database file will be created automatically at db.sqlite3
# Run migrations
python manage.py migrate
```

### PostgreSQL (Production)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE exam_db;
CREATE USER exam_user WITH PASSWORD 'your_password';
ALTER ROLE exam_user SET client_encoding TO 'utf8';
ALTER ROLE exam_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE exam_user SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE exam_db TO exam_user;
\q

# Apply migrations
python manage.py migrate
```

---

## 🚀 Running the Application

### Development Server
```bash
# Start Django server
python manage.py runserver

# Access at: http://localhost:8000
```

### Celery (Background Tasks)
```bash
# Start Celery worker
celery -A exam_prep worker -l info

# Start Celery beat (scheduled tasks)
celery -A exam_prep beat -l info

# Start Redis (if not already running)
redis-server
```

### Production (Gunicorn + Nginx)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:8000 exam_prep.wsgi:application

# Using systemd for production (create service file)
sudo nano /etc/systemd/system/gunicorn.service
```

---

## 📚 Features in Detail

### 1. User Authentication

#### Login & Registration
- **OTP-based login**: Passwordless authentication via email OTP
- **Password-based login**: Traditional email/password login
- **Registration**: Create account with email and password or OTP

#### Password Management
- **Forgot Password**: Reset password via email link
- **Change Password**: Change password from profile
- **Set Password**: Set password for OTP users

### 2. Exam Management

#### Creating an Exam
```python
from apps.exams.models import Exam, Subject, Topic, Question, Option

# Create Exam
exam = Exam.objects.create(
    name='SBI PO 2024',
    short_name='SBI PO',
    category=category,
    description='<p>Exam description</p>',
    duration_minutes=60,
    total_marks=100,
    total_questions=100,
    negative_marking=True,
    is_paid=True,
    price=999
)

# Create Subject
subject = Subject.objects.create(
    exam=exam,
    name='Quantitative Aptitude',
    weightage=35
)

# Create Topic
topic = Topic.objects.create(
    subject=subject,
    name='Percentage',
    weightage=5
)

# Create Question
question = Question.objects.create(
    exam=exam,
    subject=subject,
    topic=topic,
    question_text='What is 15% of 200?',
    question_type='mcq',
    difficulty='easy',
    marks=2,
    negative_marks=0.25,
    explanation='15/100 * 200 = 30'
)

# Create Options
Option.objects.create(question=question, option_text='20', is_correct=False)
Option.objects.create(question=question, option_text='30', is_correct=True)
Option.objects.create(question=question, option_text='40', is_correct=False)
```

### 3. Mock Tests

#### Taking a Test
```python
from apps.mocktests.models import MockTest, TestAttempt, TestAnswer

# Start test attempt
attempt = TestAttempt.objects.create(
    user=request.user,
    mock_test=mock_test,
    status='in_progress',
    start_time=timezone.now()
)

# Submit answer
TestAnswer.objects.create(
    attempt=attempt,
    question=question,
    selected_option='A',
    is_correct=True,
    marks_obtained=2,
    time_taken=15
)

# Complete test
attempt.status = 'completed'
attempt.end_time = timezone.now()
attempt.score = total_score
attempt.percentage = percentage
attempt.save()
```

### 4. Study Materials

```python
from apps.study_materials.models import Course, Section, Lecture

# Create Course
course = Course.objects.create(
    title='Complete Banking Course',
    description='Comprehensive banking exam preparation',
    exam=exam,
    is_free=False,
    price=1999
)

# Create Section
section = Section.objects.create(
    course=course,
    title='Quantitative Aptitude',
    order=1
)

# Create Lecture
lecture = Lecture.objects.create(
    section=section,
    title='Percentage Basics',
    lecture_type='video',
    video_url='https://youtube.com/watch?v=xxx',
    duration=30
)
```

### 5. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login/` | POST | User login |
| `/api/auth/register/` | POST | User registration |
| `/api/exams/` | GET | List all exams |
| `/api/exams/{id}/` | GET | Exam details |
| `/api/mocktests/` | GET | List mock tests |
| `/api/mocktests/{id}/start/` | POST | Start mock test |
| `/api/mocktests/{id}/submit/` | POST | Submit mock test |
| `/api/questions/` | GET | List questions |
| `/api/analytics/performance/` | GET | User performance |
| `/api/payments/create-order/` | POST | Create payment order |
| `/api/payments/verify/` | POST | Verify payment |

---

## 💳 Payment Integration

### PayTM Integration

The platform uses PayTM as the primary payment gateway.

#### Configuration
```python
# settings.py
PAYTM_ENABLED = True
PAYTM_MID = "YOUR_MID"
PAYTM_MERCHANT_KEY = "YOUR_KEY"
PAYTM_WEBSITE_NAME = "WEBSTAGING"  # For testing
```

#### Payment Flow
1. User adds items to cart
2. User proceeds to checkout
3. Create order in database
4. Initiate PayTM payment
5. User redirected to PayTM
6. PayTM redirects back with status
7. Verify payment signature
8. Unlock content for user

#### Testing
```bash
# Test with PayTM staging
PAYTM_DEBUG = True

# Test card details
Card: 4111111111111111
Expiry: 12/25
CVV: 123
OTP: 123456
```

---

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password
3. Use the app password in settings

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # App Password
```

### Email Templates
- **Password Reset**: `templates/emails/password_reset_email.html`
- **OTP Email**: `templates/emails/otp_email.html`
- **Welcome Email**: `templates/emails/welcome_email.html`

---

## 🎨 Admin Panel

### Custom Admin Features
- **Colorful Theme**: Modern gradient-based admin interface
- **Quick Actions**: Verify users, export data
- **Inline Editing**: Edit related objects directly
- **Advanced Filters**: Filter by date, status, etc.
- **Bulk Actions**: Delete, update multiple records

### Access Admin Panel
```bash
# Login with superuser credentials
http://localhost:8000/admin/
```

### Admin Customization
```python
# apps/accounts/admin.py
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active']
    actions = ['verify_users']
    
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, f'{queryset.count()} users verified.')
```

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.exams

# Run with coverage
pip install coverage
coverage run manage.py test
coverage report
```

### Test Data
```bash
# Load sample data
python manage.py create_sample_data

# Create test users
python manage.py create_test_users
```

---

## 🚢 Deployment

### Requirements
- Python 3.12+
- PostgreSQL
- Redis
- Nginx (for serving static/media)
- Supervisor/systemd (for process management)

### Deployment Steps

#### 1. Setup Server
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install Python and dependencies
sudo apt install python3-pip python3-dev python3-venv
sudo apt install nginx postgresql redis-server
```

#### 2. Configure Database
```bash
sudo -u postgres psql
CREATE DATABASE exam_db;
CREATE USER exam_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE exam_db TO exam_user;
```

#### 3. Configure Gunicorn
```bash
# Create gunicorn service
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=Gunicorn instance for exam platform
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/exam-platform
Environment="PATH=/home/ubuntu/exam-platform/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=exam_prep.settings"
ExecStart=/home/ubuntu/exam-platform/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/exam-platform/exam-platform.sock exam_prep.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 4. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/exam-platform
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/exam-platform/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/exam-platform/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/exam-platform/exam-platform.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/exam-platform /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### 5. Configure Celery (Optional)
```bash
# Celery worker service
sudo nano /etc/systemd/system/celery.service
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Email Not Sending
```bash
# Check email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@email.com', ['to@email.com'], fail_silently=False)

# If using Gmail, ensure App Password is correct
# Check logs: logs/django.log
```

#### 2. PayTM Integration Fails
```bash
# Check PayTM configuration
python manage.py shell
>>> from apps.payments.paytm_utils import paytm_gateway
>>> result = paytm_gateway.verify_payment('test_order')
>>> print(result)

# Ensure PAYTM_DEBUG=True for testing
# Check PayTM merchant credentials
```

#### 3. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT in settings
# Ensure WhiteNoise is configured correctly
```

#### 4. Database Migration Issues
```bash
# Reset migrations
python manage.py reset_db
python manage.py makemigrations
python manage.py migrate

# For specific app
python manage.py migrate apps.exams --fake
python manage.py migrate apps.exams
```

#### 5. Celery Not Working
```bash
# Check Redis is running
redis-cli ping

# Start celery with verbose logging
celery -A exam_prep worker -l debug

# Check celery beat
celery -A exam_prep beat -l debug
```

#### 6. Admin Panel


### Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions
- Write tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

- **Email**: support@govtexamwala.com
- **Documentation**: [https://docs.govtexamwala.com](https://docs.govtexamwala.com)
- **Issue Tracker**: [GitHub Issues](https://github.com/yourusername/govt-exam-platform/issues)

---

## 🙏 Acknowledgments

- Django Community for the amazing framework
- All open-source contributors
- Our beta testers

---

## 📝 Changelog

### v1.0.0 (2026-06-21)
- Initial release
- Complete exam management system
- PayTM payment integration
- Mock tests with analytics
- Study materials management
- Interview preparation module
- User authentication with OTP

---

**Built with ❤️ for Government Exam Aspirants**
