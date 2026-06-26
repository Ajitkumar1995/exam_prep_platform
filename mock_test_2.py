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

def add_new_mock_tests():
    print("=" * 80)
    print("📰 ADDING NEW CURRENT AFFAIRS MOCK TESTS (PARTS 6-10)")
    print("=" * 80)
    
    # Get or create Exam Category
    exam_category, _ = ExamCategory.objects.get_or_create(
        name='Current Affairs',
        defaults={
            'slug': 'current-affairs',
            'description': 'Current Affairs exams and mock tests'
        }
    )
    print(f"✓ Exam Category: {exam_category.name}")
    
    # Get the main exam (should exist from first script)
    try:
        main_exam = Exam.objects.get(slug='current-affairs-2024')
        print(f"✓ Found Main Exam: {main_exam.name} (ID: {main_exam.id})")
    except Exam.DoesNotExist:
        print("❌ Main exam not found! Please run the first script first.")
        sys.exit(1)
    
    # Get or create subject
    main_subject, _ = Subject.objects.get_or_create(
        exam=main_exam,
        name='Current Affairs 2024',
        defaults={'weightage': 100, 'order': 1}
    )
    print(f"✓ Subject: {main_subject.name}")
    
    # ============================================================
    # NEW QUESTIONS FROM SET 6-10 (Questions 301-500)
    # ============================================================
    
    # PART 6: Questions 301-350 (Chapter 3: Policy Reforms)
    part6_questions = [
        # Q301-Q320: Business Environment Reforms
        {
            'text': 'The primary objective of business environment reforms in India has been to:',
            'options': [
                'Increase import dependence',
                'Promote ease of doing business and investment',
                'Reduce industrial production',
                'Restrict private sector participation'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The chapter highlights that policy reforms have focused on improving the business climate, attracting investments and enhancing India\'s competitiveness.'
        },
        {
            'text': 'Which factor has been identified as a major driver of India\'s improved business ecosystem?',
            'options': [
                'Policy stability',
                'Regulatory simplification',
                'Digital governance',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'The reforms combine policy stability, simplified regulations and digital governance to improve the investment climate.'
        },
        {
            'text': 'Which of the following is a major objective of regulatory reforms?',
            'options': [
                'Increasing compliance burden',
                'Reducing transparency',
                'Improving investor confidence',
                'Reducing exports'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'Transparent regulations improve investor confidence and encourage domestic and foreign investment.'
        },
        {
            'text': 'Business reforms mainly aim to encourage:',
            'options': [
                'Entrepreneurship',
                'Innovation',
                'Employment generation',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'The reforms seek to create a business-friendly ecosystem that promotes entrepreneurship, innovation and employment.'
        },
        {
            'text': 'Which sector benefits the most from simplified regulatory approvals?',
            'options': [
                'Manufacturing',
                'Services',
                'MSMEs',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Simplified approvals reduce costs and delays for businesses across all sectors.'
        },
        {
            'text': 'One of the major outcomes of business reforms has been:',
            'options': [
                'Higher transaction costs',
                'Greater transparency',
                'Reduced digital adoption',
                'Lower industrial productivity'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'Transparent governance has been one of the major achievements highlighted in the chapter.'
        },
        {
            'text': 'Which category of enterprises has received special attention in India\'s reform agenda?',
            'options': [
                'Only large industries',
                'Only multinational corporations',
                'MSMEs and startups',
                'Only public sector undertakings'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'The reforms particularly encourage MSMEs and startups through simplified regulations and digital services.'
        },
        {
            'text': 'Which principle best reflects India\'s business reform strategy?',
            'options': [
                'Maximum regulation',
                'Minimum government, maximum governance',
                'Import substitution alone',
                'Complete privatization'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'The reforms emphasize efficient governance with minimal procedural hurdles.'
        },
        {
            'text': 'Policy reforms are expected to improve India\'s position in:',
            'options': [
                'Investment attractiveness',
                'Business competitiveness',
                'Economic resilience',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Reforms improve India\'s competitiveness, investment appeal and long-term resilience.'
        },
        {
            'text': 'Which type of governance has significantly reduced paperwork for businesses?',
            'options': [
                'Manual governance',
                'Digital governance',
                'Offline approvals',
                'Paper-based administration'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Digital governance has streamlined business processes and reduced paperwork.'
        },
        {
            'text': 'A predictable policy environment mainly helps:',
            'options': [
                'Increase uncertainty',
                'Improve investor confidence',
                'Reduce exports',
                'Increase inflation'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'Investors prefer predictable policies that reduce business risks.'
        },
        {
            'text': 'Which is a direct benefit of simplified compliance procedures?',
            'options': [
                'Higher compliance costs',
                'Reduced compliance burden',
                'Longer approval timelines',
                'Reduced entrepreneurship'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'Simplified compliance lowers costs and improves ease of doing business.'
        },
        {
            'text': 'Which reform contributes most to reducing physical interaction between businesses and government?',
            'options': [
                'Digital platforms',
                'Paper records',
                'Manual verification',
                'Offline licensing'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'Online platforms reduce human interface and improve transparency.'
        },
        {
            'text': 'Business reforms contribute to employment primarily by:',
            'options': [
                'Discouraging investment',
                'Encouraging enterprise growth',
                'Reducing manufacturing',
                'Increasing import dependence'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'Easier business conditions encourage expansion, creating employment opportunities.'
        },
        {
            'text': 'Which feature is essential for a competitive business ecosystem?',
            'options': [
                'Complex procedures',
                'Transparent regulations',
                'Frequent policy uncertainty',
                'High compliance costs'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Transparency is a key element of an efficient business environment.'
        },
        {
            'text': 'Which of the following is most likely to attract Foreign Direct Investment (FDI)?',
            'options': [
                'Stable regulatory environment',
                'Frequent policy changes',
                'Complicated approvals',
                'High compliance burden'
            ],
            'correct': 0,
            'difficulty': 'easy',
            'explanation': 'A stable regulatory framework is a major factor influencing FDI decisions.'
        },
        {
            'text': 'India\'s reform approach focuses on balancing:',
            'options': [
                'Growth and governance',
                'Innovation and regulation',
                'Investment and transparency',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'medium',
            'explanation': 'The chapter emphasizes balanced reforms supporting sustainable economic growth.'
        },
        {
            'text': 'Which among the following is NOT a characteristic of an efficient business environment?',
            'options': [
                'Transparency',
                'Predictability',
                'Excessive procedural delays',
                'Digital service delivery'
            ],
            'correct': 2,
            'difficulty': 'easy',
            'explanation': 'Procedural delays discourage business activity and investment.'
        },
        {
            'text': 'Business reforms ultimately aim to strengthen India\'s:',
            'options': [
                'Economic competitiveness',
                'Manufacturing ecosystem',
                'Investment climate',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'The reforms seek to build a globally competitive and investment-friendly economy.'
        },
        {
            'text': 'Which statement best summarizes India\'s business reform strategy?',
            'options': [
                'Increase regulations for all businesses.',
                'Promote transparent, technology-driven and investment-friendly governance.',
                'Restrict private investment.',
                'Discourage foreign investment.'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'The chapter concludes that India\'s reforms are designed to create a transparent, technology-enabled and globally competitive business environment.'
        },
        # Q321-Q340: Startup India and MSME Reforms
        {
            'text': 'Under the Startup India initiative, startup recognition is granted by which department?',
            'options': [
                'Department for Promotion of Industry and Internal Trade (DPIIT)',
                'Ministry of MSME',
                'NITI Aayog',
                'Department of Revenue'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'Eligible companies receive recognition from DPIIT, enabling them to access tax incentives, simplified compliance, fast-tracked IPR processing and regulatory support.'
        },
        {
            'text': 'As of February 2026, India had approximately how many DPIIT-recognised startups?',
            'options': [
                '1.25 lakh',
                '1.75 lakh',
                'Over 2.16 lakh',
                'Over 3 lakh'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'India had more than 2.16 lakh DPIIT-recognised startups as of February 2026.'
        },
        {
            'text': 'Startup India was launched primarily to:',
            'options': [
                'Increase import substitution',
                'Build a robust startup ecosystem promoting innovation and employment',
                'Privatise public sector enterprises',
                'Increase customs duty'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Startup India aims to foster innovation, sustainable economic growth and large-scale employment.'
        },
        {
            'text': 'Which of the following is NOT a benefit available to DPIIT-recognised startups?',
            'options': [
                'Tax incentives',
                'Simplified compliance procedures',
                'Fast-tracked Intellectual Property Rights (IPR) processing',
                'Automatic government equity investment'
            ],
            'correct': 3,
            'difficulty': 'medium',
            'explanation': 'The initiative provides tax incentives, compliance support and IPR facilitation, but not automatic government equity investment.'
        },
        {
            'text': 'The Credit Guarantee Scheme for Micro and Small Enterprises (CGTMSE) provides credit support up to:',
            'options': [
                '₹5 crore',
                '₹10 crore',
                '₹15 crore',
                '₹20 crore'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'CGTMSE facilitates credit guarantees for loans up to ₹10 crore for Micro and Small Enterprises.'
        },
        {
            'text': 'Under the revised framework, the maximum guarantee coverage under CGTMSE has been enhanced to:',
            'options': [
                '₹10 crore',
                '₹15 crore',
                '₹20 crore',
                '₹25 crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The revised framework increased the guarantee coverage from ₹10 crore to ₹20 crore per eligible borrower.'
        },
        {
            'text': 'The Credit Guarantee Scheme for Exporters (CGSE) provides additional collateral-free credit support of up to:',
            'options': [
                '₹5,000 crore',
                '₹10,000 crore',
                '₹15,000 crore',
                '₹20,000 crore'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'CGSE provides ₹20,000 crore of additional collateral-free credit support to exporter MSMEs.'
        },
        {
            'text': 'The Credit Assessment Model (CAM) introduced by Public Sector Banks is mainly based on:',
            'options': [
                'Manual field inspections',
                'Digital footprints of MSMEs',
                'Credit card transactions only',
                'Income tax raids'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'CAM uses digitally fetched and verifiable data to automate MSME loan appraisal.'
        },
        {
            'text': 'The Credit Assessment Model (CAM) for MSMEs was launched in:',
            'options': [
                '2023',
                '2024',
                '2025',
                '2026'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Public Sector Banks launched CAM during 2025.'
        },
        {
            'text': 'Between 1 April and 30 November 2025, MSME loan applications processed under CAM exceeded:',
            'options': [
                '₹2 lakh crore',
                '₹3.2 lakh crore',
                '₹4.5 lakh crore',
                '₹5 lakh crore'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'MSME loan applications exceeding ₹3.2 lakh crore were processed under CAM.'
        },
        {
            'text': 'During the same period, loans sanctioned under CAM amounted to more than:',
            'options': [
                '₹21.5 thousand crore',
                '₹31.5 thousand crore',
                '₹41.5 thousand crore',
                '₹51.5 thousand crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Loans worth more than ₹41.5 thousand crore were sanctioned.'
        },
        {
            'text': 'The Sabka Bima, Sabki Raksha (Amendment of Insurance Laws) Act was enacted in:',
            'options': [
                '2023',
                '2024',
                '2025',
                '2026'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'The Sabka Bima, Sabki Raksha (Amendment of Insurance Laws) Act, 2025 introduced major insurance sector reforms.'
        },
        {
            'text': 'The insurance sector FDI limit has been increased to:',
            'options': [
                '49%',
                '74%',
                '90%',
                '100%'
            ],
            'correct': 3,
            'difficulty': 'medium',
            'explanation': 'The Act proposes increasing the FDI limit to 100% to attract investment and improve insurance penetration.'
        },
        {
            'text': 'The IRDAI approval threshold for share transfers has been increased from:',
            'options': [
                '1% to 5%',
                '5% to 10%',
                '10% to 15%',
                '15% to 20%'
            ],
            'correct': 0,
            'difficulty': 'hard',
            'explanation': 'The threshold was raised from 1% to 5%, simplifying compliance.'
        },
        {
            'text': 'The Net Owned Fund requirement for foreign reinsurers has been reduced from:',
            'options': [
                '₹3,000 crore to ₹1,000 crore',
                '₹4,000 crore to ₹2,000 crore',
                '₹5,000 crore to ₹1,000 crore',
                '₹6,000 crore to ₹2,000 crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The requirement was reduced from ₹5,000 crore to ₹1,000 crore.'
        },
        {
            'text': 'Which initiative provides a single interconnected digital window for cargo clearance approvals?',
            'options': [
                'PM Gati Shakti',
                'Trade and Investment Facilitation',
                'Startup India',
                'PM Vishwakarma'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'Under Trade and Investment Facilitation, a single digital window has been introduced for cargo clearance approvals.'
        },
        {
            'text': 'Under the new customs system, goods without compliance requirements will be cleared:',
            'options': [
                'After physical inspection',
                'After Cabinet approval',
                'Immediately after online registration and duty payment',
                'After seven working days'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'Such goods are cleared immediately after online registration and payment of applicable duty.'
        },
        {
            'text': 'The Customs Integrated System (CIS) is proposed to be rolled out within:',
            'options': [
                'One year',
                'Two years',
                'Three years',
                'Five years'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'CIS will be implemented as a single integrated customs platform within two years.'
        },
        {
            'text': 'Under the phased customs modernisation plan, the Government aims to scan:',
            'options': [
                'Every export consignment only',
                'Every imported container at airports only',
                'Every container across all major ports',
                'Only hazardous cargo'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The objective is to scan every container across all major ports using advanced imaging and AI-based risk assessment.'
        },
        {
            'text': 'The expanded use of non-intrusive scanning in customs will primarily rely on:',
            'options': [
                'Blockchain technology',
                'Artificial Intelligence and advanced imaging',
                'Quantum computing',
                'Satellite communication'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'The document states that customs risk assessment will increasingly use advanced imaging and Artificial Intelligence for non-intrusive scanning.'
        },
        # Q341-Q350: Regulatory Reforms
        {
            'text': 'Under the Portfolio Investment Scheme (PIS), the investment limit for an individual Person Resident Outside India (PROI) has been proposed to increase from:',
            'options': [
                '2% to 5%',
                '5% to 10%',
                '10% to 15%',
                '15% to 20%'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'The investment limit for an individual PROI under the PIS has been proposed to increase from 5% to 10%.'
        },
        {
            'text': 'The overall investment limit for Individual Persons Resident Outside India (PROIs) under the PIS has been proposed to increase to:',
            'options': [
                '15%',
                '20%',
                '24%',
                '26%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The overall investment limit for PROIs has been proposed to increase from 10% to 24%.'
        },
        {
            'text': 'Regulatory reforms aimed at enhancing Ease of Doing Business have focused on:',
            'options': [
                'Capacity-building',
                'Regulatory coherence',
                'Trust-based governance',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'The reforms emphasize capacity-building, regulatory coherence and trust-based governance to improve Ease of Doing Business.'
        },
        {
            'text': 'RBI has consolidated more than __ circulars and guidelines into Master Directions.',
            'options': [
                '5,000',
                '7,000',
                '9,000',
                '12,000'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'RBI consolidated over 9,000 circulars and guidelines into function-specific Master Directions.'
        },
        {
            'text': 'RBI consolidated its regulatory framework into how many function-specific Master Directions?',
            'options': [
                '138',
                '188',
                '238',
                '338'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'RBI issued 238 function-specific Master Directions for regulated entities.'
        },
        {
            'text': 'RBI simplified instructions for Regional Rural Banks and Cooperative Banks in coordination with:',
            'options': [
                'SIDBI',
                'NABARD',
                'EXIM Bank',
                'SEBI'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'RBI coordinated with NABARD to simplify instructions for Regional Rural Banks and Cooperative Banks.'
        },
        {
            'text': 'A total of how many RBI circulars are being repealed under the simplification exercise?',
            'options': [
                '7,446',
                '8,446',
                '9,446',
                '10,446'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': '9,446 circulars are being repealed to improve accessibility and reduce compliance burden.'
        },
        {
            'text': 'How many RBI circulars have been consolidated into Master Circulars?',
            'options': [
                '2,809',
                '3,809',
                '4,809',
                '5,809'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': '3,809 circulars have been consolidated into Master Circulars.'
        },
        {
            'text': 'RBI identified __ circulars as obsolete during its regulatory simplification exercise.',
            'options': [
                '4,673',
                '5,173',
                '5,673',
                '6,173'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'RBI identified 5,673 circulars as obsolete.'
        },
        {
            'text': 'SEBI aligned the guidelines for issuance and listing of securitised debt instruments with the norms of:',
            'options': [
                'IRDAI',
                'NABARD',
                'Reserve Bank of India',
                'Ministry of Finance'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'SEBI aligned the SDI framework with the Reserve Bank of India\'s securitisation norms.'
        }
    ]

    # PART 7: Questions 351-400 (Chapter 3 continued + Digital Blueprint)
    part7_questions = [
        # Q351-Q370: Tax Reforms
        {
            'text': 'The primary objective of SEBI\'s recent regulatory reforms is to:',
            'options': [
                'Increase litigation',
                'Simplify regulations and improve transparency',
                'Increase compliance burden',
                'Restrict market participation'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'SEBI\'s reforms focus on regulatory simplification, transparency and deeper capital markets.'
        },
        {
            'text': 'Integrated assessment and penalty orders provide relief by reducing the mandatory pre-deposit from:',
            'options': [
                '30% to 20%',
                '25% to 15%',
                '20% to 10%',
                '15% to 5%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The mandatory pre-deposit has been reduced from 20% to 10% on the core tax demand.'
        },
        {
            'text': 'Updated income tax returns are permitted even after reassessment with an additional tax of:',
            'options': [
                '5%',
                '8%',
                '10%',
                '15%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Updated returns are permitted after reassessment with an additional tax of 10%.'
        },
        {
            'text': 'Immunity from penalty and prosecution has been extended from underreporting to:',
            'options': [
                'Tax avoidance',
                'Misreporting',
                'GST evasion',
                'Transfer pricing'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'Immunity has been extended from underreporting to misreporting, subject to payment of full tax and interest.'
        },
        {
            'text': 'Which offence has been decriminalised under the rationalisation measures?',
            'options': [
                'Smuggling',
                'Production of counterfeit currency',
                'Non-production of books and TDS on payments in kind',
                'Money laundering'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Non-production of books and TDS defaults on payments in kind have been decriminalised, with minor offences attracting only monetary fines.'
        },
        {
            'text': 'Technical penalties under the new framework have largely been converted into:',
            'options': [
                'Criminal prosecution',
                'Community service',
                'Fees',
                'Licence suspension'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Technical penalties have been rationalised into fees, reducing compliance stress.'
        },
        {
            'text': 'Under the revised prosecution framework, the maximum simple imprisonment is:',
            'options': [
                'Six months',
                'One year',
                'Two years',
                'Five years'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The maximum punishment is simple imprisonment up to two years, which may also be converted into a fine.'
        },
        {
            'text': 'Retrospective immunity for non-disclosure of foreign assets below ₹20 lakh is effective from:',
            'options': [
                '1 April 2024',
                '1 July 2024',
                '1 October 2024',
                '1 January 2025'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Retrospective immunity applies from 1 October 2024.'
        },
        {
            'text': 'The Government\'s customs reform strategy is primarily based on:',
            'options': [
                'Physical verification of every consignment',
                'Trust-based customs systems',
                'Manual documentation',
                'State-wise customs licensing'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'The chapter emphasizes trust-based customs systems to improve Ease of Doing Business.'
        },
        {
            'text': 'The combined objective of the regulatory reforms discussed in this section is to:',
            'options': [
                'Increase procedural complexity',
                'Reduce transparency',
                'Reduce regulatory friction while preserving accountability',
                'Restrict foreign investment'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'The reforms aim to reduce regulatory friction, preserve accountability, improve regulatory certainty and encourage competition, thereby strengthening India\'s business environment.'
        },
        {
            'text': 'The Jan Vishwas (Amendment of Provisions) Act, 2023 decriminalised how many provisions?',
            'options': [
                '120',
                '150',
                '183',
                '288'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Jan Vishwas (Amendment of Provisions) Act, 2023 decriminalised 183 provisions across 42 Acts, reducing criminal liability for minor and technical offences.'
        },
        {
            'text': 'The Jan Vishwas (Amendment of Provisions) Act, 2023 amended provisions across how many Acts?',
            'options': [
                '28',
                '35',
                '42',
                '50'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Act decriminalised 183 provisions spread across 42 Acts.'
        },
        {
            'text': 'The Jan Vishwas (Amendment of Provisions) Bill, 2025 comprises how many provisions?',
            'options': [
                '255',
                '300',
                '355',
                '400'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Bill consists of 355 provisions aimed at improving Ease of Doing Business and Ease of Living.'
        },
        {
            'text': 'Out of the 355 provisions in the Jan Vishwas Bill, 2025, how many are proposed for decriminalisation?',
            'options': [
                '183',
                '250',
                '288',
                '355'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Bill proposes amendments to 288 provisions for decriminalisation.'
        },
        {
            'text': 'The remaining provisions in the Jan Vishwas Bill, 2025 primarily aim to improve:',
            'options': [
                'Export promotion',
                'Ease of Living',
                'Digital payments',
                'Capital markets'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'The remaining 67 provisions focus on enhancing Ease of Living.'
        },
        {
            'text': 'The Jan Vishwas reforms reflect the Government\'s commitment to which governance philosophy?',
            'options': [
                'Cooperative Federalism',
                'Sabka Saath, Sabka Vikas',
                'Minimum Government, Maximum Governance',
                'Vocal for Local'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'The reforms reflect the philosophy of "Minimum Government, Maximum Governance."'
        },
        {
            'text': 'The Insolvency and Bankruptcy Code (IBC) was enacted in:',
            'options': [
                '2014',
                '2015',
                '2016',
                '2017'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'The Insolvency and Bankruptcy Code (IBC), 2016 established a time-bound insolvency resolution framework.'
        },
        {
            'text': 'The primary objective of the Insolvency and Bankruptcy Code (IBC) is:',
            'options': [
                'Increasing corporate taxation',
                'Rescuing corporate debtors in distress',
                'Promoting exports',
                'Nationalising private companies'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The IBC primarily aims at rescuing financially distressed corporate debtors through timely resolution.'
        },
        {
            'text': 'Till September 2025, how many corporate debtors had been rescued under the IBC?',
            'options': [
                '2,865',
                '3,265',
                '3,865',
                '4,865'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Since its inception, 3,865 corporate debtors had been rescued up to September 2025.'
        },
        {
            'text': 'Out of the rescued corporate debtors, how many were resolved through approved resolution plans?',
            'options': [
                '1,100',
                '1,300',
                '1,500',
                '1,700'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': '1,300 corporate debtors were rescued through approved resolution plans.'
        },
        # Q371-Q390: Digital Blueprint
        {
            'text': 'The primary objective of India\'s Digital Blueprint for Ease of Doing Business is to:',
            'options': [
                'Increase paperwork in governance',
                'Build a transparent, technology-driven and efficient business ecosystem',
                'Replace all State Governments',
                'Restrict digital services'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The chapter explains that digital governance aims to make business processes transparent, efficient and technology-driven, thereby improving Ease of Doing Business.'
        },
        {
            'text': 'Digital governance primarily improves Ease of Doing Business by:',
            'options': [
                'Increasing manual verification',
                'Reducing physical interface between citizens and government',
                'Increasing paperwork',
                'Eliminating online services'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Digital platforms reduce physical interaction, making approvals faster and more transparent.'
        },
        {
            'text': 'Which of the following is a key feature of digital governance?',
            'options': [
                'Paper-based approvals',
                'Technology-enabled public services',
                'Offline-only applications',
                'Manual record keeping'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Digital governance relies on technology-enabled service delivery to improve efficiency and transparency.'
        },
        {
            'text': 'Digital transformation contributes to business growth mainly by:',
            'options': [
                'Increasing procedural delays',
                'Simplifying regulatory compliance',
                'Restricting innovation',
                'Reducing internet access'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'Simplified compliance reduces costs and improves the ease of establishing and operating businesses.'
        },
        {
            'text': 'Digital public services are designed to promote:',
            'options': [
                'Transparency',
                'Accountability',
                'Efficiency',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Digital governance strengthens transparency, accountability and efficiency simultaneously.'
        },
        {
            'text': 'Which of the following is a major advantage of digital platforms for businesses?',
            'options': [
                'Reduced processing time',
                'Faster approvals',
                'Better service delivery',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Digital platforms reduce processing time, accelerate approvals and improve service delivery.'
        },
        {
            'text': 'Technology-driven governance mainly improves:',
            'options': [
                'Administrative efficiency',
                'Public trust',
                'Investor confidence',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Transparent digital systems improve governance quality and strengthen investor confidence.'
        },
        {
            'text': 'Which principle is central to India\'s digital governance reforms?',
            'options': [
                'Paper-first governance',
                'Digital-first governance',
                'Manual approvals',
                'Physical documentation'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The reforms promote digital-first service delivery for faster and more efficient governance.'
        },
        {
            'text': 'Digital governance helps businesses primarily by:',
            'options': [
                'Increasing compliance burden',
                'Simplifying interactions with government agencies',
                'Eliminating private enterprises',
                'Increasing licensing fees'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Online systems simplify communication and reduce procedural complexity.'
        },
        {
            'text': 'The Digital Blueprint aims to strengthen India\'s position as:',
            'options': [
                'A technology-enabled investment destination',
                'A closed economy',
                'A cash-only economy',
                'An import-dependent economy'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'Digital reforms enhance India\'s attractiveness for domestic and international investors.'
        },
        {
            'text': 'Which of the following is NOT a characteristic of digital governance?',
            'options': [
                'Transparency',
                'Speed',
                'Accountability',
                'Manual file movement'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Digital governance reduces manual file movement through electronic processing.'
        },
        {
            'text': 'A major outcome of digital reforms is:',
            'options': [
                'Reduced efficiency',
                'Increased transparency',
                'Increased procedural complexity',
                'Reduced accessibility'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Digital reforms improve transparency by enabling online tracking and processing.'
        },
        {
            'text': 'Which type of ecosystem does the Digital Blueprint seek to create?',
            'options': [
                'Closed administrative ecosystem',
                'Technology-enabled business ecosystem',
                'Manual governance ecosystem',
                'Licence-based ecosystem'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The chapter emphasizes a technology-enabled ecosystem supporting innovation and business growth.'
        },
        {
            'text': 'One important benefit of digital integration is:',
            'options': [
                'Better coordination among government departments',
                'Higher compliance burden',
                'Slower approvals',
                'Increased paperwork'
            ],
            'correct': 0,
            'difficulty': 'easy',
            'explanation': 'Digital integration enables seamless coordination across departments.'
        },
        {
            'text': 'Digital governance contributes directly to:',
            'options': [
                'Ease of Doing Business',
                'Ease of Living',
                'Better public service delivery',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'The reforms improve business services as well as citizen-centric governance.'
        },
        {
            'text': 'Digital systems improve governance primarily through:',
            'options': [
                'Automation',
                'Online service delivery',
                'Real-time monitoring',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Automation, digital services and real-time monitoring collectively strengthen governance.'
        },
        {
            'text': 'Which of the following best describes India\'s digital reform strategy?',
            'options': [
                'Technology-enabled governance with simplified compliance',
                'Paper-based administration',
                'Offline licensing system',
                'Manual inspections only'
            ],
            'correct': 0,
            'difficulty': 'easy',
            'explanation': 'The strategy focuses on technology-driven governance and simplified compliance.'
        },
        {
            'text': 'Digital reforms primarily encourage:',
            'options': [
                'Innovation',
                'Entrepreneurship',
                'Investment',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'The digital ecosystem supports innovation, entrepreneurship and investment simultaneously.'
        },
        {
            'text': 'Which statement best reflects the Digital Blueprint?',
            'options': [
                'Digital governance increases regulatory burden.',
                'Digital governance strengthens transparency and efficiency.',
                'Digital governance discourages businesses.',
                'Digital governance replaces economic reforms.'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The Digital Blueprint aims to improve transparency, efficiency and ease of doing business through technology.'
        },
        {
            'text': 'The long-term vision behind India\'s digital governance reforms is to:',
            'options': [
                'Build a competitive, transparent and digitally empowered economy',
                'Reduce internet penetration',
                'Increase manual compliance',
                'Restrict digital innovation'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'The chapter concludes that digital governance is a key pillar of India\'s future-ready, globally competitive economy.'
        },
        # Q391-Q400: Digital Platforms
        {
            'text': 'MCA21 Version 3 has been providing end-to-end registry and incorporation-related services since:',
            'options': [
                '2004',
                '2006',
                '2010',
                '2014'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'The MCA21 platform has been used for end-to-end registry and incorporation-related services since 2006.'
        },
        {
            'text': 'Which of the following is NOT a feature of MCA21 Version 3?',
            'options': [
                'e-Scrutiny',
                'e-Adjudication',
                'Compliance Management System',
                'Manual file verification'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'MCA21 Version 3 includes e-Scrutiny, e-Adjudication, Compliance Management System, APIs, dashboards and chatbot support. Manual verification is not a feature.'
        },
        {
            'text': 'Approximately how many filings were made on MCA21 during 2021–2025?',
            'options': [
                '2.84 crore',
                '3.84 crore',
                '4.84 crore',
                '5.84 crore'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'Around 3.84 crore filings were made on MCA21 during 2021–2025.'
        },
        {
            'text': 'MCA21 ensures information security by complying with:',
            'options': [
                'ISO 9001',
                'ISO 14001',
                'ISO 27001',
                'ISO 45001'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'MCA21 follows ISO 27001 standards along with multi-factor authentication for information security.'
        },
        {
            'text': 'During FY 2025–26 (up to 31 January 2026), approximately how many helpdesk tickets were raised on MCA21?',
            'options': [
                '2,16,877',
                '3,16,877',
                '4,16,877',
                '5,16,877'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': '3,16,877 helpdesk tickets were raised during FY 2025–26 (up to 31 January 2026).'
        },
        {
            'text': 'Approximately what percentage of MCA21 helpdesk tickets were successfully resolved?',
            'options': [
                '90%',
                '94%',
                '98%',
                '100%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Around 98% of helpdesk tickets were successfully resolved.'
        },
        {
            'text': 'The Udyam Registration Portal is primarily meant for:',
            'options': [
                'Farmers',
                'MSMEs',
                'Banks',
                'Universities'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Udyam provides a free, paperless, self-declaration-based registration system for MSMEs.'
        },
        {
            'text': 'The Udyam Registration Portal integrates directly with:',
            'options': [
                'UIDAI and RBI',
                'CBDT and GSTN',
                'SEBI and IRDAI',
                'NPCI and NABARD'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'Udyam integrates with CBDT and GSTN, providing a documentation-free digital registration process.'
        },
        {
            'text': 'As of 12 February 2026, the Udyam Portal had facilitated over:',
            'options': [
                '5.71 crore registrations',
                '6.71 crore registrations',
                '7.71 crore registrations',
                '8.71 crore registrations'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Udyam Portal had facilitated over 7.71 crore registrations.'
        },
        {
            'text': 'According to the PIB document, Udyam registrations have supported approximately:',
            'options': [
                '23.97 crore jobs',
                '28.97 crore jobs',
                '33.97 crore jobs',
                '38.97 crore jobs'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The portal has supported approximately 33.97 crore jobs.'
        }
    ]

    # PART 8: Questions 401-450
    part8_questions = [
        # Q401-Q420: BRAP & Digital Infrastructure
        {
            'text': 'The Business Reforms Action Plan (BRAP) has been implemented since:',
            'options': [
                '2013',
                '2014',
                '2015',
                '2016'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'BRAP has been implemented since 2015 to improve Ease of Doing Business across States and Union Territories.'
        },
        {
            'text': 'Till 2026, how many editions of BRAP had been completed?',
            'options': [
                'Five',
                'Six',
                'Seven',
                'Eight'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Seven editions had been completed before the rollout of BRAP 2026.'
        },
        {
            'text': 'BRAP 2026 was formally rolled out on:',
            'options': [
                '15 August 2025',
                '2 October 2025',
                '11 November 2025',
                '26 January 2026'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'BRAP 2026 was formally launched on 11 November 2025.'
        },
        {
            'text': 'The District Business Reform Action Plan (D-BRAP) has been launched by:',
            'options': [
                'Ministry of Finance',
                'DPIIT',
                'RBI',
                'NITI Aayog'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'DPIIT launched D-BRAP to strengthen Ease of Doing Business at the district level.'
        },
        {
            'text': 'Under BRAP 2024, Kerala was categorised as:',
            'options': [
                'Achiever',
                'Top Performer',
                'Fast Mover',
                'Aspirer'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Kerala improved from Aspirer (BRAP 2022) to Fast Mover in BRAP 2024.'
        },
        {
            'text': 'Under BRAP reforms, Uttar Pradesh achieved:',
            'options': [
                '234 reforms across 15 areas',
                '334 reforms across 20 areas',
                '434 reforms across 25 areas',
                '534 reforms across 30 areas'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Uttar Pradesh implemented 434 reforms across 25 reform areas.'
        },
        {
            'text': 'According to the PIB document, Uttar Pradesh achieved business registration in as little as:',
            'options': [
                '10 minutes',
                '15 minutes',
                '30 minutes',
                '60 minutes'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'Uttar Pradesh\'s BRAP reforms enabled 15-minute business registrations.'
        },
        {
            'text': 'Uttar Pradesh reduced labour compliance requirements by approximately:',
            'options': [
                '20%',
                '30%',
                '40%',
                '50%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Labour compliance was reduced by 40% under the state\'s reforms.'
        },
        {
            'text': 'Uttar Pradesh accelerated land administration by making transactions approximately:',
            'options': [
                '25% faster',
                '40% faster',
                '50% faster',
                '60% faster'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Land administration reforms resulted in 50% faster transactions.'
        },
        {
            'text': 'The principal objective of BRAP is to:',
            'options': [
                'Increase regulatory burden',
                'Compare State regulatory systems and reduce compliance burdens',
                'Increase documentation requirements',
                'Centralise all State laws'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'BRAP compares regulatory requirements across States and encourages them to simplify procedures, reduce compliance burdens and create a more business-friendly environment.'
        },
        {
            'text': 'The National Single Window System (NSWS) is primarily designed to:',
            'options': [
                'Collect direct taxes',
                'Guide businesses in identifying and applying for approvals',
                'Issue passports',
                'Regulate stock exchanges'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'NSWS is a digital platform that helps businesses identify and apply for the required approvals through a single digital gateway.'
        },
        {
            'text': 'The National Single Window System integrates approval processes across:',
            'options': [
                '28 Central Departments and 28 States',
                '30 Central Departments and 30 States',
                '32 Central Departments and 32 State Governments',
                '36 Central Departments and 36 States'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'NSWS integrates approvals across 32 Central Departments and 32 State Governments.'
        },
        {
            'text': 'NSWS provides access to approximately how many Central approvals?',
            'options': [
                '498',
                '598',
                '698',
                '798'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'NSWS provides access to 698 Central approvals.'
        },
        {
            'text': 'The National Single Window System provides access to approximately how many State approvals?',
            'options': [
                '5,435',
                '6,435',
                '7,435',
                '8,435'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'NSWS integrates 7,435 State approvals.'
        },
        {
            'text': 'Since its launch, NSWS has granted over:',
            'options': [
                '5 lakh approvals',
                '6.5 lakh approvals',
                '7.25 lakh approvals',
                '8,29,750 approvals'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'Since its launch, NSWS has granted over 8,29,750 approvals.'
        },
        {
            'text': 'PARIVESH 3.0 primarily deals with:',
            'options': [
                'Company incorporation',
                'Environmental clearances and post-approval compliance',
                'GST registration',
                'Customs duty payments'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'PARIVESH 3.0 facilitates environmental clearances and post-approval compliance monitoring.'
        },
        {
            'text': 'PARIVESH stands for:',
            'options': [
                'Public Approval for Industrial Ventures and Environmental Safety Hub',
                'Pro-Active and Responsive Facilitation by Interactive, Virtuous and Environmental Single Window Hub',
                'Public Resource Integration for Environmental Sustainability Hub',
                'Proactive Regulatory Interface for Environmental Services Hub'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'PARIVESH stands for Pro-Active and Responsive Facilitation by Interactive, Virtuous and Environmental Single Window Hub.'
        },
        {
            'text': 'Which of the following features is available in PARIVESH 3.0?',
            'options': [
                'AI-enabled support',
                'Afforestation land banks',
                'Inter-ministerial dashboards',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'PARIVESH 3.0 integrates AI-enabled support, afforestation land banks and inter-ministerial dashboards.'
        },
        {
            'text': 'The e-Gram SWARAJ Portal mainly supports:',
            'options': [
                'Railway ticket booking',
                'Gram Panchayat planning and monitoring',
                'Income tax filing',
                'Stock trading'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'e-Gram SWARAJ provides a unified platform for Gram Panchayat profiles, finances, assets and GPDP activities.'
        },
        {
            'text': 'GPDP stands for:',
            'options': [
                'Gram Panchayat Development Plan',
                'General Public Development Programme',
                'Government Planning Data Portal',
                'Gram Public Distribution Programme'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'GPDP refers to the Gram Panchayat Development Plan.'
        },
        # Q421-Q440: Infrastructure and Logistics
        {
            'text': 'PM Gati Shakti National Master Plan (NMP) was launched in:',
            'options': [
                '2019',
                '2020',
                '2021',
                '2022'
            ],
            'correct': 2,
            'difficulty': 'easy',
            'explanation': 'PM Gati Shakti National Master Plan was launched in October 2021 to enable integrated infrastructure planning across sectors.'
        },
        {
            'text': 'PM Gati Shakti aims to integrate infrastructure planning through a:',
            'options': [
                'Paper-based approval system',
                'GIS-based digital platform',
                'Manual departmental process',
                'Offline project monitoring system'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The National Master Plan is built on a GIS-based digital platform integrating infrastructure data across ministries.'
        },
        {
            'text': 'PM Gati Shakti promotes coordination among:',
            'options': [
                'Only Central Ministries',
                'Only State Governments',
                'Central Ministries, States and Infrastructure Agencies',
                'Private Companies only'
            ],
            'correct': 2,
            'difficulty': 'easy',
            'explanation': 'The platform facilitates coordinated planning among Central Ministries, States and infrastructure agencies.'
        },
        {
            'text': 'The primary objective of PM Gati Shakti is to:',
            'options': [
                'Increase project delays',
                'Improve multimodal connectivity and reduce logistics costs',
                'Increase import dependency',
                'Reduce exports'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'PM Gati Shakti focuses on integrated infrastructure, seamless connectivity and logistics efficiency.'
        },
        {
            'text': 'Which of the following sectors is integrated under PM Gati Shakti?',
            'options': [
                'Roads',
                'Railways',
                'Ports and Airports',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'PM Gati Shakti integrates roads, railways, ports, airports, logistics parks and other infrastructure sectors.'
        },
        {
            'text': 'One of the major expected outcomes of PM Gati Shakti is:',
            'options': [
                'Higher logistics costs',
                'Faster infrastructure implementation',
                'Reduced industrial growth',
                'Increased regulatory burden'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Integrated planning minimizes delays and accelerates infrastructure development.'
        },
        {
            'text': 'PM Gati Shakti particularly supports the development of:',
            'options': [
                'Multimodal logistics infrastructure',
                'Traditional paperwork',
                'Manual planning systems',
                'Cash-based transactions'
            ],
            'correct': 0,
            'difficulty': 'easy',
            'explanation': 'A key objective is the development of multimodal logistics infrastructure.'
        },
        {
            'text': 'Which initiative complements PM Gati Shakti by reducing logistics costs?',
            'options': [
                'National Logistics Policy',
                'Startup India',
                'PM Kisan',
                'Digital India'
            ],
            'correct': 0,
            'difficulty': 'easy',
            'explanation': 'The National Logistics Policy complements PM Gati Shakti to improve logistics efficiency.'
        },
        {
            'text': 'The National Logistics Policy primarily aims to:',
            'options': [
                'Increase freight costs',
                'Improve logistics efficiency and competitiveness',
                'Restrict exports',
                'Increase customs duties'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'NLP seeks to reduce logistics costs and improve India\'s competitiveness.'
        },
        {
            'text': 'Efficient logistics primarily contributes to:',
            'options': [
                'Export competitiveness',
                'Industrial growth',
                'Investment attraction',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Efficient logistics strengthens exports, manufacturing and investment.'
        },
        {
            'text': 'Which technology forms the foundation of PM Gati Shakti planning?',
            'options': [
                'Blockchain',
                'GIS Mapping',
                'Quantum Computing',
                'Cryptocurrency'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'PM Gati Shakti uses GIS mapping for integrated planning.'
        },
        {
            'text': 'Integrated infrastructure planning helps in reducing:',
            'options': [
                'Project duplication',
                'Time overruns',
                'Cost overruns',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Integrated planning minimizes duplication while reducing time and cost overruns.'
        },
        {
            'text': 'PM Gati Shakti improves coordination through:',
            'options': [
                'Shared digital data layers',
                'Paper maps',
                'Manual surveys only',
                'Offline approvals'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'Shared GIS data layers enable coordinated infrastructure planning.'
        },
        {
            'text': 'Which ministry coordinates the PM Gati Shakti National Master Plan?',
            'options': [
                'Ministry of Finance',
                'DPIIT',
                'Ministry of Home Affairs',
                'Ministry of Agriculture'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'The Department for Promotion of Industry and Internal Trade (DPIIT) coordinates PM Gati Shakti.'
        },
        {
            'text': 'PM Gati Shakti mainly promotes:',
            'options': [
                'Silo-based planning',
                'Integrated infrastructure development',
                'Isolated departmental functioning',
                'Manual coordination'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'It replaces silo-based planning with integrated infrastructure development.'
        },
        {
            'text': 'Reduced logistics costs improve India\'s:',
            'options': [
                'Ease of Doing Business',
                'Global competitiveness',
                'Export performance',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Lower logistics costs strengthen business competitiveness and exports.'
        },
        {
            'text': 'Which of the following is a major focus area under PM Gati Shakti?',
            'options': [
                'Last-mile connectivity',
                'Multimodal transport',
                'Integrated planning',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'PM Gati Shakti emphasizes multimodal connectivity, last-mile connectivity and integrated planning.'
        },
        {
            'text': 'PM Gati Shakti supports India\'s vision of becoming:',
            'options': [
                'A logistics-efficient global economy',
                'A closed economy',
                'An import-only economy',
                'A paper-based governance system'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'Efficient infrastructure and logistics are essential for India\'s global economic competitiveness.'
        },
        {
            'text': 'Better logistics infrastructure directly benefits:',
            'options': [
                'MSMEs',
                'Exporters',
                'Manufacturers',
                'All of the above'
            ],
            'correct': 3,
            'difficulty': 'easy',
            'explanation': 'Improved logistics reduces costs and improves market access for MSMEs, exporters and manufacturers.'
        },
        {
            'text': 'The combined objective of PM Gati Shakti and the National Logistics Policy is to:',
            'options': [
                'Increase transport costs',
                'Build an integrated, efficient and globally competitive logistics ecosystem',
                'Restrict freight movement',
                'Increase compliance burden'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'Together, these initiatives aim to create an integrated logistics ecosystem that supports economic growth, exports and Ease of Doing Business.'
        }
    ]

    # PART 9: Questions 451-500
    part9_questions = [
        # Q451-Q480: Various topics
        {
            'text': 'India ranks as the world\'s second-largest manufacturer of which product?',
            'options': [
                'Cars',
                'Mobile phones',
                'Semiconductors',
                'Televisions'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'India has emerged as the world\'s second-largest mobile phone manufacturer.'
        },
        {
            'text': 'The India Semiconductor Mission 2.0 primarily focuses on:',
            'options': [
                'Coal mining',
                'Chip design and semiconductor ecosystem',
                'Tourism',
                'Agriculture'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'India Semiconductor Mission 2.0 focuses on building a robust semiconductor ecosystem.'
        },
        {
            'text': 'Which state houses one of India\'s first end-to-end OSAT semiconductor facilities?',
            'options': [
                'Karnataka',
                'Gujarat',
                'Tamil Nadu',
                'Odisha'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'The OSAT facility is located in Sanand, Gujarat.'
        },
        {
            'text': 'The Government approved how many semiconductor projects across six states?',
            'options': [
                '5',
                '8',
                '10',
                '15'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'The Government approved 10 semiconductor projects across six states.'
        },
        {
            'text': 'India\'s automotive industry provides employment to approximately:',
            'options': [
                '10 million people',
                '20 million people',
                '30 million people',
                '40 million people'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'India\'s automotive industry supports approximately 30 million jobs.'
        },
        {
            'text': 'India is the world\'s largest market for:',
            'options': [
                'Passenger cars only',
                'Two-wheelers and three-wheelers',
                'Trucks only',
                'Electric buses only'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'India leads the world in two-wheelers and three-wheelers market.'
        },
        {
            'text': 'India is known as the "Pharmacy of the World" because of its:',
            'options': [
                'Oil exports',
                'Generic medicine production',
                'Steel production',
                'Automobile exports'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'India is known worldwide as the Pharmacy of the World for its generic medicine production.'
        },
        {
            'text': 'India ranks ____ globally in pharmaceutical production by volume.',
            'options': [
                '1st',
                '2nd',
                '3rd',
                '5th'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'India is the third-largest pharmaceutical producer by volume.'
        },
        {
            'text': 'At least what percentage of India\'s defence equipment is now manufactured domestically?',
            'options': [
                '40%',
                '50%',
                '65%',
                '80%'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'Around 65% of defence equipment is now manufactured in India.'
        },
        {
            'text': 'Indigenous defence production reached approximately ____ in FY 2024–25.',
            'options': [
                '₹80,000 crore',
                '₹1 lakh crore',
                '₹1.54 lakh crore',
                '₹2 lakh crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Defence production reached ₹1.54 lakh crore in FY 2024–25.'
        },
        {
            'text': 'Which policy document has improved speed, transparency, and self-reliance in defence capital procurement?',
            'options': [
                'National Defence Policy 2018',
                'Defence Acquisition Procedure (DAP) 2020',
                'Industrial Policy 2020',
                'National Security Policy 2022'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'DAP 2020 streamlined defence procurement and promoted indigenous manufacturing.'
        },
        {
            'text': 'What is the Government\'s target for annual defence manufacturing by 2029?',
            'options': [
                '₹2 lakh crore',
                '₹2.5 lakh crore',
                '₹3 lakh crore',
                '₹5 lakh crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The target for annual defence manufacturing is ₹3 lakh crore by 2029.'
        },
        {
            'text': 'India\'s defence export target by 2029 is:',
            'options': [
                '₹20,000 crore',
                '₹30,000 crore',
                '₹40,000 crore',
                '₹50,000 crore'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'The target is ₹50,000 crore in defence exports by 2029.'
        },
        {
            'text': 'Which two states host India\'s Defence Industrial Corridors?',
            'options': [
                'Gujarat and Maharashtra',
                'Uttar Pradesh and Tamil Nadu',
                'Karnataka and Telangana',
                'Odisha and Andhra Pradesh'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'The Defence Industrial Corridors are in Uttar Pradesh and Tamil Nadu.'
        },
        {
            'text': 'Around how many MSMEs are contributing to India\'s defence manufacturing ecosystem?',
            'options': [
                '5,000',
                '8,000',
                '12,000',
                'Nearly 16,000'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'Nearly 16,000 MSMEs are contributing to India\'s defence manufacturing ecosystem.'
        },
        {
            'text': 'The Ministry of Defence signed a record how many contracts in FY 2024–25?',
            'options': [
                '120',
                '145',
                '193',
                '220'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Ministry of Defence signed a record 193 contracts in FY 2024–25.'
        },
        {
            'text': 'India\'s cumulative merchandise and services exports during April–January 2025–26 were estimated at:',
            'options': [
                'USD 600 billion',
                'USD 650 billion',
                'USD 720.76 billion',
                'USD 800 billion'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'India\'s cumulative exports reached USD 720.76 billion during April–January 2025–26.'
        },
        {
            'text': 'India\'s cumulative exports during April–January 2025–26 grew by approximately:',
            'options': [
                '3.5%',
                '4.8%',
                '6.15%',
                '8.2%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Exports increased by an estimated 6.15% year-on-year.'
        },
        {
            'text': 'According to UNCTAD\'s trade diversity indices, India ranks among the top ____ economies of the Global South for diversity of traded products.',
            'options': [
                'Two',
                'Three',
                'Five',
                'Ten'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'UNCTAD ranks India among the top five Global South economies for the diversity of traded products.'
        },
        {
            'text': 'India ranks among the top ____ economies of the Global South in the diversity of its trade partnerships.',
            'options': [
                'Two',
                'Three',
                'Four',
                'Five'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'India ranks among the top three Global South economies for the diversity of trade partnerships.'
        },
        # Q481-Q500: More topics
        {
            'text': 'Which export category recorded the highest growth in January 2025 (YoY)?',
            'options': [
                'Electronic Goods',
                'Petroleum Products',
                'Other Cereals',
                'Pharmaceuticals'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Other cereals recorded the highest year-on-year export growth of 88.49%.'
        },
        {
            'text': 'Coffee exports registered approximately what percentage growth in January 2025 (YoY)?',
            'options': [
                '18.25%',
                '24.60%',
                '36.03%',
                '52.15%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Coffee exports grew by 36.03% year-on-year.'
        },
        {
            'text': 'India is the world\'s ____ largest exporter of refined petroleum products.',
            'options': [
                'Third',
                'Fifth',
                'Seventh',
                'Tenth'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'India ranks as the seventh-largest exporter of refined petroleum products globally.'
        },
        {
            'text': 'By FY25, electronic goods became India\'s ____ largest export category.',
            'options': [
                'First',
                'Second',
                'Third',
                'Fifth'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Electronics emerged as India\'s third-largest export category in FY25.'
        },
        {
            'text': 'Smartphone exports during the first five months of FY 2025–26 touched approximately:',
            'options': [
                '₹50,000 crore',
                '₹75,000 crore',
                '₹1 lakh crore',
                '₹1.5 lakh crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Smartphone exports touched ₹1 lakh crore, showing a 55% increase.'
        },
        {
            'text': 'India accounts for approximately what share of global pharmaceutical exports by value?',
            'options': [
                '1%',
                '3%',
                '5%',
                '8%'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'India accounts for approximately 3% of global pharmaceutical exports by value.'
        },
        {
            'text': 'India is the ____ largest global exporter of textiles and apparel.',
            'options': [
                'Third',
                'Fourth',
                'Sixth',
                'Eighth'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'India ranks sixth in textile and apparel exports worldwide.'
        },
        {
            'text': 'India\'s defence products are now exported to more than:',
            'options': [
                '50 countries',
                '75 countries',
                '100 countries',
                '150 countries'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'Indian defence products are exported to over 100 countries.'
        },
        {
            'text': 'The Export Promotion Mission (EPM) has been approved with a total outlay of:',
            'options': [
                '₹15,000 crore',
                '₹20,000 crore',
                '₹25,060 crore',
                '₹30,000 crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The EPM has an outlay of ₹25,060 crore for FY2025–26 to FY2030–31.'
        },
        {
            'text': 'The Export Promotion Mission covers the period:',
            'options': [
                'FY 2024–25 to FY 2028–29',
                'FY 2025–26 to FY 2030–31',
                'FY 2026–27 to FY 2031–32',
                'FY 2025–26 to FY 2029–30'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'The EPM covers FY 2025–26 to FY 2030–31.'
        },
        {
            'text': 'The vision of "Viksit Bharat" aims to be achieved by which year?',
            'options': [
                '2030',
                '2035',
                '2047',
                '2050'
            ],
            'correct': 2,
            'difficulty': 'easy',
            'explanation': 'The vision of Viksit Bharat aims to be achieved by 2047.'
        },
        {
            'text': 'India\'s digital transformation is primarily powered by:',
            'options': [
                'Imported software',
                'Digital Public Infrastructure (DPI)',
                'Cryptocurrency',
                'Blockchain only'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'India\'s digital transformation is powered by Digital Public Infrastructure (DPI).'
        },
        {
            'text': 'Which initiative focuses on making India self-reliant in manufacturing?',
            'options': [
                'Startup India',
                'Digital India',
                'Atmanirbhar Bharat',
                'Skill India'
            ],
            'correct': 2,
            'difficulty': 'easy',
            'explanation': 'Atmanirbhar Bharat focuses on making India self-reliant in manufacturing.'
        },
        {
            'text': 'Which flagship initiative promotes domestic manufacturing in India?',
            'options': [
                'Make in India',
                'PM Gati Shakti',
                'Smart Cities Mission',
                'BharatNet'
            ],
            'correct': 0,
            'difficulty': 'easy',
            'explanation': 'Make in India promotes domestic manufacturing in India.'
        },
        {
            'text': 'Which scheme provides incentives based on production to manufacturers?',
            'options': [
                'PM-KISAN',
                'Production Linked Incentive (PLI) Scheme',
                'PMAY',
                'SVAMITVA'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'The Production Linked Incentive (PLI) Scheme provides incentives based on production.'
        },
        {
            'text': 'Electronics production in India increased from ₹1.9 lakh crore in 2014–15 to about ____ in 2024–25.',
            'options': [
                '₹6 lakh crore',
                '₹8 lakh crore',
                '₹11.3 lakh crore',
                '₹15 lakh crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Electronics production reached ₹11.3 lakh crore in 2024–25.'
        },
        {
            'text': 'India has attracted over how much FDI in electronics manufacturing since 2020–21?',
            'options': [
                'USD 2 billion',
                'USD 3 billion',
                'USD 4 billion',
                'USD 8 billion'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Electronics manufacturing attracted over USD 4 billion in FDI.'
        },
        {
            'text': 'Around how many jobs have been generated by the electronics manufacturing sector in the last decade?',
            'options': [
                '10 lakh',
                '15 lakh',
                '20 lakh',
                '25 lakh'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'Around 25 lakh jobs were created by the electronics manufacturing sector.'
        },
        {
            'text': 'Mobile phone production increased from ₹18,000 crore in 2014–15 to approximately ____ in 2024–25.',
            'options': [
                '₹3 lakh crore',
                '₹4 lakh crore',
                '₹5.45 lakh crore',
                '₹6 lakh crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Mobile manufacturing rose 28-fold to ₹5.45 lakh crore.'
        },
        {
            'text': 'India currently has more than how many mobile manufacturing units?',
            'options': [
                '100',
                '200',
                '300',
                '500'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'India currently has more than 300 mobile manufacturing units.'
        }
    ]

    # PART 10: Questions 501-530 (Additional)
    part10_questions = [
        {
            'text': 'India is currently the world\'s ____ largest mobile phone manufacturer.',
            'options': [
                'First',
                'Second',
                'Third',
                'Fourth'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'India is the second-largest mobile phone manufacturer in the world.'
        },
        {
            'text': 'India Semiconductor Mission 2.0 was announced in which Budget?',
            'options': [
                'Union Budget 2024–25',
                'Union Budget 2025–26',
                'Union Budget 2026–27',
                'Interim Budget 2026'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'India Semiconductor Mission 2.0 was announced in Union Budget 2026–27.'
        },
        {
            'text': 'The expanded Electronics Components Manufacturing Scheme has an outlay of:',
            'options': [
                '₹22,919 crore',
                '₹30,000 crore',
                '₹40,000 crore',
                '₹50,000 crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The expanded Electronics Components Manufacturing Scheme has an outlay of ₹40,000 crore.'
        },
        {
            'text': 'One of India\'s first end-to-end OSAT semiconductor facilities was inaugurated in:',
            'options': [
                'Chennai',
                'Hyderabad',
                'Sanand',
                'Noida'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'The OSAT facility was inaugurated in Sanand, Gujarat.'
        },
        {
            'text': 'Sanand, where the OSAT facility is located, is in which state?',
            'options': [
                'Maharashtra',
                'Gujarat',
                'Karnataka',
                'Telangana'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'Sanand is in Gujarat.'
        },
        {
            'text': 'India has approved how many semiconductor projects across six states?',
            'options': [
                '6',
                '8',
                '10',
                '12'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'India has approved 10 semiconductor projects across six states.'
        },
        {
            'text': 'Total investment approved for semiconductor projects is about:',
            'options': [
                '₹75,000 crore',
                '₹1 lakh crore',
                '₹1.6 lakh crore',
                '₹2 lakh crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Total investment approved for semiconductor projects is about ₹1.6 lakh crore.'
        },
        {
            'text': 'India is the world\'s largest market for:',
            'options': [
                'Passenger cars',
                'Two-wheelers and three-wheelers',
                'Heavy trucks',
                'Electric buses'
            ],
            'correct': 1,
            'difficulty': 'easy',
            'explanation': 'India is the world\'s largest market for two-wheelers and three-wheelers.'
        },
        {
            'text': 'India ranks ____ globally in passenger and commercial vehicle production.',
            'options': [
                'First',
                'Second',
                'Third',
                'Fourth'
            ],
            'correct': 2,
            'difficulty': 'medium',
            'explanation': 'India ranks third globally in passenger and commercial vehicle production.'
        },
        {
            'text': 'The Export Promotion Mission (EPM) operates through how many integrated sub-schemes?',
            'options': [
                'One',
                'Two',
                'Three',
                'Four'
            ],
            'correct': 1,
            'difficulty': 'medium',
            'explanation': 'EPM operates through two integrated sub-schemes: Niryat Protsahan and Niryat Disha.'
        },
        {
            'text': 'Which of the following is an integrated sub-scheme under the Export Promotion Mission?',
            'options': [
                'Niryat Protsahan',
                'Startup India',
                'PM Gati Shakti',
                'Make in India'
            ],
            'correct': 0,
            'difficulty': 'medium',
            'explanation': 'Niryat Protsahan is one of the two integrated sub-schemes under EPM.'
        },
        {
            'text': 'Which EPM intervention promotes export factoring as a working capital solution for MSMEs?',
            'options': [
                'FLOW',
                'TRACE',
                'Support for Alternative Trade Instruments (Export Factoring)',
                'LIFT'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Support for Alternative Trade Instruments promotes export factoring for MSMEs.'
        },
        {
            'text': 'Under the Export Factoring initiative, the interest subvention is:',
            'options': [
                '1.50%',
                '2.00%',
                '2.75%',
                '4.00%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The interest subvention under Export Factoring is 2.75%.'
        },
        {
            'text': 'Under the Export Factoring initiative, the annual interest subsidy for an MSME is capped at:',
            'options': [
                '₹10 lakh',
                '₹25 lakh',
                '₹50 lakh',
                '₹1 crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The annual interest subsidy is capped at ₹50 lakh per MSME.'
        },
        {
            'text': 'Which EPM intervention supports credit for e-commerce exporters?',
            'options': [
                'TRACE',
                'INSIGHT',
                'Credit Assistance for E-Commerce Exporters',
                'FLOW'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Credit Assistance for E-Commerce Exporters supports credit for e-commerce exporters.'
        },
        {
            'text': 'Under the Direct E-Commerce Credit Facility, the maximum credit available is:',
            'options': [
                '₹25 lakh',
                '₹50 lakh',
                '₹75 lakh',
                '₹1 crore'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'The Direct E-Commerce Credit Facility provides loans up to ₹50 lakh.'
        },
        {
            'text': 'The guarantee coverage under the Direct E-Commerce Credit Facility is:',
            'options': [
                '50%',
                '75%',
                '90%',
                '100%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The guarantee coverage under the Direct E-Commerce Credit Facility is 90%.'
        },
        {
            'text': 'The Overseas Inventory Credit Facility provides loans up to:',
            'options': [
                '₹2 crore',
                '₹3 crore',
                '₹5 crore',
                '₹10 crore'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The Overseas Inventory Credit Facility provides loans up to ₹5 crore.'
        },
        {
            'text': 'The guarantee coverage under the Overseas Inventory Credit Facility is:',
            'options': [
                '50%',
                '60%',
                '75%',
                '90%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'The guarantee coverage under the Overseas Inventory Credit Facility is 75%.'
        },
        {
            'text': 'TRACE stands for:',
            'options': [
                'Trade Regulations, Accreditation & Compliance Enablement',
                'Trade Reform and Customs Enhancement',
                'Transport Regulation and Export Council',
                'Technology for Rural Commerce Expansion'
            ],
            'correct': 0,
            'difficulty': 'hard',
            'explanation': 'TRACE stands for Trade Regulations, Accreditation & Compliance Enablement.'
        },
        {
            'text': 'Under TRACE, reimbursement for the Positive List is up to:',
            'options': [
                '40%',
                '50%',
                '60%',
                '75%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Under TRACE, reimbursement for the Positive List is up to 60%.'
        },
        {
            'text': 'Under TRACE, reimbursement for the Priority Positive List is:',
            'options': [
                '60%',
                '70%',
                '75%',
                '100%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Under TRACE, reimbursement for the Priority Positive List is 75%.'
        },
        {
            'text': 'The reimbursement under TRACE is capped at:',
            'options': [
                '₹10 lakh per IEC',
                '₹15 lakh per IEC',
                '₹20 lakh per IEC',
                '₹25 lakh per IEC annually'
            ],
            'correct': 3,
            'difficulty': 'hard',
            'explanation': 'The reimbursement under TRACE is capped at ₹25 lakh per IEC annually.'
        },
        {
            'text': 'FLOW under the Export Promotion Mission is related to:',
            'options': [
                'Agricultural exports',
                'Overseas warehousing and fulfilment',
                'Defence exports',
                'Port modernization'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'FLOW assists exporters with overseas warehousing and fulfilment.'
        },
        {
            'text': 'LIFT primarily provides reimbursement for:',
            'options': [
                'Customs duty',
                'Freight costs',
                'GST',
                'Insurance premium'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'LIFT provides reimbursement for freight costs.'
        },
        {
            'text': 'Under LIFT, reimbursement of eligible freight costs is up to:',
            'options': [
                '20%',
                '25%',
                '30%',
                '50%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Under LIFT, reimbursement of eligible freight costs is up to 30%.'
        },
        {
            'text': 'Under LIFT, reimbursement is capped at:',
            'options': [
                '₹10 lakh',
                '₹15 lakh',
                '₹20 lakh per IEC per financial year',
                '₹25 lakh'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Under LIFT, reimbursement is capped at ₹20 lakh per IEC per financial year.'
        },
        {
            'text': 'INSIGHT under the EPM is primarily intended to strengthen:',
            'options': [
                'Defence procurement',
                'Exporter capacity building and trade intelligence',
                'GST collection',
                'Tourism promotion'
            ],
            'correct': 1,
            'difficulty': 'hard',
            'explanation': 'INSIGHT strengthens exporter capacity building and trade intelligence.'
        },
        {
            'text': 'India\'s services exports reached an all-time high of approximately ____ in FY25.',
            'options': [
                'USD 250 billion',
                'USD 300 billion',
                'USD 387.5 billion',
                'USD 450 billion'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'India\'s services exports reached USD 387.5 billion in FY25.'
        },
        {
            'text': 'Services exports in FY25 grew by approximately:',
            'options': [
                '8.5%',
                '10.2%',
                '13.6%',
                '15.8%'
            ],
            'correct': 2,
            'difficulty': 'hard',
            'explanation': 'Services exports grew by 13.6% in FY25.'
        }
    ]

    # Combine all parts with their data
    all_new_parts = [
        {'name': 'Current Affairs 2024 - Part 6', 'slug': 'current-affairs-2024-part6',
         'description': 'Policy Reforms & Business Environment (Questions 301-350)', 'questions': part6_questions},
        {'name': 'Current Affairs 2024 - Part 7', 'slug': 'current-affairs-2024-part7',
         'description': 'Tax Reforms & Digital Blueprint (Questions 351-400)', 'questions': part7_questions},
        {'name': 'Current Affairs 2024 - Part 8', 'slug': 'current-affairs-2024-part8',
         'description': 'BRAP, Digital Infrastructure & Logistics (Questions 401-450)', 'questions': part8_questions},
        {'name': 'Current Affairs 2024 - Part 9', 'slug': 'current-affairs-2024-part9',
         'description': 'Defence, Pharma, Electronics & Trade (Questions 451-500)', 'questions': part9_questions},
        {'name': 'Current Affairs 2024 - Part 10', 'slug': 'current-affairs-2024-part10',
         'description': 'Semiconductors, EPM & Services (Questions 501-530)', 'questions': part10_questions}
    ]

    print("\n📚 Adding 5 New Mock Tests with 230+ New Questions...")
    total_questions_created = 0
    
    for part in all_new_parts:
        print(f"\n📝 Creating {part['name']}...")
        
        # Check if mock test already exists
        existing_mock = MockTest.objects.filter(slug=f'{part["slug"]}-mock').first()
        if existing_mock:
            print(f"  ⚠️ Mock test already exists: {existing_mock.name}")
            print(f"  ℹ️ Skipping to avoid duplicates...")
            continue
        
        # CREATE MOCK TEST
        mock_test = MockTest.objects.create(
            name=f'{part["name"]} ({len(part["questions"])} Questions)',
            slug=f'{part["slug"]}-mock',
            exam=main_exam,
            description=part['description'],
            duration_minutes=60,
            total_questions=len(part['questions']),
            total_marks=len(part['questions']) * 2,
            is_paid=False,
            price=0,
            attempts_allowed=10,
            is_active=True
        )
        print(f"  ✓ Mock Test Created: {mock_test.name}")
        
        # Create questions (all linked to MAIN exam and subject)
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
            
            # Use explanation if available, else "N/A"
            explanation = q_data.get('explanation', 'N/A')
            
            question = Question.objects.create(
                exam=main_exam,
                subject=main_subject,
                question_text=q_data['text'],
                question_type='mcq',
                difficulty=q_data.get('difficulty', 'medium'),
                marks=2,
                negative_marks=0.25,
                explanation=explanation,
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
        
        print(f"  ✓ Created {len(created_questions)} questions with explanations")
        
        # Add questions to mock test
        for idx, question in enumerate(created_questions):
            MockTestQuestion.objects.create(
                mock_test=mock_test,
                question=question,
                marks=2,
                order=idx
            )
        
        total_questions_created += len(created_questions)
        print(f"    └─ Added {mock_test.total_questions} questions to mock test")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ NEW MOCK TESTS ADDED SUCCESSFULLY!")
    print("=" * 80)
    
    print("\n📊 FINAL SUMMARY:")
    print(f"   • Main Exam: {main_exam.name} (ID: {main_exam.id})")
    print(f"   • Total Mock Tests: {MockTest.objects.filter(exam=main_exam).count()}")
    print(f"   • New Questions Added: {total_questions_created}")
    print(f"   • All questions have explanations (or 'N/A')")
    print(f"   • All tests are FREE (is_paid=False, price=0)")
    
    print("\n📋 ALL MOCK TESTS:")
    mock_tests = MockTest.objects.filter(exam=main_exam).order_by('id')
    for i, mt in enumerate(mock_tests, 1):
        q_count = MockTestQuestion.objects.filter(mock_test=mt).count()
        print(f"   {i}. {mt.name}: {q_count} questions")
    
    print("\n🎯 To take the mock tests:")
    print("   1. Login to the application")
    print("   2. Go to Mock Tests section")
    print("   3. Select any of the Current Affairs mock tests")
    print("   4. Start practicing!")
    
    print("\n💡 Features Added:")
    print("   • All questions include explanations")
    print("   • 5 new mock tests (Parts 6-10)")
    print("   • 230+ new unique questions")
    print("   • All linked to the same exam")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    try:
        add_new_mock_tests()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)