#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime

# Setup Django
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Try to find settings
settings_module = None
for module in ['exam_prep.settings', 'config.settings', 'settings']:
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', module)
        django.setup()
        settings_module = module
        print(f"✓ Using settings: {module}")
        break
    except ImportError:
        continue

if not settings_module:
    print("❌ Could not find Django settings")
    sys.exit(1)

# Import models
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.exams.models import Exam, Subject, Question, Option, ExamCategory
from apps.mocktests.models import MockTest, MockTestQuestion

def create_current_affairs_mock_test_part5():
    print("=" * 80)
    print("📰 CREATING CURRENT AFFAIRS MOCK TEST PART 5 (QUESTIONS 401-500)")
    print("=" * 80)
    
    # Create or get ExamCategory first
    print("\n📚 Setting up Exam Category...")
    
    exam_category, _ = ExamCategory.objects.get_or_create(
        name='Current Affairs',
        defaults={
            'slug': 'current-affairs',
            'description': 'Current Affairs exams and mock tests'
        }
    )
    print(f"✓ Exam Category: {exam_category.name}")
    
    # Create or get Current Affairs exam
    print("\n📚 Setting up Current Affairs Exam...")
    
    exam, created = Exam.objects.get_or_create(
        slug='current-affairs-2024-part5',
        defaults={
            'name': 'Current Affairs 2024 - Part 5',
            'short_name': 'CA 2024 P5',
            'category': exam_category,
            'exam_level': 'national',
            'duration_minutes': 60,
            'total_marks': 100,
            'total_questions': 100,
            'negative_marking': False,
            'description': 'Comprehensive Current Affairs Mock Test Part 5 covering Henley Passport Index, Swachh Survekshan, Global Firepower & FIFA Awards',
            'is_paid': False,
            'price': 0,
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ Created exam: {exam.name}")
    else:
        print(f"✓ Using existing exam: {exam.name}")
    
    # Create subject
    subject, _ = Subject.objects.get_or_create(
        exam=exam,
        name='Current Affairs 2024 - Part 5',
        defaults={'weightage': 100, 'order': 1}
    )
    print(f"✓ Subject: {subject.name}")
    
    # Clear existing questions for this exam
    Question.objects.filter(exam=exam).delete()
    print("✓ Cleared existing questions")
    
    # All 100 Current Affairs Questions (401-500)
    questions_data = [
        # Q401-Q425: Henley Passport Index 2024
        {
            'text': 'Which countries jointly topped the Henley Passport Index 2024?',
            'options': [
                'USA, UK, Canada',
                'France, Germany, Italy, Japan, Singapore, Spain',
                'China, Japan, South Korea',
                'Germany, Sweden, Norway'
            ],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Citizens of the top-ranked passports can access how many destinations?',
            'options': ['190', '192', '194', '196'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'India ranked ____ in the Henley Passport Index 2024.',
            'options': ['75th', '78th', '80th', '85th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': "India's passport provides visa-free or visa-on-arrival access to how many countries?",
            'options': ['52 countries', '62 countries', '72 countries', '82 countries'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country shared the top rank with Japan?',
            'options': ['India', 'Singapore', 'China', 'Australia'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Finland, South Korea, and Sweden ranked at which position?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Austria ranked at which position?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'United Kingdom ranked at which position?',
            'options': ['4th', '5th', '6th', '7th'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'United States ranked at which position?',
            'options': ['5th', '6th', '7th', '8th'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Canada ranked at which position?',
            'options': ['6th', '7th', '8th', '9th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which organization publishes the Henley Passport Index?',
            'options': ['Henley & Partners', 'World Bank', 'UNWTO', 'IMF'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'How many destinations can top-ranked passport holders access?',
            'options': ['190', '192', '194', '196'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': "India's rank in the Henley Passport Index 2024 is:",
            'options': ['75th', '78th', '80th', '85th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': "India's passport provides access to how many countries?",
            'options': ['52', '62', '72', '82'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Japan ranked at which position in Henley Passport Index 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Singapore ranked at which position in Henley Passport Index 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Germany ranked at which position in Henley Passport Index 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Spain ranked at which position in Henley Passport Index 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'South Korea ranked at which position in Henley Passport Index 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Sweden ranked at which position in Henley Passport Index 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Netherlands ranked at which position in Henley Passport Index 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'United Kingdom ranked at which position in Henley Passport Index 2024?',
            'options': ['4th', '5th', '6th', '7th'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Switzerland ranked at which position in Henley Passport Index 2024?',
            'options': ['4th', '5th', '6th', '7th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'USA ranked at which position in Henley Passport Index 2024?',
            'options': ['5th', '6th', '7th', '8th'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Canada ranked at which position in Henley Passport Index 2024?',
            'options': ['6th', '7th', '8th', '9th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        # Q426-Q450: Swachh Survekshan Awards 2023
        {
            'text': 'Which cities jointly won the Cleanest City title in Swachh Survekshan 2023?',
            'options': ['Indore & Bhopal', 'Surat & Ahmedabad', 'Indore & Surat', 'Pune & Surat'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Indore won the Cleanest City title for which consecutive time?',
            'options': ['5th time', '6th time', '7th consecutive time', '8th time'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Swachh Survekshan Awards were presented by whom?',
            'options': ['Narendra Modi', 'Amit Shah', 'Droupadi Murmu', 'Jagdeep Dhankhar'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The Swachh Survekshan Awards ceremony venue was:',
            'options': ['Rashtrapati Bhavan', 'Bharat Mandapam', 'Vigyan Bhavan', 'India Gate'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which ministry is responsible for Swachh Survekshan?',
            'options': ['MoRD', 'MoHUA', 'MoEFCC', 'MoHFW'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which was declared the Cleanest Cantonment Board?',
            'options': ['Delhi Cantonment', 'Pune Cantonment', 'Mhow Cantonment Board', 'Jaipur Cantonment'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which was declared the Best Cleanest Ganga Town?',
            'options': ['Haridwar', 'Varanasi', 'Rishikesh', 'Patna'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which was declared the Best Performing State?',
            'options': ['Gujarat', 'Maharashtra', 'Tamil Nadu', 'Karnataka'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which was declared the Second-best Performing State?',
            'options': ['Madhya Pradesh', 'Gujarat', 'Rajasthan', 'Kerala'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Which was declared the Third-best Performing State?',
            'options': ['Odisha', 'Chhattisgarh', 'Bihar', 'Assam'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which city won the Best Safaimitra Surakshit Sheher award?',
            'options': ['Indore', 'Chandigarh', 'Surat', 'Pune'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'What was the theme of Swachh Survekshan 2024?',
            'options': ['Swachh Bharat', 'Green India', 'Reduce, Reuse, Recycle', 'Clean Cities Mission'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many awards were distributed in Swachh Survekshan 2023?',
            'options': ['90', '100', '110', '120'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many Urban Local Bodies participated in Swachh Survekshan 2023?',
            'options': ['3,447', '4,447', '5,447', '6,447'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Swachh Survekshan is considered the:',
            'options': ['Largest health survey', 'Largest sanitation survey', 'World\'s largest cleanliness survey', 'Largest population survey'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Who were the joint cleanest city winners?',
            'options': ['Indore & Bhopal', 'Surat & Ahmedabad', 'Indore & Surat', 'Pune & Surat'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The Swachh Survekshan awards were presented at which venue?',
            'options': ['Rashtrapati Bhavan', 'Bharat Mandapam', 'Vigyan Bhavan', 'India Gate'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The ministry responsible for Swachh Survekshan is:',
            'options': ['MoRD', 'MoHUA', 'MoEFCC', 'MoHFW'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The Cleanest Cantonment Board winner was:',
            'options': ['Delhi Cantonment', 'Pune Cantonment', 'Mhow Cantonment Board', 'Jaipur Cantonment'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The Best Ganga Town winner was:',
            'options': ['Haridwar', 'Varanasi', 'Rishikesh', 'Patna'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The Best Performing State was:',
            'options': ['Gujarat', 'Maharashtra', 'Tamil Nadu', 'Karnataka'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The Best Safaimitra Surakshit Sheher winner was:',
            'options': ['Indore', 'Chandigarh', 'Surat', 'Pune'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The theme of Swachh Survekshan 2024 is:',
            'options': ['Swachh Bharat', 'Green India', 'Reduce, Reuse, Recycle', 'Clean Cities Mission'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The number of Urban Local Bodies participating was:',
            'options': ['3,447', '4,447', '5,447', '6,447'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'MoHUA stands for:',
            'options': ['Ministry of Housing and Urban Affairs', 'Ministry of Health and Urban Affairs', 'Ministry of Home and Urban Affairs', 'Ministry of Housing and Union Affairs'],
            'correct': 0,
            'difficulty': 'easy'
        },
        # Q451-Q475: Global Firepower Military Rankings 2024
        {
            'text': 'Which country topped the Global Firepower Rankings 2024?',
            'options': ['Russia', 'China', 'USA', 'India'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Russia ranked at which position in Global Firepower Rankings 2024?',
            'options': ['1st', '2nd', '3rd', '4th'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'China ranked at which position in Global Firepower Rankings 2024?',
            'options': ['2nd', '3rd', '4th', '5th'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': "India's rank in Global Firepower Rankings 2024 was:",
            'options': ['3rd', '4th', '5th', '6th'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Pakistan ranked at which position in Global Firepower Rankings 2024?',
            'options': ['7th', '8th', '9th', '10th'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'United Kingdom ranked at which position in Global Firepower Rankings 2024?',
            'options': ['5th', '6th', '7th', '8th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Japan ranked at which position in Global Firepower Rankings 2024?',
            'options': ['6th', '7th', '8th', '9th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'South Korea ranked at which position in Global Firepower Rankings 2024?',
            'options': ['4th', '5th', '6th', '7th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 145th in Global Firepower Rankings 2024?',
            'options': ['Moldova', 'Somalia', 'Bhutan', 'Belize'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many countries were evaluated in Global Firepower Rankings 2024?',
            'options': ['140', '142', '145', '150'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 1st in Global Firepower 2024?',
            'options': ['Russia', 'China', 'USA', 'India'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Which country ranked 2nd in Global Firepower 2024?',
            'options': ['Russia', 'China', 'USA', 'India'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country ranked 3rd in Global Firepower 2024?',
            'options': ['Russia', 'China', 'USA', 'India'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country ranked 4th in Global Firepower 2024?',
            'options': ['Russia', 'China', 'USA', 'India'],
            'correct': 3,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country ranked 5th in Global Firepower 2024?',
            'options': ['UK', 'South Korea', 'Japan', 'Turkey'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 6th in Global Firepower 2024?',
            'options': ['UK', 'South Korea', 'Japan', 'Turkey'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 7th in Global Firepower 2024?',
            'options': ['UK', 'South Korea', 'Japan', 'Turkey'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 8th in Global Firepower 2024?',
            'options': ['UK', 'South Korea', 'Japan', 'Turkey'],
            'correct': 3,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 9th in Global Firepower 2024?',
            'options': ['Pakistan', 'Italy', 'Brazil', 'France'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 10th in Global Firepower 2024?',
            'options': ['Pakistan', 'Italy', 'Brazil', 'France'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The lowest rank (145th) in Global Firepower 2024 was held by:',
            'options': ['Moldova', 'Somalia', 'Bhutan', 'Belize'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The Power Index of USA in Global Firepower 2024 was:',
            'options': ['0.0699', '0.0702', '0.0706', '0.0711'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The Power Index of Russia in Global Firepower 2024 was:',
            'options': ['0.0699', '0.0702', '0.0706', '0.0711'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The Power Index of China in Global Firepower 2024 was:',
            'options': ['0.0699', '0.0702', '0.0706', '0.0711'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Global Firepower 2024 covered how many countries?',
            'options': ['140', '142', '145', '150'],
            'correct': 2,
            'difficulty': 'hard'
        },
        # Q476-Q500: FIFA Football Awards 2024
        {
            'text': 'FIFA Men\'s Player of the Year 2024 was:',
            'options': ['Mbappe', 'Haaland', 'Lionel Messi', 'De Bruyne'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'FIFA Women\'s Player of the Year 2024 was:',
            'options': ['Alexia Putellas', 'Aitana Bonmati', 'Mary Earps', 'Sam Kerr'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Men\'s Coach of the Year 2024 was:',
            'options': ['Klopp', 'Pep Guardiola', 'Xavi', 'Ancelotti'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Women\'s Coach of the Year 2024 was:',
            'options': ['Emma Hayes', 'Sarina Wiegman', 'Jill Ellis', 'Pia Sundhage'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'FIFA Men\'s Goalkeeper of the Year 2024 was:',
            'options': ['Alisson', 'Ederson', 'Courtois', 'Martinez'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'FIFA Women\'s Goalkeeper of the Year 2024 was:',
            'options': ['Mary Earps', 'Berger', 'Endler', 'Musovic'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'FIFA Puskas Award 2024 winner was:',
            'options': ['Lionel Messi', 'Haaland', 'Guilherme Madruga', 'Mbappe'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'FIFA Special Award 2024 winner was:',
            'options': ['Lionel Messi', 'Marta', 'Ronaldo', 'Mbappe'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'FIFA Fair Play Award 2024 was won by:',
            'options': ['Argentina', 'Brazil Men\'s Team', 'Spain', 'Germany'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'FIFA Fan Award 2024 winner was:',
            'options': ['Lionel Messi', 'Marta', 'Hugo Daniel Iniguez', 'Mbappe'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won the FIFA Men\'s Player of the Year 2024?',
            'options': ['Mbappe', 'Haaland', 'Lionel Messi', 'De Bruyne'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Who won the FIFA Women\'s Player of the Year 2024?',
            'options': ['Alexia Putellas', 'Aitana Bonmati', 'Mary Earps', 'Sam Kerr'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won the FIFA Men\'s Coach of the Year 2024?',
            'options': ['Klopp', 'Pep Guardiola', 'Xavi', 'Ancelotti'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won the FIFA Women\'s Coach of the Year 2024?',
            'options': ['Emma Hayes', 'Sarina Wiegman', 'Jill Ellis', 'Pia Sundhage'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won the FIFA Men\'s Goalkeeper of the Year 2024?',
            'options': ['Alisson', 'Ederson', 'Courtois', 'Martinez'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won the FIFA Women\'s Goalkeeper of the Year 2024?',
            'options': ['Mary Earps', 'Berger', 'Endler', 'Musovic'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won the FIFA Puskas Award 2024?',
            'options': ['Lionel Messi', 'Haaland', 'Guilherme Madruga', 'Mbappe'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won the FIFA Special Award 2024?',
            'options': ['Lionel Messi', 'Marta', 'Ronaldo', 'Mbappe'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won the FIFA Fair Play Award 2024?',
            'options': ['Argentina', 'Brazil Men\'s Team', 'Spain', 'Germany'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won the FIFA Fan Award 2024?',
            'options': ['Lionel Messi', 'Marta', 'Hugo Daniel Iniguez', 'Mbappe'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The FIFA Awards 2024 ceremony was held in which city?',
            'options': ['London', 'Paris', 'Madrid', 'Berlin'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Lionel Messi is from which country?',
            'options': ['Brazil', 'Argentina', 'Spain', 'Portugal'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Aitana Bonmati is from which country?',
            'options': ['Spain', 'England', 'France', 'Germany'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Pep Guardiola is the coach of which club?',
            'options': ['Arsenal', 'Barcelona', 'Manchester City', 'Bayern Munich'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Awards are related to which sport?',
            'options': ['Cricket', 'Football', 'Tennis', 'Basketball'],
            'correct': 1,
            'difficulty': 'easy'
        }
    ]
    
    # Create questions
    print("\n📝 Creating 100 Current Affairs Questions (401-500)...")
    
    created_questions = []
    for idx, q_data in enumerate(questions_data, 401):
        # Shuffle options and track correct answer
        options = q_data['options']
        correct_index = q_data['correct']
        correct_answer = options[correct_index]
        
        # Randomize options position
        option_list = list(enumerate(options))
        random.shuffle(option_list)
        shuffled_options = [opt for _, opt in option_list]
        new_correct_index = [opt for _, opt in option_list].index(correct_answer)
        
        # Create question with explanation "N/A"
        question = Question.objects.create(
            exam=exam,
            subject=subject,
            question_text=q_data['text'],
            question_type='mcq',
            difficulty=q_data['difficulty'],
            marks=1,
            negative_marks=0,
            explanation="N/A",
            is_active=True
        )
        
        # Create options
        for i, opt_text in enumerate(shuffled_options):
            Option.objects.create(
                question=question,
                option_text=opt_text,
                is_correct=(i == new_correct_index),
                order=i
            )
        
        created_questions.append(question)
        
        if idx % 10 == 0:
            print(f"   ✓ Created question {idx}...")
    
    print(f"\n✓ Created {len(created_questions)} questions (401-500)")
    
    # Create Mock Test
    print("\n🎯 Creating Current Affairs Mock Test Part 5...")
    
    # Delete existing mock test
    MockTest.objects.filter(slug='current-affairs-mock-test-2024-part5').delete()
    
    mock_test = MockTest.objects.create(
        name='Current Affairs Mock Test 2024 - Part 5 (401-500 Questions)',
        slug='current-affairs-mock-test-2024-part5',
        exam=exam,
        description='Comprehensive mock test covering Henley Passport Index, Swachh Survekshan, Global Firepower & FIFA Awards',
        duration_minutes=60,
        total_questions=len(created_questions),
        total_marks=len(created_questions),
        is_paid=False,
        price=0,
        attempts_allowed=5,
        is_active=True
    )
    
    # Add questions to mock test
    for idx, question in enumerate(created_questions):
        MockTestQuestion.objects.create(
            mock_test=mock_test,
            question=question,
            marks=1,
            order=idx
        )
    
    print(f"✓ Created mock test: {mock_test.name}")
    print(f"  └─ {mock_test.total_questions} questions | {mock_test.duration_minutes} minutes")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ CURRENT AFFAIRS MOCK TEST PART 5 CREATION COMPLETED!")
    print("=" * 80)
    
    print("\n📊 SUMMARY:")
    print(f"   • Exam Category: {exam_category.name}")
    print(f"   • Exam: {exam.name}")
    print(f"   • Subject: {subject.name}")
    print(f"   • Questions Created: {len(created_questions)}")
    print(f"   • Mock Test: {mock_test.name}")
    print(f"   • Total Questions in Mock Test: {MockTestQuestion.objects.filter(mock_test=mock_test).count()}")
    print(f"   • Price: ₹{mock_test.price} ({'FREE' if not mock_test.is_paid else 'PAID'})")
    
    print("\n🎯 To take the mock test:")
    print("   1. Login to the application")
    print("   2. Go to Mock Tests section")
    print("   3. Select 'Current Affairs Mock Test 2024 - Part 5 (401-500 Questions)'")
    print("   4. Start practicing!")
    
    print("\n📈 DIFFICULTY DISTRIBUTION:")
    easy = Question.objects.filter(exam=exam, difficulty='easy').count()
    medium = Question.objects.filter(exam=exam, difficulty='medium').count()
    hard = Question.objects.filter(exam=exam, difficulty='hard').count()
    print(f"   • Easy: {easy}")
    print(f"   • Medium: {medium}")
    print(f"   • Hard: {hard}")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        create_current_affairs_mock_test_part5()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)