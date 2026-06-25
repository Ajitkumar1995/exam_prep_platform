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

def create_current_affairs_mock_test_part4():
    print("=" * 80)
    print("📰 CREATING CURRENT AFFAIRS MOCK TEST PART 4 (QUESTIONS 301-400)")
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
        slug='current-affairs-2024-part4',
        defaults={
            'name': 'Current Affairs 2024 - Part 4',
            'short_name': 'CA 2024 P4',
            'category': exam_category,
            'exam_level': 'national',
            'duration_minutes': 60,
            'total_marks': 100,
            'total_questions': 100,
            'negative_marking': False,
            'description': 'Comprehensive Current Affairs Mock Test Part 4 covering India-Nepal Relations, BAPS Temple, Lakshadweep & PRITHVI VIGYAN',
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
        name='Current Affairs 2024 - Part 4',
        defaults={'weightage': 100, 'order': 1}
    )
    print(f"✓ Subject: {subject.name}")
    
    # Clear existing questions for this exam
    Question.objects.filter(exam=exam).delete()
    print("✓ Cleared existing questions")
    
    # All 100 Current Affairs Questions (301-400)
    questions_data = [
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
            'text': 'India agreed to import how much hydroelectricity from Nepal in the next decade?',
            'options': ['5,000 MW', '8,000 MW', '10,000 MW', '12,000 MW'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': "Nepal's electricity generation capacity mentioned in the report was:",
            'options': ['2,000 MW', '2,600 MW', '3,200 MW', '4,000 MW'],
            'correct': 1,
            'difficulty': 'hard'
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
            'text': 'EAM stands for:',
            'options': ['External Affairs Minister', 'Economic Affairs Minister', 'Environment Affairs Minister', 'Education Affairs Minister'],
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
            'text': 'The Joint Commission Meeting number held in January 2024 was:',
            'options': ['5th', '6th', '7th', '8th'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The library inaugurated was located in which city?',
            'options': ['Pokhara', 'Kathmandu', 'Biratnagar', 'Lalitpur'],
            'correct': 1,
            'difficulty': 'medium'
        },
        {
            'text': 'The power export target from Nepal to India is:',
            'options': ['5,000 MW', '8,000 MW', '10,000 MW', '12,000 MW'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'HIT includes Information Ways?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': "Nepal's power capacity mentioned was:",
            'options': ['2,000 MW', '2,600 MW', '3,200 MW', '4,000 MW'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The treaty reviewed was from which year?',
            'options': ['1947', '1950', '1955', '1960'],
            'correct': 1,
            'difficulty': 'hard'
        },
        # Q326-Q350: BAPS Hindu Mandir, UAE
        {
            'text': 'The first Hindu temple in UAE is located in which city?',
            'options': ['Dubai', 'Sharjah', 'Abu Dhabi', 'Ajman'],
            'correct': 2,
            'difficulty': 'easy'
        },
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
            'text': 'Which organization built the temple?',
            'options': ['ISKCON', 'Ramakrishna Mission', 'BAPS', 'Chinmaya Mission'],
            'correct': 2,
            'difficulty': 'easy'
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
            'text': 'BAPS stands for:',
            'options': [
                'Bochasanwasi Shri Akshar Purushottam Swaminarayan Sanstha',
                'Bharat Akhil Parishad Sanstha',
                'Bharatiya Purushottam Society',
                'Bochasan Trust'
            ],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'UAE has how many Emirates?',
            'options': ['5', '6', '7', '8'],
            'correct': 2,
            'difficulty': 'easy'
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
            'text': 'The BAPS temple was inaugurated in which city?',
            'options': ['Dubai', 'Sharjah', 'Abu Dhabi', 'Ajman'],
            'correct': 2,
            'difficulty': 'easy'
        },
        {
            'text': 'The BAPS temple was built by which organization?',
            'options': ['BAPS', 'ISKCON', 'Ramakrishna Mission', 'Chinmaya Mission'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'The BAPS temple cost was approximately:',
            'options': ['₹500 crore', '₹600 crore', '₹700 crore', '₹900 crore'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The number of spires on the BAPS temple is:',
            'options': ['5', '6', '7', '8'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The BAPS temple is made of which materials?',
            'options': ['Granite and Marble', 'Pink Sandstone and Marble', 'White Marble only', 'Sandstone only'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'BAPS was founded in which year?',
            'options': ['1890', '1907', '1920', '1947'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The founder of BAPS was:',
            'options': ['Swami Vivekananda', 'Shastriji Maharaj', 'Pramukh Swami Maharaj', 'Mahatma Gandhi'],
            'correct': 1,
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
            'text': 'The cable provides internet speed of:',
            'options': ['10 Gbps', '50 Gbps', '100 Gbps', '200 Gbps'],
            'correct': 2,
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
            'text': 'The cable length is:',
            'options': ['1,268 km', '1,568 km', '1,868 km', '2,168 km'],
            'correct': 2,
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
            'text': 'The telecom company involved in the project is:',
            'options': ['Reliance Jio', 'Airtel', 'BSNL', 'Vodafone'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The technology company that executed the project is:',
            'options': ['Samsung', 'NEC Japan', 'Nokia', 'Ericsson'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The internet speed provided by the cable is:',
            'options': ['10 Gbps', '50 Gbps', '100 Gbps', '200 Gbps'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The cable length is how many kilometers?',
            'options': ['1,268 km', '1,568 km', '1,868 km', '2,168 km'],
            'correct': 2,
            'difficulty': 'hard'
        },
        {
            'text': 'The new services enabled by the project are:',
            'options': ['2G only', '3G only', '4G & 5G', 'Satellite only'],
            'correct': 2,
            'difficulty': 'medium'
        },
        {
            'text': 'The capital of Lakshadweep is which island?',
            'options': ['Agatti', 'Kavaratti', 'Minicoy', 'Androth'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'Lakshadweep is which type of territory?',
            'options': ['State', 'Union Territory', 'District', 'Autonomous Region'],
            'correct': 1,
            'difficulty': 'easy'
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
            'text': 'An Indian Reserve Battalion HQ was included?',
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
            'text': 'PRITHVI VIGYAN is a scheme of which ministry?',
            'options': ['Ministry of Space', 'Ministry of Earth Sciences', 'Ministry of Defence', 'ISRO'],
            'correct': 1,
            'difficulty': 'easy'
        },
        {
            'text': 'The budget allocation for PRITHVI VIGYAN is:',
            'options': ['₹3,797 crore', '₹4,797 crore', '₹5,797 crore', '₹6,797 crore'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'The scheme duration is from:',
            'options': ['2020–25', '2021–26', '2022–27', '2023–28'],
            'correct': 1,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI include weather forecasting?',
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
            'text': 'Does PRITHVI include ocean studies?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Does PRITHVI include cryosphere studies?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI include geosphere studies?',
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
            'text': 'Does PRITHVI include ocean resource utilization?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI cover disaster warnings like cyclones, floods, tsunamis?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
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
            'options': ['National Centre for Medium Range Weather Forecasting', 'National Centre for Meteorological Research', 'National Centre for Monsoon Research', 'National Centre for Weather Research'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'CMLRE stands for:',
            'options': ['Centre for Marine Living Resources and Ecology', 'Centre for Marine Life Research', 'Centre for Marine Living Resources', 'Centre for Marine Ecology'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI include earthquake monitoring?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Does PRITHVI translate scientific knowledge into services?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI support research vessels?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Does PRITHVI focus on multidisciplinary research?',
            'options': ['Yes', 'No', 'Only partially', 'Not mentioned'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'PRITHVI relates to which field of study?',
            'options': ['Earth Sciences', 'Defence', 'Agriculture', 'Tourism'],
            'correct': 0,
            'difficulty': 'easy'
        },
        {
            'text': 'The full form of PRITHVI is:',
            'options': ['PRITHvi VIgyan', 'Planetary Research Initiative', 'Program for Research', 'None of the above'],
            'correct': 0,
            'difficulty': 'hard'
        }
    ]
    
    # Create questions
    print("\n📝 Creating 100 Current Affairs Questions (301-400)...")
    
    created_questions = []
    for idx, q_data in enumerate(questions_data, 301):
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
    
    print(f"\n✓ Created {len(created_questions)} questions (301-400)")
    
    # Create Mock Test
    print("\n🎯 Creating Current Affairs Mock Test Part 4...")
    
    # Delete existing mock test
    MockTest.objects.filter(slug='current-affairs-mock-test-2024-part4').delete()
    
    mock_test = MockTest.objects.create(
        name='Current Affairs Mock Test 2024 - Part 4 (301-400 Questions)',
        slug='current-affairs-mock-test-2024-part4',
        exam=exam,
        description='Comprehensive mock test covering India-Nepal Relations, BAPS Hindu Mandir, Lakshadweep Development & PRITHVI VIGYAN Scheme',
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
    print("✅ CURRENT AFFAIRS MOCK TEST PART 4 CREATION COMPLETED!")
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
    print("   3. Select 'Current Affairs Mock Test 2024 - Part 4 (301-400 Questions)'")
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
        create_current_affairs_mock_test_part4()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)