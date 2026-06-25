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

def create_current_affairs_mock_test_part3():
    print("=" * 80)
    print("📰 CREATING CURRENT AFFAIRS MOCK TEST PART 3 (QUESTIONS 201-300)")
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
        slug='current-affairs-2024-part3',
        defaults={
            'name': 'Current Affairs 2024 - Part 3',
            'short_name': 'CA 2024 P3',
            'category': exam_category,
            'exam_level': 'national',
            'duration_minutes': 60,
            'total_marks': 100,
            'total_questions': 100,
            'negative_marking': False,
            'description': 'Comprehensive Current Affairs Mock Test Part 3 covering National Sports Awards, Emmy Awards 2024',
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
        name='Current Affairs 2024 - Part 3',
        defaults={'weightage': 100, 'order': 1}
    )
    print(f"✓ Subject: {subject.name}")
    
    # Clear existing questions for this exam
    Question.objects.filter(exam=exam).delete()
    print("✓ Cleared existing questions")
    
    # All 100 Current Affairs Questions (201-300)
    questions_data = [
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
            'text': 'Who won Lead Actor in Drama Series at Emmy Awards 2024?',
            'options': ['Kieran Culkin', 'Pedro Pascal', 'Jeremy Allen White', 'Steven Yeun'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won Lead Actress in Drama Series at Emmy Awards 2024?',
            'options': ['Sarah Snook', 'Jennifer Coolidge', 'Ali Wong', 'Emma Stone'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Who won Lead Actor in Limited Series at Emmy Awards 2024?',
            'options': ['Steven Yeun', 'Kieran Culkin', 'Paul Walter Hauser', 'Jeremy Allen White'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Who won Lead Actress in Limited Series at Emmy Awards 2024?',
            'options': ['Ali Wong', 'Sarah Snook', 'Emma Stone', 'Ayo Edebiri'],
            'correct': 0,
            'difficulty': 'hard'
        },
        {
            'text': 'Variety Special (Live) winner at Emmy Awards 2024 was:',
            'options': ['Elton John Live: Farewell from Dodger Stadium', 'Taylor Swift Special', 'Beyonce Special', 'Adele Special'],
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
            'text': 'Best Original Score composer at Golden Globes 2024 was:',
            'options': ['Ludwig Göransson', 'Hans Zimmer', 'John Williams', 'AR Rahman'],
            'correct': 0,
            'difficulty': 'hard'
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
            'text': 'Golden Globe host venue is located in which city?',
            'options': ['Beverly Hills', 'Los Angeles', 'Hollywood', 'New York'],
            'correct': 0,
            'difficulty': 'medium'
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
            'text': 'Best Supporting Actor at Golden Globes 2024 was from which film?',
            'options': ['Oppenheimer', 'Barbie', 'Poor Things', 'The Holdovers'],
            'correct': 0,
            'difficulty': 'medium'
        },
        {
            'text': 'Best Supporting Actress at Golden Globes 2024 was from which film?',
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
    
    # Create questions
    print("\n📝 Creating 100 Current Affairs Questions (201-300)...")
    
    created_questions = []
    for idx, q_data in enumerate(questions_data, 201):
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
    
    print(f"\n✓ Created {len(created_questions)} questions (201-300)")
    
    # Create Mock Test
    print("\n🎯 Creating Current Affairs Mock Test Part 3...")
    
    # Delete existing mock test
    MockTest.objects.filter(slug='current-affairs-mock-test-2024-part3').delete()
    
    mock_test = MockTest.objects.create(
        name='Current Affairs Mock Test 2024 - Part 3 (201-300 Questions)',
        slug='current-affairs-mock-test-2024-part3',
        exam=exam,
        description='Comprehensive mock test covering National Sports Awards, Emmy Awards 2024 & Golden Globes 2024',
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
    print("✅ CURRENT AFFAIRS MOCK TEST PART 3 CREATION COMPLETED!")
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
    print("   3. Select 'Current Affairs Mock Test 2024 - Part 3 (201-300 Questions)'")
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
        create_current_affairs_mock_test_part3()
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)