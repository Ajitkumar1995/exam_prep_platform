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

def create_all_mock_tests():
    print("=" * 80)
    print("📰 CREATING 5 CURRENT AFFAIRS MOCK TESTS (500 UNIQUE QUESTIONS)")
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
    
    # Delete all existing current affairs mock tests and questions
    print("\n🗑️ Cleaning up existing data...")
    MockTestQuestion.objects.filter(mock_test__exam__category=exam_category).delete()
    MockTest.objects.filter(exam__category=exam_category).delete()
    Question.objects.filter(exam__category=exam_category).delete()
    Subject.objects.filter(exam__category=exam_category).delete()
    Exam.objects.filter(category=exam_category).delete()
    print("✓ Cleanup complete")
    
    # ===== PART 1: Questions 1-100 =====
    part1_questions = [
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

    # ===== PART 2: Questions 101-200 =====
    part2_questions = [
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
        }
    ]

    # ===== PART 3: Questions 201-300 =====
    part3_questions = [
        # Q201-Q225: National Sports Awards 2023
        {
            'text': 'Which cricketer received the National Sports Award 2023?',
            'options': ['Rohit Sharma', 'Virat Kohli', 'Mohammed Shami', 'KL Rahul'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Pawan Sehrawat is associated with which sport?',
            'options': ['Wrestling', 'Kabaddi', 'Hockey', 'Athletics'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Vaishali Rameshbabu is associated with which sport?',
            'options': ['Chess', 'Tennis', 'Shooting', 'Archery'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Murali Sreeshankar belongs to which sport?',
            'options': ['Cricket', 'Athletics', 'Hockey', 'Wrestling'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Krishan Bahadur Pathak is associated with which sport?',
            'options': ['Football', 'Hockey', 'Kabaddi', 'Boxing'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Sunil Kumar received the National Sports Award in which sport?',
            'options': ['Wrestling', 'Boxing', 'Shooting', 'Athletics'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Aditi Gopichand Swami belongs to which sport?',
            'options': ['Archery', 'Shooting', 'Tennis', 'Golf'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Mohammad Hussamuddin is associated with which sport?',
            'options': ['Wrestling', 'Boxing', 'Hockey', 'Athletics'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Esha Singh is related to which sport?',
            'options': ['Archery', 'Shooting', 'Tennis', 'Golf'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Diksha Dagar is associated with which sport?',
            'options': ['Golf', 'Tennis', 'Athletics', 'Shooting'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Sheetal Devi belongs to which sport?',
            'options': ['Para-Archery', 'Para-Athletics', 'Para-Swimming', 'Para-Shooting'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Prachi Yadav is associated with which sport?',
            'options': ['Para Canoeing', 'Para Archery', 'Para Athletics', 'Para Swimming'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Harinder Pal Sandhu belongs to which sport?',
            'options': ['Tennis', 'Squash', 'Golf', 'Hockey'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Nasreen Shaikh is associated with which sport?',
            'options': ['Kho-Kho', 'Kabaddi', 'Athletics', 'Wrestling'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Pinki Singh received the National Sports Award in which sport?',
            'options': ['Lawn Bowls', 'Golf', 'Squash', 'Chess'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'RB Ramesh received the Dronacharya Award for which sport?',
            'options': ['Athletics', 'Chess', 'Hockey', 'Wrestling'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Shivendra Singh received the Dronacharya Award in which sport?',
            'options': ['Kabaddi', 'Hockey', 'Boxing', 'Athletics'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Ganesh Prabhakaran is a coach in which sport?',
            'options': ['Mallakhamb', 'Wrestling', 'Hockey', 'Cricket'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Mahavir Saini received the Dronacharya Award for which sport?',
            'options': ['Para Athletics', 'Hockey', 'Kabaddi', 'Boxing'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Lalit Kumar received the Dronacharya Award in which sport?',
            'options': ['Wrestling', 'Chess', 'Hockey', 'Archery'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Dhyan Chand Lifetime Award winner Kavita belongs to which sport?',
            'options': ['Hockey', 'Kabaddi', 'Boxing', 'Athletics'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Manjusha Kanwar received the Dhyan Chand Lifetime Award for which sport?',
            'options': ['Tennis', 'Badminton', 'Chess', 'Shooting'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Vineet Kumar Sharma belongs to which sport?',
            'options': ['Hockey', 'Football', 'Cricket', 'Wrestling'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'MAKA Trophy 2023 winner was which university?',
            'options': ['Delhi University', 'Guru Nanak Dev University', 'Panjab University', 'Kurukshetra University'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'MAKA Trophy 2023 first runner-up was which university?',
            'options': ['Lovely Professional University', 'Delhi University', 'BHU', 'JNU'],
            'correct': 0,
            'difficulty': 'hard'
        },
        # Q226-Q250: Emmy Awards 2024
        {
            'text': 'Emmy Award 2024 for Drama Series was won by which show?',
            'options': ['Beef', 'Succession', 'The Bear', 'The Crown'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Emmy Award 2024 for Comedy Series was won by which show?',
            'options': ['The Crown', 'Beef', 'The Bear', 'Wednesday'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won Lead Actress in Drama Series at Emmy Awards 2024?',
            'options': ['Sarah Snook', 'Jennifer Coolidge', 'Ali Wong', 'Emma Stone'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won Lead Actor in Drama Series at Emmy Awards 2024?',
            'options': ['Kieran Culkin', 'Pedro Pascal', 'Jeremy Allen White', 'Steven Yeun'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Which show won the Limited or Anthology Series at Emmy Awards 2024?',
            'options': ['The Bear', 'Beef', 'Succession', 'The Crown'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won Lead Actress in Limited Series at Emmy Awards 2024?',
            'options': ['Ali Wong', 'Sarah Snook', 'Emma Stone', 'Ayo Edebiri'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won Lead Actor in Limited Series at Emmy Awards 2024?',
            'options': ['Steven Yeun', 'Kieran Culkin', 'Paul Walter Hauser', 'Jeremy Allen White'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Outstanding Competition Program winner at Emmy Awards 2024 was:',
            'options': ['The Voice', 'RuPaul\'s Drag Race', 'Big Brother', 'Survivor'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Talk Series winner at Emmy Awards 2024 was:',
            'options': ['Jimmy Kimmel Live', 'The Daily Show with Trevor Noah', 'Tonight Show', 'Late Night Show'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won Writing for Comedy Series at Emmy Awards 2024?',
            'options': ['Christopher Storer', 'Jesse Armstrong', 'Lee Sung Jin', 'Mark Mylod'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won Lead Actor in Comedy Series at Emmy Awards 2024?',
            'options': ['Jeremy Allen White', 'Steve Martin', 'Martin Short', 'Jason Sudeikis'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won Lead Actress in Comedy Series at Emmy Awards 2024?',
            'options': ['Jennifer Coolidge', 'Quinta Brunson', 'Sarah Snook', 'Ali Wong'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won Supporting Actress in Comedy Series at Emmy Awards 2024?',
            'options': ['Ayo Edebiri', 'Emma Stone', 'Ali Wong', 'Sarah Snook'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won Supporting Actor in Drama Series at Emmy Awards 2024?',
            'options': ['Matthew Macfadyen', 'Kieran Culkin', 'Steven Yeun', 'Mark Mylod'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won Supporting Actress in Drama Series at Emmy Awards 2024?',
            'options': ['Jennifer Coolidge', 'Sarah Snook', 'Ali Wong', 'Ayo Edebiri'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Which show won the Comedy Series at Emmy Awards 2024?',
            'options': ['The Crown', 'Beef', 'The Bear', 'Succession'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which show won the Drama Series at Emmy Awards 2024?',
            'options': ['Beef', 'Succession', 'The Bear', 'The Crown'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Which show won the Anthology Series at Emmy Awards 2024?',
            'options': ['The Bear', 'Beef', 'Succession', 'The Crown'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Variety Special (Live) winner at Emmy Awards 2024 was:',
            'options': ['Elton John Live: Farewell from Dodger Stadium', 'Taylor Swift Special', 'Beyonce Special', 'Adele Special'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Supporting Actor in Drama Series winner at Emmy Awards 2024 was:',
            'options': ['Matthew Macfadyen', 'Kieran Culkin', 'Steven Yeun', 'Mark Mylod'],
            'correct': 0,
            'difficulty': 'hard'
        },
        # Q251-Q300: Important Current Affairs January 2024
        {
            'text': 'Which movie received the Cinematic and Box Office Achievement award at Golden Globes 2024?',
            'options': ['Oppenheimer', 'Barbie', 'Poor Things', 'Wonka'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Best Original Song at Golden Globes 2024 was:',
            'options': ['Dance the Night', 'What Was I Made For?', 'I\'m Just Ken', 'Lift Me Up'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Original Score winner at Golden Globes 2024 was:',
            'options': ['Hans Zimmer', 'Ludwig Göransson', 'John Williams', 'AR Rahman'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Animated Film winner at Golden Globes 2024 was:',
            'options': ['Spider-Man', 'Elemental', 'The Boy and the Heron', 'Wish'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Best Non-English Language Film winner at Golden Globes 2024 was:',
            'options': ['Past Lives', 'Society of the Snow', 'Anatomy of a Fall', 'Perfect Days'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Screenplay winner at Golden Globes 2024 was:',
            'options': ['Christopher Nolan', 'Justine Triet & Arthur Harari', 'Greta Gerwig', 'Martin Scorsese'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Supporting Actor at Golden Globes 2024 was won by:',
            'options': ['Robert Downey Jr.', 'Ryan Gosling', 'Mark Ruffalo', 'Willem Dafoe'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Best Supporting Actress at Golden Globes 2024 was won by:',
            'options': ['Emma Stone', 'Margot Robbie', 'Da\'Vine Joy Randolph', 'Lily Gladstone'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Which film received 9 nominations at Golden Globes 2024?',
            'options': ['Oppenheimer', 'Barbie', 'Killers of the Flower Moon', 'Poor Things'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Golden Globe Awards 2024 was the:',
            'options': ['79th', '80th', '81st', '82nd'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Venue of Golden Globes 2024 was:',
            'options': ['Beverly Hilton', 'Hollywood Bowl', 'Dolby Theatre', 'Madison Square Garden'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'City of Golden Globes 2024 was:',
            'options': ['Los Angeles', 'Beverly Hills', 'Hollywood', 'New York'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Best Actress Drama at Golden Globes 2024 was won by:',
            'options': ['Lily Gladstone', 'Emma Stone', 'Margot Robbie', 'Carey Mulligan'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Actor Comedy at Golden Globes 2024 was won by:',
            'options': ['Paul Giamatti', 'Ryan Gosling', 'Joaquin Phoenix', 'Nicolas Cage'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Actress Comedy at Golden Globes 2024 was won by:',
            'options': ['Emma Stone', 'Margot Robbie', 'Natalie Portman', 'Jennifer Lawrence'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Director at Golden Globes 2024 was won by:',
            'options': ['Christopher Nolan', 'Greta Gerwig', 'Martin Scorsese', 'Denis Villeneuve'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Best TV Musical/Comedy at Golden Globes 2024 was won by:',
            'options': ['The Bear', 'Beef', 'Succession', 'The Crown'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Best Limited Series at Golden Globes 2024 was won by:',
            'options': ['The Bear', 'Beef', 'Succession', 'The Crown'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Best TV Actress Drama at Golden Globes 2024 was won by:',
            'options': ['Sarah Snook', 'Jennifer Coolidge', 'Ali Wong', 'Ayo Edebiri'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best TV Actor Drama at Golden Globes 2024 was won by:',
            'options': ['Kieran Culkin', 'Pedro Pascal', 'Jeremy Allen White', 'Steven Yeun'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best TV Actress Comedy at Golden Globes 2024 was won by:',
            'options': ['Ayo Edebiri', 'Jennifer Coolidge', 'Quinta Brunson', 'Sarah Snook'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best TV Actor Comedy at Golden Globes 2024 was won by:',
            'options': ['Jeremy Allen White', 'Steve Martin', 'Martin Short', 'Jason Sudeikis'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Best Stand-up Comedy on TV at Golden Globes 2024 was won by:',
            'options': ['Ricky Gervais', 'Dave Chappelle', 'Chris Rock', 'Jerry Seinfeld'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Ricky Gervais special name at Golden Globes 2024 was:',
            'options': ['Armageddon', 'SuperNature', 'Humanity', 'After Life'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Oppenheimer lead actor was:',
            'options': ['Cillian Murphy', 'Robert Downey Jr.', 'Matt Damon', 'Emily Blunt'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Oppenheimer director was:',
            'options': ['Christopher Nolan', 'Martin Scorsese', 'Greta Gerwig', 'Denis Villeneuve'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Barbie lead actress was:',
            'options': ['Margot Robbie', 'Emma Stone', 'Lily Gladstone', 'Carey Mulligan'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Barbie lead actor was:',
            'options': ['Ryan Gosling', 'Paul Giamatti', 'Joaquin Phoenix', 'Nicolas Cage'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Poor Things lead actress was:',
            'options': ['Emma Stone', 'Margot Robbie', 'Lily Gladstone', 'Carey Mulligan'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Beef lead actor was:',
            'options': ['Steven Yeun', 'Kieran Culkin', 'Jeremy Allen White', 'Pedro Pascal'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Beef lead actress was:',
            'options': ['Ali Wong', 'Sarah Snook', 'Jennifer Coolidge', 'Ayo Edebiri'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Succession genre is:',
            'options': ['Drama', 'Comedy', 'Thriller', 'Action'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'The Bear genre is:',
            'options': ['Drama', 'Comedy', 'Thriller', 'Action'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Golden Globe Best Drama Film 2024 was:',
            'options': ['Oppenheimer', 'Barbie', 'Poor Things', 'Killers of the Flower Moon'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Golden Globe Best Comedy Film 2024 was:',
            'options': ['Oppenheimer', 'Barbie', 'Poor Things', 'Wonka'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Billie Eilish won Golden Globe 2024 for which category?',
            'options': ['Best Original Song', 'Best Actress', 'Best Supporting Actress', 'Best Screenplay'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Finneas collaborated with Billie Eilish on which song?',
            'options': ['What Was I Made For?', 'Dance the Night', 'I\'m Just Ken', 'Lift Me Up'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Anatomy of a Fall won which Golden Globe category?',
            'options': ['Non-English Film', 'Best Drama', 'Best Screenplay', 'Best Director'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Golden Globe Awards are related to which industries?',
            'options': ['Film & Television', 'Only Film', 'Only Television', 'Music & Film'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Best Supporting Actress TV at Golden Globes 2024 was won by:',
            'options': ['Elizabeth Debicki', 'Jennifer Coolidge', 'Ali Wong', 'Sarah Snook'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Elizabeth Debicki won for which show?',
            'options': ['The Crown', 'Succession', 'Beef', 'The Bear'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Robert Downey Jr. won Golden Globe 2024 for which film?',
            'options': ['Oppenheimer', 'Barbie', 'Poor Things', 'The Holdovers'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Da\'Vine Joy Randolph won Golden Globe 2024 for which film?',
            'options': ['The Holdovers', 'Oppenheimer', 'Barbie', 'Poor Things'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The Golden Globe trophy is made of:',
            'options': ['Gold', 'Marble', 'Bronze', 'Silver'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Golden Globe Awards are presented by which organization?',
            'options': ['Hollywood Foreign Press Association', 'Academy of Motion Picture', 'Screen Actors Guild', 'Directors Guild'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The Golden Globe Awards were first held in which year?',
            'options': ['1943', '1944', '1945', '1946'],
            'correct': 0,
            'difficulty': 'hard'
        }
    ]

    # ===== PART 4: Questions 301-400 =====
    part4_questions = [
        # Q301-Q325: India-Nepal Relations & International Affairs
        {
            'text': 'Which India-Nepal Joint Commission Meeting was held in January 2024?',
            'options': ['5th', '6th', '7th', '8th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': "India's External Affairs Minister who visited Nepal in January 2024 was:",
            'options': ['Rajnath Singh', 'Amit Shah', 'S. Jaishankar', 'Piyush Goyal'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': "Nepal's Foreign Minister during the visit was:",
            'options': ['Sher Bahadur Deuba', 'Pushpa Kamal Dahal', 'N.P. Saud', 'K.P. Sharma Oli'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'India announced reconstruction assistance of how much?',
            'options': ['NPR 500 crore', 'NPR 750 crore', 'NPR 1,000 crore', 'NPR 1,500 crore'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The reconstruction aid was related to which event?',
            'options': ['2020 floods', '2015 earthquake', 'COVID-19 recovery', 'Border infrastructure'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'Which university library was inaugurated during the visit?',
            'options': ['Kathmandu University Library', 'Pokhara University Library', 'Tribhuvan University Central Library', 'Nepal Sanskrit University Library'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The HIT formula was introduced during PM Modi\'s visit in which year?',
            'options': ['2012', '2014', '2016', '2018'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'HIT stands for:',
            'options': ['Highways, I-Ways, Transways', 'Highways, Industry, Technology', 'Housing, Infrastructure, Trade', 'Highways, Innovation, Tourism'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Capital of Nepal is:',
            'options': ['Pokhara', 'Biratnagar', 'Kathmandu', 'Lalitpur'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'Currency of Nepal is:',
            'options': ['Rupee', 'Nepali Rupee', 'Taka', 'Dollar'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Long-term power trade agreement was signed between which countries?',
            'options': ['India and Bhutan', 'India and Bangladesh', 'India and Nepal', 'India and Sri Lanka'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Which treaty was reviewed during discussions?',
            'options': ['Treaty of Sugauli', 'Treaty of Friendship 1950', 'Indus Treaty', 'Panchsheel Treaty'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Nepal shares border with which countries?',
            'options': ['India & China', 'India & Bhutan', 'India only', 'China only'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': "Nepal's Prime Minister in 2024 was:",
            'options': ['Sher Bahadur Deuba', 'Pushpa Kamal Dahal (Prachanda)', 'K.P. Sharma Oli', 'N.P. Saud'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': "India's reconstruction package value in USD was:",
            'options': ['USD 50 million', 'USD 75 million', 'USD 100 million', 'USD 150 million'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The Nepal earthquake occurred in which year?',
            'options': ['2014', '2015', '2016', '2017'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The library inaugurated was located in which city?',
            'options': ['Pokhara', 'Kathmandu', 'Biratnagar', 'Lalitpur'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'HIT includes Information Ways?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'The treaty reviewed was from which year?',
            'options': ['1947', '1950', '1955', '1960'],
            'correct': 1,
            'difficulty': 'hard'
        },
        # Q326-Q350: BAPS Hindu Mandir, UAE
        {
            'text': 'PM Modi inaugurated the BAPS temple on which date?',
            'options': ['22 January 2024', '14 February 2024', '15 August 2024', '26 January 2024'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The BAPS temple is situated in which area?',
            'options': ['Abu Mureikha', 'Yas Island', 'Al Ain', 'Khalifa City'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The temple cost approximately:',
            'options': ['₹500 crore', '₹600 crore', '₹700 crore', '₹900 crore'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The temple was built on how many hectares?',
            'options': ['2 hectares', '3 hectares', '5.4 hectares', '10 hectares'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The temple has how many spires representing UAE Emirates?',
            'options': ['5', '6', '7', '8'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The temple façade is made of which materials?',
            'options': ['Granite and Marble', 'Pink Sandstone and Marble', 'White Marble only', 'Sandstone only'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'BAPS was formally established in which year?',
            'options': ['1890', '1907', '1920', '1947'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Founder of BAPS was:',
            'options': ['Swami Vivekananda', 'Shastriji Maharaj', 'Pramukh Swami Maharaj', 'Mahatma Gandhi'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Construction of the BAPS temple started in which year?',
            'options': ['2018', '2019', '2020', '2021'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Land for the BAPS temple was allocated during Modi\'s UAE visit in:',
            'options': ['2014', '2015', '2016', '2017'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': "PM Modi's 2015 UAE visit was the first by an Indian PM in how many years?",
            'options': ['20 years', '25 years', '30 years', '34 years'],
            'correct': 3,
            'difficulty': 'hard'
        },
        {
            'text': 'The largest Hindu temple outside India built by BAPS is:',
            'options': ['Akshardham, New Jersey', 'Akshardham, London', 'BAPS Temple, Abu Dhabi', 'Swaminarayan Temple, UK'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The capital of UAE is:',
            'options': ['Dubai', 'Sharjah', 'Abu Dhabi', 'Ajman'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The currency of UAE is:',
            'options': ['UAE Dirham', 'Riyal', 'Dinar', 'Dollar'],
            'correct': 0,
            'difficulty': 'easy'
        },
        # Q351-Q375: Lakshadweep Development Projects
        {
            'text': 'PM Modi inaugurated projects worth how much in Lakshadweep?',
            'options': ['₹956 crore', '₹1,056 crore', '₹1,156 crore', '₹1,256 crore'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Kochi-Lakshadweep Optical Fibre Project cost was:',
            'options': ['₹972 crore', '₹1,072 crore', '₹1,172 crore', '₹1,272 crore'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The cable was laid by which telecom company?',
            'options': ['Reliance Jio', 'Airtel', 'BSNL', 'Vodafone'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The project was executed by which company?',
            'options': ['Samsung', 'NEC Japan', 'Nokia', 'Ericsson'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Which islands are connected under the project?',
            'options': ['Kavaratti', 'Agatti', 'Minicoy', 'All of the above'],
            'correct': 3,
            'difficulty': 'medium'
        },
        {
            'text': 'The project enables which services?',
            'options': ['2G only', '3G only', '4G & 5G services', 'Satellite only'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'Capital of Lakshadweep is:',
            'options': ['Agatti', 'Kavaratti', 'Minicoy', 'Androth'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Lakshadweep is a:',
            'options': ['State', 'Union Territory', 'District', 'Autonomous Region'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The Kochi-Lakshadweep project is what type?',
            'options': ['Submarine Optical Fibre Cable', 'Satellite Network', 'Underwater Pipeline', 'Hydroelectric Project'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'The cable is connected from which city?',
            'options': ['Mumbai', 'Chennai', 'Kochi', 'Mangalore'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'A desalination plant was inaugurated in Lakshadweep?',
            'options': ['Yes', 'No', 'Only planned', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Jan Jeevan Mission tap connections were provided?',
            'options': ['Yes', 'No', 'Only planned', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'A Solar Power Plant was included in the Lakshadweep projects?',
            'options': ['Yes', 'No', 'Only planned', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'A Polytechnic College was launched at which island?',
            'options': ['Agatti', 'Kavaratti', 'Minicoy', 'Androth'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Educational institutions were started at which islands?',
            'options': ['Agatti & Kadmat', 'Andrott & Kadmat', 'Minicoy & Agatti', 'Kavaratti & Andrott'],
            'correct': 1,
            'difficulty': 'hard'
        },
        # Q376-Q400: PRITHVI VIGYAN Scheme
        {
            'text': 'PRITHVI VIGYAN scheme was launched by which ministry?',
            'options': ['Ministry of Space', 'Ministry of Earth Sciences', 'Ministry of Defence', 'ISRO'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'What is the budget of PRITHVI VIGYAN scheme?',
            'options': ['₹3,797 crore', '₹4,797 crore', '₹5,797 crore', '₹6,797 crore'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The scheme period is:',
            'options': ['2020–25', '2021–26', '2022–27', '2023–28'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'PRITHVI focuses on which field?',
            'options': ['Earth Sciences', 'Defence', 'Agriculture', 'Tourism'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'Which of these is NOT part of Earth System Science?',
            'options': ['Atmosphere', 'Hydrosphere', 'Biosphere', 'Legislature'],
            'correct': 3,
            'difficulty': 'medium'
        },
        {
            'text': 'IMD works under which ministry?',
            'options': ['Ministry of Space', 'Ministry of Earth Sciences', 'Ministry of Defence', 'Ministry of Agriculture'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'NCMRWF stands for:',
            'options': ['National Centre for Medium Range Weather Forecasting', 'National Climate Monitoring Research', 'National Centre for Meteorology and Rainfall', 'None of these'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'CMLRE stands for:',
            'options': ['Centre for Marine Living Resources and Ecology', 'Centre for Marine Life Research', 'Council for Marine Living Resources', 'None of these'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Cryosphere refers to which region?',
            'options': ['Oceans', 'Ice and Snow regions', 'Atmosphere', 'Forests'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Hydrosphere refers to which system?',
            'options': ['Water systems', 'Land systems', 'Air systems', 'Ice systems'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Biosphere refers to which system?',
            'options': ['Rocks', 'Water', 'Living organisms', 'Atmosphere'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI include weather forecasting?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Does PRITHVI include ocean research?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Does PRITHVI include climate research?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Does PRITHVI include earthquake monitoring?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Does PRITHVI include disaster warnings?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Does PRITHVI include cyclone warnings?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI include flood warnings?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI include tsunami warnings?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI include polar exploration?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'The PRITHVI scheme was announced in which year?',
            'options': ['2022', '2023', '2024', '2021'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Earth Science includes which of the following?',
            'options': ['Atmosphere, Hydrosphere, Biosphere, Geosphere', 'Only Atmosphere and Hydrosphere', 'Only Biosphere and Geosphere', 'None of these'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'The Ministry of Earth Sciences was established in which year?',
            'options': ['2000', '2004', '2006', '2008'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'Atmosphere refers to which part of Earth?',
            'options': ['Air', 'Water', 'Earth', 'Living things'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Geosphere refers to which part of Earth?',
            'options': ['Air', 'Water', 'Earth/rocks', 'Living things'],
            'correct': 2,
            'difficulty': 'hard'
        }
    ]

    # ===== PART 5: Questions 401-500 =====
    part5_questions = [
        # Q401-Q425: Henley Passport Index 2024
        {
            'text': 'Citizens of the top-ranked passports can access how many destinations?',
            'options': ['190', '192', '194', '196'],
            'correct': 2,
            'difficulty': 'hard'
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
            'text': 'Switzerland ranked at which position in Henley Passport Index 2024?',
            'options': ['4th', '5th', '6th', '7th'],
            'correct': 1,
            'difficulty': 'hard'
        },
        # Q426-Q450: Swachh Survekshan Awards 2023
        {
            'text': 'Indore won the Cleanest City title for which consecutive time?',
            'options': ['5th time', '6th time', '7th consecutive time', '8th time'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The Swachh Survekshan Awards ceremony venue was:',
            'options': ['Rashtrapati Bhavan', 'Bharat Mandapam', 'Vigyan Bhavan', 'India Gate'],
            'correct': 1,
            'difficulty': 'hard'
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
            'text': 'MoHUA stands for:',
            'options': ['Ministry of Housing and Urban Affairs', 'Ministry of Health and Urban Affairs', 'Ministry of Home and Urban Affairs', 'Ministry of Housing and Union Affairs'],
            'correct': 0,
            'difficulty': 'easy'
        },
        # Q451-Q475: Global Firepower Military Rankings 2024
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
            'text': 'Which country ranked 8th in Global Firepower 2024?',
            'options': ['UK', 'South Korea', 'Japan', 'Turkey'],
            'correct': 3,
            'difficulty': 'hard'
        },
        {
            'text': 'Which country ranked 10th in Global Firepower 2024?',
            'options': ['Pakistan', 'Italy', 'Brazil', 'France'],
            'correct': 1,
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
        # Q476-Q500: FIFA Football Awards 2024
        {
            'text': 'FIFA Women\'s Player of the Year 2024 was:',
            'options': ['Alexia Putellas', 'Aitana Bonmati', 'Mary Earps', 'Sam Kerr'],
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
            'text': 'The FIFA Awards 2024 ceremony was held in which city?',
            'options': ['London', 'Paris', 'Madrid', 'Berlin'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Aitana Bonmati is from which country?',
            'options': ['Spain', 'England', 'France', 'Germany'],
            'correct': 0,
            'difficulty': 'hard'
        }
    ]

    # Combine all parts
    all_parts = [
        {'name': 'Current Affairs 2024 - Part 1', 'slug': 'current-affairs-2024-part1', 
         'description': 'Golden Globes, FIFA, ICC Awards & more (Questions 1-100)', 'questions': part1_questions},
        {'name': 'Current Affairs 2024 - Part 2', 'slug': 'current-affairs-2024-part2',
         'description': 'Awards, Republic Day, Constitution & Ram Mandir (Questions 101-200)', 'questions': part2_questions},
        {'name': 'Current Affairs 2024 - Part 3', 'slug': 'current-affairs-2024-part3',
         'description': 'National Sports Awards, Emmy Awards & Golden Globes (Questions 201-300)', 'questions': part3_questions},
        {'name': 'Current Affairs 2024 - Part 4', 'slug': 'current-affairs-2024-part4',
         'description': 'India-Nepal, BAPS Temple, Lakshadweep & PRITHVI (Questions 301-400)', 'questions': part4_questions},
        {'name': 'Current Affairs 2024 - Part 5', 'slug': 'current-affairs-2024-part5',
         'description': 'Henley Passport, Swachh Survekshan, Global Firepower & FIFA (Questions 401-500)', 'questions': part5_questions}
    ]

    # Create exams and mock tests
    print("\n📚 Creating 5 Mock Tests with 500 Unique Questions...")
    all_parts.reverse()
    total_questions_created = 0
    
    for part in all_parts:
        print(f"\n📝 Creating {part['name']}...")
        
        # Create exam for this part
        exam, created = Exam.objects.get_or_create(
            slug=part['slug'],
            defaults={
                'name': part['name'],
                'short_name': f'CA P{all_parts.index(part)+1}',
                'category': exam_category,
                'exam_level': 'national',
                'duration_minutes': 60,
                'total_marks': len(part['questions']),
                'total_questions': len(part['questions']),
                'negative_marking': False,
                'description': f'Comprehensive Current Affairs Mock Test Part {all_parts.index(part)+1} - {part["description"]}',
                'is_paid': False,
                'price': 0,
                'is_active': True
            }
        )
        print(f"  ✓ Exam: {exam.name}")
        
        # Create subject for this exam
        subject, _ = Subject.objects.get_or_create(
            exam=exam,
            name=part['name'],
            defaults={'weightage': 100, 'order': 1}
        )
        print(f"  ✓ Subject: {subject.name}")
        
        # Create questions
        created_questions = []
        for idx, q_data in enumerate(part['questions'], 1):
            # Shuffle options
            options = q_data['options']
            correct_index = q_data['correct']
            correct_answer = options[correct_index]
            
            option_list = list(enumerate(options))
            random.shuffle(option_list)
            shuffled_options = [opt for _, opt in option_list]
            new_correct_index = [opt for _, opt in option_list].index(correct_answer)
            
            question = Question.objects.create(
                exam=exam,
                subject=subject,
                question_text=q_data['text'],
                question_type='mcq',
                difficulty=q_data['difficulty'],
                marks=2,
                negative_marks=0.25,
                explanation="N/A",
                is_active=True
            )
            
            for i, opt_text in enumerate(shuffled_options):
                Option.objects.create(
                    question=question,
                    option_text=opt_text,
                    is_correct=(i == new_correct_index),
                    order=i
                )
            
            created_questions.append(question)
        
        print(f"  ✓ Created {len(created_questions)} questions")
        
        # Create Mock Test
        mock_test = MockTest.objects.create(
            name=f'{part["name"]} ({len(created_questions)} Questions)',
            slug=f'{part["slug"]}-mock',
            exam=exam,
            description=part['description'],
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
                marks=2,
                order=idx
            )
        
        total_questions_created += len(created_questions)
        print(f"  ✓ Created mock test: {mock_test.name}")
        print(f"    └─ {mock_test.total_questions} questions")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ ALL 5 CURRENT AFFAIRS MOCK TESTS CREATION COMPLETED!")
    print("=" * 80)
    
    print("\n📊 FINAL SUMMARY:")
    print(f"   • Total Mock Tests Created: {MockTest.objects.filter(exam__category=exam_category).count()}")
    print(f"   • Total Questions: {total_questions_created}")
    print(f"   • Total Exams: {Exam.objects.filter(category=exam_category).count()}")
    print(f"   • Total Subjects: {Subject.objects.filter(exam__category=exam_category).count()}")
    print(f"   • All tests are FREE (is_paid=False, price=0)")
    
    print("\n📋 MOCK TESTS CREATED:")
    for i, part in enumerate(all_parts, 1):
        mock = MockTest.objects.filter(slug=f'{part["slug"]}-mock').first()
        if mock:
            q_count = MockTestQuestion.objects.filter(mock_test=mock).count()
            print(f"   {i}. {part['name']}: {q_count} questions")
    
    print("\n🎯 To take the mock tests:")
    print("   1. Login to the application")
    print("   2. Go to Mock Tests section")
    print("   3. Select any of the 5 Current Affairs mock tests")
    print("   4. Start practicing!")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        create_all_mock_tests()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)