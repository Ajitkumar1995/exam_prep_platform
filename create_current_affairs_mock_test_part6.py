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

def create_current_affairs_mock_test_part6():
    print("=" * 80)
    print("📰 CREATING CURRENT AFFAIRS MOCK TEST PART 6 (QUESTIONS 501-600)")
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
        slug='current-affairs-2024-part6',
        defaults={
            'name': 'Current Affairs 2024 - Part 6',
            'short_name': 'CA 2024 P6',
            'category': exam_category,
            'exam_level': 'national',
            'duration_minutes': 60,
            'total_marks': 100,
            'total_questions': 100,
            'negative_marking': False,
            'description': 'Comprehensive Current Affairs Mock Test Part 6 covering Ram Mandir, Bal Puraskar, ICC Awards & Republic Day 2024',
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
        name='Current Affairs 2024 - Part 6',
        defaults={'weightage': 100, 'order': 1}
    )
    print(f"✓ Subject: {subject.name}")
    
    # Clear existing questions for this exam
    Question.objects.filter(exam=exam).delete()
    print("✓ Cleared existing questions")
    
    # All 100 Current Affairs Questions (501-600)
    questions_data = [
        # Q501-Q525: Ram Mandir & Ayodhya
        {
            'text': 'Ram Mandir was inaugurated on which date?',
            'options': ['14 January 2024', '22 January 2024', '26 January 2024', '1 February 2024'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Ram Mandir is located in which city?',
            'options': ['Mathura', 'Varanasi', 'Ayodhya', 'Prayagraj'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The Pran Pratishtha ceremony was led by whom?',
            'options': ['Yogi Adityanath', 'Mohan Bhagwat', 'Narendra Modi', 'Droupadi Murmu'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Ram Lalla idol was sculpted by whom?',
            'options': ['Ram Sutar', 'Arun Yogiraj', 'Sudarsan Pattnaik', 'Adwaita Gadanayak'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'What is the height of Ram Lalla idol?',
            'options': ['41 inches', '45 inches', '51 inches', '61 inches'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Lalla idol depicts Lord Ram as what age?',
            'options': ['Infant', 'Five-year-old child', 'Teenager', 'Adult king'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Mandir architecture style is:',
            'options': ['Dravidian', 'Vesara', 'Nagara', 'Indo-Islamic'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'What is the height of Ram Mandir?',
            'options': ['141 feet', '151 feet', '161 feet', '171 feet'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'What is the length of Ram Mandir?',
            'options': ['360 feet', '380 feet', '400 feet', '420 feet'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'What is the width of Ram Mandir?',
            'options': ['230 feet', '250 feet', '270 feet', '290 feet'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Mandir is located in which state?',
            'options': ['Madhya Pradesh', 'Uttar Pradesh', 'Uttarakhand', 'Rajasthan'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Ram Mandir is situated on the banks of which river?',
            'options': ['Ganga', 'Yamuna', 'Saryu', 'Godavari'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'What is the color of Ram Lalla idol?',
            'options': ['White', 'Black', 'Brown', 'Golden'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'What is the consecration ceremony called?',
            'options': ['Pran Pratishtha', 'Puja', 'Abhishek', 'Yagna'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Which Prime Minister was present at the Ram Mandir inauguration?',
            'options': ['Narendra Modi', 'Manmohan Singh', 'Atal Bihari Vajpayee', 'Indira Gandhi'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'How many dignitaries attended the Ram Mandir inauguration?',
            'options': ['5,000+', '6,000+', '7,000+', '10,000+'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Ram Lalla idol sculptor belongs to which state?',
            'options': ['Karnataka', 'Tamil Nadu', 'Kerala', 'Andhra Pradesh'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Lalla idol was installed on which date?',
            'options': ['15 January 2024', '18 January 2024', '20 January 2024', '22 January 2024'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Mandir is dedicated to which deity?',
            'options': ['Lord Shiva', 'Lord Vishnu', 'Lord Ram', 'Lord Krishna'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Ram Mandir is located in which city?',
            'options': ['Mathura', 'Varanasi', 'Ayodhya', 'Prayagraj'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'What is the sanctum of Ram Mandir called?',
            'options': ['Garbhagriha', 'Sabha Mandap', 'Rang Mandap', 'Yagya Mandap'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Mandir is built in which architectural style?',
            'options': ['Dravidian', 'Vesara', 'Nagara', 'Indo-Islamic'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Mandir height is how many feet?',
            'options': ['141 feet', '151 feet', '161 feet', '171 feet'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Mandir length is how many feet?',
            'options': ['360 feet', '380 feet', '400 feet', '420 feet'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The Ram Mandir width is how many feet?',
            'options': ['230 feet', '250 feet', '270 feet', '290 feet'],
            'correct': 1,
            'difficulty': 'hard'
        },
        # Q526-Q550: Pradhan Mantri Rashtriya Bal Puraskar 2024
        {
            'text': 'How many children were awarded PMRBP 2024?',
            'options': ['15', '17', '19', '21'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The PMRBP 2024 awards were presented by whom?',
            'options': ['Prime Minister', 'President Droupadi Murmu', 'Vice President', 'Home Minister'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The PMRBP 2024 award ceremony venue was:',
            'options': ['Bharat Mandapam', 'Vigyan Bhawan', 'Rashtrapati Bhavan', 'Parliament House'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Aaditya Vijay Bramhane received PMRBP 2024 in which category?',
            'options': ['Sports', 'Bravery', 'Innovation', 'Social Service'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Suhani Chauhan received PMRBP 2024 in which category?',
            'options': ['Innovation', 'Sports', 'Art & Culture', 'Science'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Aryan Singh received PMRBP 2024 in which category?',
            'options': ['Sports', 'Innovation', 'Science & Technology', 'Social Service'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Avnish Tiwari received PMRBP 2024 in which category?',
            'options': ['Social Service', 'Sports', 'Bravery', 'Art & Culture'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Aaditya Yadav received PMRBP 2024 in which category?',
            'options': ['Sports', 'Innovation', 'Bravery', 'Art & Culture'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Charvi A who received PMRBP 2024 belongs to which state?',
            'options': ['Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Linthoi Chanambam who received PMRBP 2024 belongs to which state?',
            'options': ['Assam', 'Manipur', 'Mizoram', 'Tripura'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'PMRBP stands for:',
            'options': ['Pradhan Mantri Rashtriya Bal Puraskar', 'Prime Minister\'s Rashtriya Bal Puraskar', 'Pradhan Mantri Bal Puraskar', 'Pradhan Mantri Rashtriya Bal Award'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'PMRBP 2024 was awarded in which year?',
            'options': ['2023', '2024', '2025', '2022'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'How many total awardees were there in PMRBP 2024?',
            'options': ['15', '17', '19', '21'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'How many boys received PMRBP 2024?',
            'options': ['7', '8', '9', '10'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many girls received PMRBP 2024?',
            'options': ['8', '9', '10', '11'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many States/UTs were represented in PMRBP 2024?',
            'options': ['16', '17', '18', '19'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Who received PMRBP 2024 in Innovation category?',
            'options': ['Suhani Chauhan', 'Aryan Singh', 'Avnish Tiwari', 'Aaditya Yadav'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Who received PMRBP 2024 in Science & Technology category?',
            'options': ['Suhani Chauhan', 'Aryan Singh', 'Avnish Tiwari', 'Aaditya Yadav'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who received PMRBP 2024 in Bravery category?',
            'options': ['Aaditya Vijay Bramhane', 'Aryan Singh', 'Avnish Tiwari', 'Aaditya Yadav'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'How many awardees were in Sports category?',
            'options': ['3', '4', '5', '6'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many awardees were in Social Service category?',
            'options': ['2', '3', '4', '5'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many awardees were in Art & Culture category?',
            'options': ['5', '6', '7', '8'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The President of India who presented PMRBP 2024 was:',
            'options': ['Droupadi Murmu', 'Ram Nath Kovind', 'Pranab Mukherjee', 'Pratibha Patil'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'PM interaction with PMRBP awardees was held on which date?',
            'options': ['21 January 2024', '22 January 2024', '23 January 2024', '24 January 2024'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'PMRBP awardees participated in which event?',
            'options': ['Independence Day', 'Republic Day', 'Gandhi Jayanti', 'Constitution Day'],
            'correct': 1,
            'difficulty': 'medium'
        },
        # Q551-Q575: ICC Awards 2023
        {
            'text': 'ICC Men\'s Cricketer of the Year 2023 was:',
            'options': ['Virat Kohli', 'Pat Cummins', 'Rohit Sharma', 'Travis Head'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'ICC Men\'s ODI Cricketer of the Year 2023 was:',
            'options': ['Virat Kohli', 'Shubman Gill', 'Rohit Sharma', 'Travis Head'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Men\'s Test Cricketer of the Year 2023 was:',
            'options': ['Joe Root', 'Usman Khawaja', 'Ravichandran Ashwin', 'Travis Head'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Women\'s Cricketer of the Year 2023 was:',
            'options': ['Hayley Matthews', 'Nat Sciver-Brunt', 'Ellyse Perry', 'Ashleigh Gardner'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Women\'s ODI Cricketer of the Year 2023 was:',
            'options': ['Hayley Matthews', 'Ellyse Perry', 'Chamari Athapaththu', 'Ashleigh Gardner'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s Associate Cricketer of the Year 2023 was:',
            'options': ['Bas de Leede', 'Gerald Coetzee', 'Yashasvi Jaiswal', 'Rachin Ravindra'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Women\'s Associate Cricketer of the Year 2023 was:',
            'options': ['Marufa Akter', 'Queentor Abel', 'Michael Bell', 'Darcey Carter'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s T20I Cricketer of the Year 2023 was:',
            'options': ['Rohit Sharma', 'Shubman Gill', 'Suryakumar Yadav', 'Hardik Pandya'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Women\'s T20I Cricketer of the Year 2023 was:',
            'options': ['Hayley Matthews', 'Ellyse Perry', 'Ashleigh Gardner', 'Michael Bell'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Men\'s Emerging Cricketer of the Year 2023 was:',
            'options': ['Yashasvi Jaiswal', 'Rachin Ravindra', 'Gerald Coetzee', 'Dilshan Madushanka'],
            'correct': 1,
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
            'text': 'Rachin Ravindra represents which country?',
            'options': ['India', 'Australia', 'New Zealand', 'South Africa'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC headquarters is located in which city?',
            'options': ['London', 'Dubai', 'Sydney', 'Mumbai'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ODI World Cup 2023 was won by which country?',
            'options': ['India', 'Australia', 'England', 'New Zealand'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'ODI World Cup 2023 runner-up was which country?',
            'options': ['India', 'Australia', 'England', 'South Africa'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Player of Tournament in ODI World Cup 2023 was:',
            'options': ['Rohit Sharma', 'Virat Kohli', 'Pat Cummins', 'Travis Head'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC was founded in which year?',
            'options': ['1909', '1919', '1929', '1939'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s Cricketer of the Year trophy is named after:',
            'options': ['Sir Garfield Sobers', 'Don Bradman', 'Jack Hobbs', 'Viv Richards'],
            'correct': 0,
            'difficulty': 'hard'
        },
        # Q576-Q600: Republic Day 2024
        {
            'text': 'Republic Day 2024 was India\'s which Republic Day?',
            'options': ['73rd', '74th', '75th', '76th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Republic Day is celebrated on which date?',
            'options': ['15 August', '26 January', '2 October', '14 November'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Chief Guest of Republic Day 2024 was:',
            'options': ['Joe Biden', 'Rishi Sunak', 'Emmanuel Macron', 'Olaf Scholz'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Theme of Republic Day 2024 was:',
            'options': ['New India', 'Viksit Bharat', 'Digital Bharat', 'Swachh Bharat'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Second theme of Republic Day 2024 was:',
            'options': ['Bharat Mata', 'Bharat-Loktantra ki Matruka', 'Ek Bharat', 'Atmanirbhar Bharat'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The Constitution of India came into force on:',
            'options': ['15 Aug 1947', '26 Nov 1949', '26 Jan 1950', '24 Jan 1950'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Chairman of the Drafting Committee of the Constitution was:',
            'options': ['Jawaharlal Nehru', 'Sardar Patel', 'B.R. Ambedkar', 'Rajendra Prasad'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day parade is held in which city?',
            'options': ['Mumbai', 'New Delhi', 'Kolkata', 'Chennai'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The President of France in 2024 was:',
            'options': ['Nicolas Sarkozy', 'Emmanuel Macron', 'Francois Hollande', 'Jacques Chirac'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day celebrates what occasion?',
            'options': ['Independence', 'Constitution enforcement', 'Gandhi Jayanti', 'Formation of Parliament'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The Constitution was adopted on which date?',
            'options': ['15 Aug 1947', '26 Nov 1949', '26 Jan 1950', '24 Jan 1950'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who is known as the Father of Indian Constitution?',
            'options': ['Mahatma Gandhi', 'Jawaharlal Nehru', 'B.R. Ambedkar', 'Sardar Patel'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Who was India\'s first President?',
            'options': ['Jawaharlal Nehru', 'Dr. Rajendra Prasad', 'Sardar Patel', 'B.R. Ambedkar'],
            'correct': 1,
            'difficulty': 'easy'
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
            'text': 'The Chief Guest for Republic Day 2024 was from which country?',
            'options': ['USA', 'UK', 'France', 'Germany'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The theme of Republic Day 2024 was:',
            'options': ['New India', 'Viksit Bharat', 'Digital Bharat', 'Swachh Bharat'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Republic Day is celebrated in which month?',
            'options': ['August', 'October', 'January', 'November'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Constitution Day is observed on which date?',
            'options': ['15 August', '26 January', '26 November', '2 October'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'India became a Sovereign Democratic Republic in which year?',
            'options': ['1947', '1949', '1950', '1952'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Republic Day significance is:',
            'options': ['Independence from British rule', 'Constitution came into force', 'First President took office', 'First Prime Minister took office'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Republic Day 2024 was celebrated on which date?',
            'options': ['22 January 2024', '24 January 2024', '26 January 2024', '28 January 2024'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day 2024 was the how many Republic Day of India?',
            'options': ['73rd', '74th', '75th', '76th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Constitution of India was adopted by the Constituent Assembly on:',
            'options': ['15 Aug 1947', '26 Nov 1949', '26 Jan 1950', '24 Jan 1950'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The Drafting Committee of the Constitution had how many members?',
            'options': ['5', '6', '7', '8'],
            'correct': 2,
            'difficulty': 'hard'
        }
    ]
    
    # Create questions
    print("\n📝 Creating 100 Current Affairs Questions (501-600)...")
    
    created_questions = []
    for idx, q_data in enumerate(questions_data, 501):
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
    
    print(f"\n✓ Created {len(created_questions)} questions (501-600)")
    
    # Create Mock Test
    print("\n🎯 Creating Current Affairs Mock Test Part 6...")
    
    # Delete existing mock test
    MockTest.objects.filter(slug='current-affairs-mock-test-2024-part6').delete()
    
    mock_test = MockTest.objects.create(
        name='Current Affairs Mock Test 2024 - Part 6 (501-600 Questions)',
        slug='current-affairs-mock-test-2024-part6',
        exam=exam,
        description='Comprehensive mock test covering Ram Mandir, Bal Puraskar, ICC Awards & Republic Day 2024',
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
    print("✅ CURRENT AFFAIRS MOCK TEST PART 6 CREATION COMPLETED!")
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
    print("   3. Select 'Current Affairs Mock Test 2024 - Part 6 (501-600 Questions)'")
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
        create_current_affairs_mock_test_part6()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)