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

def create_current_affairs_mock_test():
    print("=" * 80)
    print("📰 CREATING CURRENT AFFAIRS MOCK TEST (100 QUESTIONS)")
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
        slug='current-affairs-2024',
        defaults={
            'name': 'Current Affairs 2024 - Part 1',
            'short_name': 'CA 2024',
            'category': exam_category,
            'exam_level': 'national',
            'duration_minutes': 60,
            'total_marks': 100,
            'total_questions': 100,
            'negative_marking': False,
            'description': 'Comprehensive Current Affairs Mock Test covering 2024 events',
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
        name='Current Affairs 2024  - Part 1',
        defaults={'weightage': 100, 'order': 1}
    )
    print(f"✓ Subject: {subject.name}")
    
    # Clear existing questions for this exam
    Question.objects.filter(exam=exam).delete()
    print("✓ Cleared existing questions")
    
    # All 100 Current Affairs Questions with options
    questions_data = [
        # Q1-Q10: Golden Globe Awards
        {
            'text': 'Which film won the Best Film – Drama award at the Golden Globe Awards 2024?',
            'options': ['Barbie', 'Oppenheimer', 'Poor Things', 'Killers of the Flower Moon'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Who won the Best Director award at the Golden Globe Awards 2024?',
            'options': ['Greta Gerwig', 'Christopher Nolan', 'Martin Scorsese', 'Denis Villeneuve'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Which movie won the Best Film – Musical or Comedy category at the Golden Globe Awards 2024?',
            'options': ['Barbie', 'Wonka', 'Poor Things', 'The Holdovers'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Who won the Best Actor – Drama category at the Golden Globe Awards 2024?',
            'options': ['Cillian Murphy', 'Ryan Gosling', 'Leonardo DiCaprio', 'Bradley Cooper'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Which TV series won the Best TV Series – Drama award at the Golden Globes 2024?',
            'options': ['The Crown', 'Beef', 'Succession', 'The Bear'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Which Indian cricketer received the National Sports Award 2023?',
            'options': ['Rohit Sharma', 'Mohammed Shami', 'Virat Kohli', 'Jasprit Bumrah'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who received the Major Dhyan Chand Khel Ratna Award 2023?',
            'options': ['Lakshya Sen', 'PV Sindhu', 'Satwik Sairaj Rankireddy & Chirag Shetty', 'Neeraj Chopra'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'India agreed to import how much hydroelectricity from Nepal over the next decade?',
            'options': ['5,000 MW', '8,000 MW', '10,000 MW', '12,000 MW'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which Indian minister visited Nepal and attended the 7th India-Nepal Joint Commission Meeting?',
            'options': ['Rajnath Singh', 'Amit Shah', 'S. Jaishankar', 'Nirmala Sitharaman'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The first Hindu temple in UAE was inaugurated in which city?',
            'options': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman'],
            'correct': 1,
            'difficulty': 'easy'
        },
        # Q11-Q20
        {
            'text': 'The BAPS Hindu Mandir is located in which area of Abu Dhabi?',
            'options': ['Khalifa City', 'Abu Mureikha', 'Al Ain', 'Yas Island'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'What is the full form of BAPS?',
            'options': [
                'Bochasanwasi Akhil Purushottam Sanstha',
                'Bochasanwasi Shri Akshar Purushottam Swaminarayan Sanstha',
                'Bharat Akshar Purushottam Society',
                'Bharatiya Akhil Parishad Sanstha'
            ],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'PM Modi launched projects worth how much in Lakshadweep?',
            'options': ['₹956 crore', '₹1,056 crore', '₹1,156 crore', '₹1,256 crore'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Kochi–Lakshadweep Submarine Optical Fibre Cable project cost:',
            'options': ['₹972 crore', '₹1,072 crore', '₹1,172 crore', '₹872 crore'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'PRITHVI VIGYAN Scheme is related to which field?',
            'options': ['Agriculture', 'Space Science', 'Earth Sciences', 'Defence Research'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'What is the budget allocation for PRITHVI VIGYAN Scheme?',
            'options': ['₹3,500 crore', '₹4,797 crore', '₹5,200 crore', '₹6,000 crore'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which countries jointly topped the Henley Passport Index 2024?',
            'options': [
                'USA, UK, Canada',
                'France, Germany, Italy, Japan, Singapore, Spain',
                'China, Japan, Korea',
                'Germany, Sweden, Norway'
            ],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'India ranked ____ in the Henley Passport Index 2024.',
            'options': ['75th', '78th', '80th', '85th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which cities jointly won the Cleanest City title in Swachh Survekshan Awards 2023?',
            'options': ['Indore & Bhopal', 'Surat & Ahmedabad', 'Indore & Surat', 'Pune & Indore'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Who presented the Swachh Survekshan Awards 2023?',
            'options': ['PM Narendra Modi', 'Jagdeep Dhankhar', 'Droupadi Murmu', 'Amit Shah'],
            'correct': 2,
            'difficulty': 'easy'
        },
        # Q21-Q40: Rankings, Reports & Defence
        {
            'text': 'Which country topped Global Firepower Military Rankings 2024?',
            'options': ['Russia', 'China', 'USA', 'India'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': "India's rank in Global Firepower Military Rankings 2024 was:",
            'options': ['2nd', '3rd', '4th', '5th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country ranked last (145th) in Global Firepower 2024?',
            'options': ['Iceland', 'Bhutan', 'Somalia', 'Liberia'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked second in Global Firepower 2024?',
            'options': ['China', 'India', 'Russia', 'UK'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country ranked third in Global Firepower 2024?',
            'options': ['China', 'India', 'Japan', 'UK'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won FIFA Men\'s Player of the Year 2024?',
            'options': ['Erling Haaland', 'Lionel Messi', 'Mbappe', 'Kevin De Bruyne'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'FIFA Women\'s Player of the Year 2024 was:',
            'options': ['Alexia Putellas', 'Mary Earps', 'Aitana Bonmati', 'Sam Kerr'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Men\'s Coach of the Year 2024:',
            'options': ['Xavi', 'Pep Guardiola', 'Klopp', 'Ancelotti'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Women\'s Coach of the Year 2024:',
            'options': ['Emma Hayes', 'Sarina Wiegman', 'Pia Sundhage', 'Jill Ellis'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Puskas Award 2023 winner:',
            'options': ['Lionel Messi', 'Haaland', 'Guilherme Madruga', 'Mbappe'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Men\'s Goalkeeper Award winner at FIFA Awards:',
            'options': ['Alisson', 'Ederson', 'Courtois', 'Martinez'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Best Women\'s Goalkeeper Award winner at FIFA Awards:',
            'options': ['Mary Earps', 'Endler', 'Musovic', 'Berger'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Fair Play Award was won by:',
            'options': ['Argentina Team', 'Brazil Men\'s Team', 'Spain Team', 'Germany Team'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Fan Award 2023 winner:',
            'options': ['Hugo Daniel Iniguez', 'Lionel Messi', 'Marta', 'Haaland'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country hosted the FIFA Awards ceremony?',
            'options': ['France', 'Spain', 'England', 'Germany'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which footballer won FIFA Men\'s Player award for the third time?',
            'options': ['Ronaldo', 'Messi', 'Modric', 'Mbappe'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Which club did Pep Guardiola coach when he won FIFA Coach of the Year?',
            'options': ['Arsenal', 'Barcelona', 'Manchester City', 'Bayern Munich'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Which nation won the FIFA Fair Play Award for standing against racism?',
            'options': ['Argentina', 'Brazil', 'Spain', 'Portugal'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which goalkeeper was selected in FIFA Women\'s World XI?',
            'options': ['Mary Earps', 'Berger', 'Musovic', 'Endler'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Which goalkeeper was selected in FIFA Men\'s World XI?',
            'options': ['Ederson', 'Thibaut Courtois', 'Martinez', 'Alisson'],
            'correct': 1,
            'difficulty': 'medium'
        },
        # Q41-Q60: National Affairs, Awards & Culture
        {
            'text': 'PM Modi launched commemorative stamps dedicated to which temple?',
            'options': ['Somnath Temple', 'Kedarnath Temple', 'Ram Mandir', 'Kashi Vishwanath'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'How many commemorative Ram Mandir stamps were released?',
            'options': ['4', '5', '6', '8'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Ram Mandir is located in which city?',
            'options': ['Mathura', 'Varanasi', 'Ayodhya', 'Prayagraj'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Ram Mandir Pran Pratishtha was held on which date?',
            'options': ['14 January 2024', '22 January 2024', '26 January 2024', '1 February 2024'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The Ram Lalla idol was sculpted by:',
            'options': ['Sudarsan Pattnaik', 'Arun Yogiraj', 'Ram Sutar', 'Adwaita Gadanayak'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Lalla idol height is:',
            'options': ['41 inches', '45 inches', '51 inches', '61 inches'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which style of architecture is used in Ram Mandir?',
            'options': ['Dravidian', 'Indo-Islamic', 'Nagara', 'Vesara'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'How many dignitaries attended Ram Mandir inauguration?',
            'options': ['5,000+', '6,000+', '7,000+', '10,000+'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Pradhan Mantri Rashtriya Bal Puraskar 2024 honoured how many children?',
            'options': ['15', '17', '19', '21'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Pradhan Mantri Rashtriya Bal Puraskar was presented by:',
            'options': ['Prime Minister', 'Vice President', 'President Droupadi Murmu', 'Home Minister'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'ICC Men\'s Cricketer of the Year 2023:',
            'options': ['Virat Kohli', 'Travis Head', 'Pat Cummins', 'Rohit Sharma'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'ICC Men\'s ODI Cricketer of the Year 2023:',
            'options': ['Rohit Sharma', 'Virat Kohli', 'Shubman Gill', 'Travis Head'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Men\'s Test Cricketer of the Year 2023:',
            'options': ['Joe Root', 'Travis Head', 'Usman Khawaja', 'Ashwin'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Women\'s Cricketer of the Year 2023:',
            'options': ['Hayley Matthews', 'Nat Sciver-Brunt', 'Meg Lanning', 'Perry'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Women\'s ODI Cricketer of the Year 2023:',
            'options': ['Chamari Athapaththu', 'Perry', 'Gardner', 'Matthews'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s Associate Cricketer of the Year 2023:',
            'options': ['Bas de Leede', 'Suryakumar Yadav', 'Ravindra', 'Coetzee'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Women\'s Associate Cricketer of the Year 2023:',
            'options': ['Marufa Akter', 'Queentor Abel', 'Darcey Carter', 'Bell'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'ICC Men\'s T20I Cricketer of the Year 2023:',
            'options': ['Rohit Sharma', 'Hardik Pandya', 'Suryakumar Yadav', 'Gill'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Women\'s T20I Cricketer of the Year 2023:',
            'options': ['Hayley Matthews', 'Perry', 'Gardner', 'Healy'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'ICC Men\'s Emerging Cricketer of the Year 2023:',
            'options': ['Yashasvi Jaiswal', 'Gerald Coetzee', 'Rachin Ravindra', 'Dilshan Madushanka'],
            'correct': 2,
            'difficulty': 'hard'
        },
        # Q61-Q80
        {
            'text': 'Republic Day is celebrated on which date?',
            'options': ['15 August', '26 January', '2 October', '14 November'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day 2024 was India\'s:',
            'options': ['74th', '75th', '76th', '77th'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Republic Day 2024 chief guest was:',
            'options': ['Joe Biden', 'Rishi Sunak', 'Emmanuel Macron', 'Olaf Scholz'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Republic Day 2024 theme was:',
            'options': ['New India', 'Viksit Bharat', 'Digital Bharat', 'Ek Bharat'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who was the President of France in 2024?',
            'options': ['Emmanuel Macron', 'Francois Hollande', 'Nicolas Sarkozy', 'Jacques Chirac'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'What is the capital of Nepal?',
            'options': ['Kathmandu', 'Pokhara', 'Biratnagar', 'Lalitpur'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Current electricity capacity of Nepal mentioned in the report:',
            'options': ['2,200 MW', '2,600 MW', '3,000 MW', '3,500 MW'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Long-term power export target of Nepal to India:',
            'options': ['5,000 MW', '8,000 MW', '10,000 MW', '12,000 MW'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'World\'s largest cleanliness survey is:',
            'options': ['Clean India Survey', 'Swachh Survekshan', 'Sanitation India', 'Clean City Survey'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Number of urban local bodies in Swachh Survekshan 2023:',
            'options': ['3,447', '4,447', '5,447', '6,447'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Safaimitra Surakshit Sheher award winner:',
            'options': ['Mumbai', 'Delhi', 'Chandigarh', 'Ahmedabad'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Performing State in Swachh Survekshan 2023:',
            'options': ['Gujarat', 'Maharashtra', 'Tamil Nadu', 'Karnataka'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Cleanest Cantonment Board in Swachh Survekshan 2023:',
            'options': ['Mhow Cantonment Board', 'Pune Cantonment', 'Delhi Cantonment', 'Jaipur Cantonment'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Cleanest Ganga Town award winner:',
            'options': ['Haridwar', 'Rishikesh', 'Varanasi', 'Patna'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'India\'s passport ranking in Henley Passport Index 2024:',
            'options': ['75th', '78th', '80th', '85th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Most powerful passport provides access to how many destinations?',
            'options': ['184', '190', '194', '198'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country shares Rank 1 with Japan in Henley Passport Index?',
            'options': ['Singapore', 'South Korea', 'Germany', 'Spain'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'FIFA Special Award winner for 2023 was:',
            'options': ['Marta', 'Messi', 'Haaland', 'Mbappe'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Lalla idol color is:',
            'options': ['White', 'Black', 'Brown', 'Golden'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Ram Mandir temple height is:',
            'options': ['141 feet', '151 feet', '161 feet', '171 feet'],
            'correct': 2,
            'difficulty': 'hard'
        },
        # Q81-Q100
        {
            'text': 'Ram Mandir temple length is:',
            'options': ['360 feet', '380 feet', '400 feet', '420 feet'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ram Mandir temple width is:',
            'options': ['230 feet', '250 feet', '270 feet', '290 feet'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Republic Day 2024 second theme was:',
            'options': ['Bharat-Navnirman', 'Bharat-Loktantra ki Matruka', 'Bharat-Viksit', 'Bharat-Aatmanirbhar'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Constitution of India came into force on:',
            'options': ['26 Jan 1950', '26 Jan 1949', '15 Aug 1950', '15 Aug 1949'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Drafting Committee Chairman of Indian Constitution:',
            'options': ['Mahatma Gandhi', 'Dr. B.R. Ambedkar', 'Jawaharlal Nehru', 'Sardar Patel'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Global Firepower rank of Pakistan:',
            'options': ['7th', '8th', '9th', '10th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country has the most powerful passport in the world?',
            'options': ['Japan', 'Singapore', 'Germany', 'Spain'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'The Ram Mandir complex covers an area of approximately:',
            'options': ['60 acres', '70 acres', '80 acres', '90 acres'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The BAPS Hindu Mandir in Abu Dhabi was built on land donated by:',
            'options': ['UAE Government', 'Indian Government', 'BAPS Trust', 'Private Donors'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The submarine optical fibre cable will provide internet connectivity to:',
            'options': ['Andaman & Nicobar', 'Lakshadweep', 'Kerala Coast', 'Goa'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which country hosted the 2024 FIFA Awards ceremony?',
            'options': ['France', 'Spain', 'England', 'Germany'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Ram Mandir Pran Pratishtha ceremony was attended by how many VVIPs?',
            'options': ['5,000', '7,000', '10,000', '12,000'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The PRITHVI VIGYAN scheme is under which ministry?',
            'options': ['Ministry of Defence', 'Ministry of Earth Sciences', 'Ministry of Space', 'Ministry of Agriculture'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The Kochi-Lakshadweep optical fibre cable will provide internet speed of:',
            'options': ['50 Gbps', '100 Gbps', '150 Gbps', '200 Gbps'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The total length of the Kochi-Lakshadweep optical fibre cable is:',
            'options': ['1,468 km', '1,568 km', '1,668 km', '1,868 km'],
            'correct': 3,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country is the largest producer of hydroelectricity in South Asia?',
            'options': ['India', 'Nepal', 'Bhutan', 'Pakistan'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'The 7th India-Nepal Joint Commission Meeting was held in which city?',
            'options': ['New Delhi', 'Kathmandu', 'Mumbai', 'Pokhara'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'The Swachh Survekshan 2023 covered how many cities?',
            'options': ['3,500+', '4,000+', '4,447+', '5,000+'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The FIFA Puskas Award 2023 was won by which player?',
            'options': ['Lionel Messi', 'Guilherme Madruga', 'Haaland', 'Mbappe'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The BAPS Hindu Mandir in Abu Dhabi was inaugurated on which date?',
            'options': ['14 February 2024', '22 January 2024', '26 January 2024', '15 August 2024'],
            'correct': 0,
            'difficulty': 'medium'
        }
    ]
    
    # Create questions
    print("\n📝 Creating 100 Current Affairs Questions...")
    
    created_questions = []
    for idx, q_data in enumerate(questions_data, 1):
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
            print(f"   ✓ Created {idx} questions...")
    
    print(f"\n✓ Created {len(created_questions)} questions")
    
    # Create Mock Test
    print("\n🎯 Creating Current Affairs Mock Test...")
    
    # Delete existing mock test
    MockTest.objects.filter(slug='current-affairs-mock-test-2024').delete()
    
    mock_test = MockTest.objects.create(
        name='Current Affairs Mock Test 2024 - Part 1 (1- 100 Questions)',
        slug='current-affairs-mock-test-2024',
        exam=exam,
        description='Comprehensive mock test covering all major Current Affairs events of 2024',
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
    print("✅ CURRENT AFFAIRS MOCK TEST CREATION COMPLETED!")
    print("=" * 80)
    
    print("\n📊 SUMMARY:")
    print(f"   • Exam Category: {exam_category.name}")
    print(f"   • Exam: {exam.name}")
    print(f"   • Subject: {subject.name}")
    print(f"   • Questions Created: {len(created_questions)}")
    print(f"   • Mock Test: {mock_test.name}")
    print(f"   • Total Questions in Mock Test: {MockTestQuestion.objects.filter(mock_test=mock_test).count()}")
    
    print("\n🎯 To take the mock test:")
    print("   1. Login to the application")
    print("   2. Go to Mock Tests section")
    print("   3. Select 'Current Affairs Mock Test 2024 (100 Questions)'")
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
        create_current_affairs_mock_test()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)