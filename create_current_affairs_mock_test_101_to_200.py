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

def create_current_affairs_mock_test_part2():
    print("=" * 80)
    print("📰 CREATING CURRENT AFFAIRS MOCK TEST PART 2 (QUESTIONS 101-200)")
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
        slug='current-affairs-2024-part2',
        defaults={
            'name': 'Current Affairs 2024 - Part 2',
            'short_name': 'CA 2024 P2',
            'category': exam_category,
            'exam_level': 'national',
            'duration_minutes': 60,
            'total_marks': 100,
            'total_questions': 100,
            'negative_marking': False,
            'description': 'Comprehensive Current Affairs Mock Test Part 2 covering Awards, Republic Day, ICC Awards 2024',
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
        name='Current Affairs 2024 - Part 2',
        defaults={'weightage': 100, 'order': 1}
    )
    print(f"✓ Subject: {subject.name}")
    
    # Clear existing questions for this exam
    Question.objects.filter(exam=exam).delete()
    print("✓ Cleared existing questions")
    
    # All 100 Current Affairs Questions (101-200)
    questions_data = [
        # Q101-Q125: Awards, Honours & Culture
        {
            'text': 'Which award is India\'s highest civilian award?',
            'options': ['Padma Shri', 'Bharat Ratna', 'Padma Bhushan', 'Padma Vibhushan'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Padma Awards are announced every year on which occasion?',
            'options': ['Independence Day', 'Republic Day', 'Gandhi Jayanti', 'Constitution Day'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The Padma Awards are given in how many categories?',
            'options': ['2', '3', '4', '5'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which is the highest category among Padma Awards?',
            'options': ['Padma Shri', 'Padma Bhushan', 'Padma Vibhushan', 'Bharat Ratna'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which award is given for distinguished service of a high order?',
            'options': ['Bharat Ratna', 'Padma Shri', 'Padma Bhushan', 'Param Vir Chakra'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which award is given for distinguished service in any field?',
            'options': ['Padma Shri', 'Ashok Chakra', 'Gallantry Award', 'Arjuna Award'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Which ministry administers the Padma Awards?',
            'options': ['Ministry of Culture', 'Ministry of Home Affairs', 'Ministry of Education', 'Ministry of Law'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Bharat Ratna was instituted in which year?',
            'options': ['1947', '1950', '1954', '1962'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which award is known as India\'s highest wartime gallantry award?',
            'options': ['Ashok Chakra', 'Kirti Chakra', 'Param Vir Chakra', 'Vir Chakra'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Which award is India\'s highest peacetime gallantry award?',
            'options': ['Ashok Chakra', 'Param Vir Chakra', 'Maha Vir Chakra', 'Sena Medal'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Ram Mandir is situated on the banks of which river?',
            'options': ['Ganga', 'Yamuna', 'Saryu', 'Godavari'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Ram Mandir commemorative stamp collection contains how many stamps?',
            'options': ['4 stamps', '5 stamps', '6 stamps', '10 stamps'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which bird character from Ramayana was featured in the stamp series?',
            'options': ['Garuda', 'Jatayu', 'Sampati', 'Huma'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which devotee was featured in the Ram Mandir stamp collection?',
            'options': ['Kevatraj', 'Sugriva', 'Vibhishana', 'Angad'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Which Hindu deity was included in the Ram Mandir stamp series?',
            'options': ['Shiva', 'Vishnu', 'Ganesh', 'Kartikeya'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The commemorative stamp collection also includes which devotee?',
            'options': ['Ma Shabri', 'Draupadi', 'Kunti', 'Sita only'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Mandir stamp collection book contains stamps from over how many countries?',
            'options': ['10 countries', '15 countries', '20 countries', '30 countries'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which international organization issued stamps related to Lord Ram?',
            'options': ['UNESCO', 'WTO', 'United Nations', 'WHO'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The five elements represented in the stamp designs are called:',
            'options': ['Panchatatva', 'Panchabhutas', 'Triguna', 'Panchakosha'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Lalla idol depicts Lord Ram at what age?',
            'options': ['3 years', '5 years', '8 years', '10 years'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Lalla idol was installed on which date?',
            'options': ['Jan 15, 2024', 'Jan 18, 2024', 'Jan 20, 2024', 'Jan 22, 2024'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Mandir\'s sanctum sanctorum is known as:',
            'options': ['Garbhagriha', 'Sabha Mandap', 'Rang Mandap', 'Yagya Mandap'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Mandir inauguration took place in which state?',
            'options': ['Uttar Pradesh', 'Madhya Pradesh', 'Uttarakhand', 'Rajasthan'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'The Ram Mandir idol was sculpted from:',
            'options': ['White marble', 'Black stone', 'Sandstone', 'Granite'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The Pran Pratishtha ceremony was attended by over:',
            'options': ['4,000 people', '5,000 people', '7,000 dignitaries', '10,000 dignitaries'],
            'correct': 2,
            'difficulty': 'medium'
        },
        # Q126-Q150: Republic Day & Constitution
        {
            'text': 'India\'s Constitution came into force on which date?',
            'options': ['15 August 1947', '26 November 1949', '26 January 1950', '24 January 1950'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day 2024 marked which Republic Day?',
            'options': ['73rd', '74th', '75th', '76th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Republic Day 2024 Chief Guest was:',
            'options': ['Joe Biden', 'Emmanuel Macron', 'Vladimir Putin', 'Rishi Sunak'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': '"Viksit Bharat" means:',
            'options': ['Digital India', 'Developed India', 'New India', 'Modern India'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Who chaired the Drafting Committee of the Constitution?',
            'options': ['Jawaharlal Nehru', 'Rajendra Prasad', 'B.R. Ambedkar', 'Vallabhbhai Patel'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The Constitution of India was adopted on which date?',
            'options': ['15 August 1947', '26 November 1949', '26 January 1950', '24 January 1950'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Republic Day parade is held at which location?',
            'options': ['Mumbai', 'Kolkata', 'New Delhi', 'Chennai'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day celebrates what occasion?',
            'options': ['Independence', 'Constitution enforcement', 'Republic formation', 'Democracy day'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country was the guest country for Republic Day 2024?',
            'options': ['USA', 'UK', 'France', 'Russia'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Who was the President of France in 2024?',
            'options': ['Emmanuel Macron', 'Francois Hollande', 'Nicolas Sarkozy', 'Jacques Chirac'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Who was India\'s first President?',
            'options': ['Jawaharlal Nehru', 'Dr. Rajendra Prasad', 'Sardar Patel', 'B.R. Ambedkar'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The Constitution describes India as:',
            'options': ['Sovereign Democratic Republic', 'Sovereign Socialist Republic', 'Sovereign Secular Republic', 'Federal Republic'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country has the longest written constitution?',
            'options': ['USA', 'UK', 'India', 'Canada'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Who is known as the Father of Indian Constitution?',
            'options': ['Mahatma Gandhi', 'Jawaharlal Nehru', 'B.R. Ambedkar', 'Sardar Patel'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day is celebrated in which month?',
            'options': ['August', 'October', 'January', 'November'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The National Flag of India was adopted in which year?',
            'options': ['1946', '1947', '1950', '1952'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who composed the National Anthem of India?',
            'options': ['Bankim Chandra Chatterjee', 'Rabindranath Tagore', 'Sarojini Naidu', 'Muhammad Iqbal'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'What is the National Song of India?',
            'options': ['Jana Gana Mana', 'Vande Mataram', 'Sare Jahan Se Achha', 'Ae Mere Watan Ke Logon'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Which awards are announced on Republic Day?',
            'options': ['Padma Awards', 'Gallantry Awards', 'Both Padma and Gallantry Awards', 'Only Bharat Ratna'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which gallantry award is announced on Republic Day?',
            'options': ['Param Vir Chakra', 'Ashok Chakra', 'Kirti Chakra', 'Vir Chakra'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The Parliament of India is located in which city?',
            'options': ['Mumbai', 'Kolkata', 'New Delhi', 'Chennai'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The Supreme Court of India was established in which year?',
            'options': ['1947', '1949', '1950', '1952'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The National Emblem of India was adopted in which year?',
            'options': ['1947', '1948', '1949', '1950'],
            'correct': 3,
            'difficulty': 'hard'
        },
        {
            'text': 'What is the motto of India?',
            'options': ['Truth Alone Triumphs', 'Unity in Diversity', 'Justice Liberty Equality', 'Work is Worship'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Constitution Day is observed on which date?',
            'options': ['15 August', '26 January', '26 November', '2 October'],
            'correct': 2,
            'difficulty': 'medium'
        },
        # Q151-Q175: ICC Awards & Cricket
        {
            'text': 'ICC Men\'s Cricketer of the Year 2023:',
            'options': ['Virat Kohli', 'Pat Cummins', 'Travis Head', 'Rohit Sharma'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Sir Garfield Sobers Trophy is awarded for:',
            'options': ['Best ODI Player', 'Best Test Player', 'ICC Men\'s Cricketer of the Year', 'Best Captain'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s ODI Cricketer of the Year 2023:',
            'options': ['Shubman Gill', 'Rohit Sharma', 'Virat Kohli', 'Travis Head'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Men\'s Test Cricketer of the Year 2023:',
            'options': ['Joe Root', 'Ravichandran Ashwin', 'Travis Head', 'Usman Khawaja'],
            'correct': 3,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Women\'s Cricketer of the Year 2023:',
            'options': ['Ellyse Perry', 'Hayley Matthews', 'Nat Sciver-Brunt', 'Alyssa Healy'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Women\'s ODI Cricketer of the Year 2023:',
            'options': ['Chamari Athapaththu', 'Ellyse Perry', 'Hayley Matthews', 'Ashleigh Gardner'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s Associate Cricketer of the Year 2023:',
            'options': ['Bas de Leede', 'Gerald Coetzee', 'Rachin Ravindra', 'Michael Bell'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Women\'s Associate Cricketer of the Year 2023:',
            'options': ['Queentor Abel', 'Michael Bell', 'Marufa Akter', 'Darcey Carter'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s T20I Cricketer of the Year 2023:',
            'options': ['Rohit Sharma', 'Suryakumar Yadav', 'Hardik Pandya', 'Shubman Gill'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Women\'s T20I Cricketer of the Year 2023:',
            'options': ['Ellyse Perry', 'Hayley Matthews', 'Ashleigh Gardner', 'Michael Bell'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Men\'s Emerging Cricketer of the Year 2023:',
            'options': ['Yashasvi Jaiswal', 'Gerald Coetzee', 'Rachin Ravindra', 'Dilshan Madushanka'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Rachin Ravindra represents which country?',
            'options': ['India', 'Australia', 'New Zealand', 'South Africa'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Women\'s Emerging Cricketer of the Year 2023:',
            'options': ['Phoebe Litchfield', 'Queentor Abel', 'Marufa Akter', 'Darcey Carter'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Pat Cummins represents which country?',
            'options': ['India', 'Australia', 'England', 'New Zealand'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Virat Kohli represents which country?',
            'options': ['India', 'Australia', 'England', 'South Africa'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Usman Khawaja represents which country?',
            'options': ['India', 'Australia', 'Pakistan', 'England'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Chamari Athapaththu represents which country?',
            'options': ['India', 'Sri Lanka', 'Bangladesh', 'Pakistan'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Bas de Leede represents which country?',
            'options': ['Netherlands', 'Belgium', 'Germany', 'Denmark'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Queentor Abel represents which country?',
            'options': ['Kenya', 'Uganda', 'Tanzania', 'Nigeria'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Suryakumar Yadav won ICC T20I award for how many consecutive years?',
            'options': ['First', 'Second', 'Third', 'Fourth'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Where is ICC headquarters located?',
            'options': ['London', 'Dubai', 'Sydney', 'Mumbai'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'What is the full form of ICC?',
            'options': ['International Cricket Council', 'Indian Cricket Council', 'International Cricket Committee', 'Indian Cricket Committee'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Who hosted the ODI World Cup 2023?',
            'options': ['India', 'Australia', 'England', 'South Africa'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Who won the World Cup 2023?',
            'options': ['India', 'Australia', 'England', 'New Zealand'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Who was the runner-up in World Cup 2023?',
            'options': ['India', 'Australia', 'England', 'South Africa'],
            'correct': 0,
            'difficulty': 'medium'
        },
        # Q176-Q200
        {
            'text': 'Who was the Player of Tournament in World Cup 2023?',
            'options': ['Rohit Sharma', 'Virat Kohli', 'Pat Cummins', 'Travis Head'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC was founded in which year?',
            'options': ['1899', '1909', '1919', '1929'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who is the ICC Chairman (2024)?',
            'options': ['Greg Barclay', 'Shashank Manohar', 'Narayanaswami Srinivasan', 'Ehsan Mani'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Cricket originated in which country?',
            'options': ['India', 'Australia', 'England', 'South Africa'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Test cricket started in which year?',
            'options': ['1867', '1877', '1887', '1897'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'How many overs are played in ODI format?',
            'options': ['40', '45', '50', '60'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'How many overs are played in T20 format?',
            'options': ['10', '15', '20', '25'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Hayley Matthews represents which country?',
            'options': ['Australia', 'England', 'West Indies', 'New Zealand'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Nat Sciver-Brunt represents which country?',
            'options': ['Australia', 'England', 'West Indies', 'New Zealand'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Associate Player award recognizes performances from:',
            'options': ['Full Members', 'Associate Nations', 'All Nations', 'Test Nations'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The Cricket World Cup is held every how many years?',
            'options': ['2 years', '3 years', '4 years', '5 years'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The Ashes is played between which two countries?',
            'options': ['India & Pakistan', 'England & Australia', 'Australia & New Zealand', 'England & South Africa'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Men\'s award trophy is named after:',
            'options': ['Don Bradman', 'Sir Garfield Sobers', 'Jack Hobbs', 'Viv Richards'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Women\'s award is named after:',
            'options': ['Rachael Heyhoe Flint', 'Betty Wilson', 'Mithali Raj', 'Belinda Clark'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'What does ODI stand for?',
            'options': ['One Day International', 'Over Day International', 'One Day India', 'Official Day International'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'What does T20 stand for?',
            'options': ['Twenty20', 'Twenty-20', 'Two Twenty', 'Twenty Twenty'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'A cricket bat is made from which wood?',
            'options': ['Teak', 'Willow', 'Oak', 'Mahogany'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The cricket pitch length is:',
            'options': ['20 yards', '21 yards', '22 yards', '23 yards'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many players are there in a cricket team?',
            'options': ['9', '10', '11', '12'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'A wicket consists of:',
            'options': ['2 stumps, 3 bails', '3 stumps, 2 bails', '3 stumps, 3 bails', '2 stumps, 2 bails'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC World Test Championship winner 2023:',
            'options': ['India', 'Australia', 'England', 'New Zealand'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who is the Australia cricket team captain?',
            'options': ['Pat Cummins', 'Steve Smith', 'David Warner', 'Mitchell Starc'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Who was India captain in ICC World Cup 2023?',
            'options': ['Virat Kohli', 'Rohit Sharma', 'Hardik Pandya', 'KL Rahul'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'ICC Awards recognize performances of which year?',
            'options': ['2022', '2023', '2024', '2021'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which cricketer won the ICC Men\'s Cricketer of the Year award for 2023?',
            'options': ['Virat Kohli', 'Pat Cummins', 'Travis Head', 'Usman Khawaja'],
            'correct': 1,
            'difficulty': 'medium'
        }
    ]
    
    # Create questions
    print("\n📝 Creating 100 Current Affairs Questions (101-200)...")
    
    created_questions = []
    for idx, q_data in enumerate(questions_data, 101):
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
    
    print(f"\n✓ Created {len(created_questions)} questions (101-200)")
    
    # Create Mock Test
    print("\n🎯 Creating Current Affairs Mock Test Part 2...")
    
    # Delete existing mock test
    MockTest.objects.filter(slug='current-affairs-mock-test-2024-part2').delete()
    
    mock_test = MockTest.objects.create(
        name='Current Affairs Mock Test 2024 - Part 2 (101-200 Questions)',
        slug='current-affairs-mock-test-2024-part2',
        exam=exam,
        description='Comprehensive mock test covering Awards, Republic Day, ICC Awards & more from 2024',
        duration_minutes=60,
        total_questions=len(created_questions),
        total_marks=len(created_questions),
        is_paid=False,
        price=0,
        attempts_allowed=10,
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
    print("✅ CURRENT AFFAIRS MOCK TEST PART 2 CREATION COMPLETED!")
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
    print("   3. Select 'Current Affairs Mock Test 2024 - Part 2 (101-200 Questions)'")
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
        create_current_affairs_mock_test_part2()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)