'''DATA RETRIVE DATA STORED '''
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Employee, TestResult, Application,WritingNotes
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import TestResult
from .models import ReadingSkill, VocabularyWord, ReadingPDF
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VocabularyWord

from .models import ReadingPDF


#Notesss
from .models import Notes

def is_superstudent(user):
    return hasattr(user, "profile") and user.profile.role == "superstudent"


@login_required
def notes_list(request):
    if not is_superstudent(request.user):
        messages.error(request, "Only Super Students can manage notes!")
        return redirect("home")

    notes = Notes.objects.filter(user=request.user)
    return render(request, "myapp/notes_list.html", {"notes": notes})


@login_required
def notes_create(request):
    if not is_superstudent(request.user):
        return redirect("home")

    if request.method == "POST":
        Notes.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            content=request.POST.get("content")
        )
        return redirect("notes_list")

    return render(request, "myapp/notes_form.html")


@login_required
def notes_edit(request, id):
    if not is_superstudent(request.user):
        return redirect("home")

    note = Notes.objects.get(id=id, user=request.user)

    if request.method == "POST":
        note.title = request.POST.get("title")
        note.content = request.POST.get("content")
        note.save()
        return redirect("notes_list")

    return render(request, "myapp/notes_form.html", {"note": note})


@login_required
def notes_delete(request, id):
    if not is_superstudent(request.user):
        return redirect("home")

    note = Notes.objects.get(id=id, user=request.user)
    note.delete()
    return redirect("notes_list")


def is_superstudent(user):
    return hasattr(user, "profile") and user.profile.role == "superstudent"

# -----------------------------
# READING PDF CRUD (SUPERSTUDENT)
# -----------------------------

@login_required
def pdf_list(request):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    pdfs = ReadingPDF.objects.all()
    return render(request, "myapp/pdf_list.html", {"pdfs": pdfs})


@login_required
def pdf_create(request):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title")
        pdf_file = request.FILES.get("pdf_file")

        ReadingPDF.objects.create(title=title, pdf_file=pdf_file)
        return redirect("pdf_list")

    return render(request, "myapp/pdf_form.html")


@login_required
def pdf_edit(request, id):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    pdf = get_object_or_404(ReadingPDF, id=id)

    if request.method == "POST":
        pdf.title = request.POST.get("title")
        if request.FILES.get("pdf_file"):
            pdf.pdf_file = request.FILES.get("pdf_file")
        pdf.save()
        return redirect("pdf_list")

    return render(request, "myapp/pdf_form.html", {"pdf": pdf})


@login_required
def pdf_delete(request, id):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    pdf = get_object_or_404(ReadingPDF, id=id)
    pdf.delete()
    return redirect("pdf_list")

# -----------------------------
# VOCABULARY CRUD (SUPERSTUDENT)
# -----------------------------

@login_required
def vocab_list(request):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    words = VocabularyWord.objects.all()
    return render(request, "myapp/vocab_list.html", {"words": words})


@login_required
def vocab_create(request):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    if request.method == "POST":
        word = request.POST.get("word")
        meaning = request.POST.get("meaning")
        example = request.POST.get("example")
        VocabularyWord.objects.create(word=word, meaning=meaning, example=example)
        return redirect("vocab_list")

    return render(request, "myapp/vocab_form.html")


@login_required
def vocab_edit(request, id):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    word = get_object_or_404(VocabularyWord, id=id)

    if request.method == "POST":
        word.word = request.POST.get("word")
        word.meaning = request.POST.get("meaning")
        word.example = request.POST.get("example")
        word.save()
        return redirect("vocab_list")

    return render(request, "myapp/vocab_form.html", {"word": word})


@login_required
def vocab_delete(request, id):
    if not request.user.profile.is_superstudent:
        return redirect("home")

    word = get_object_or_404(VocabularyWord, id=id)
    word.delete()
    return redirect("vocab_list")

# -------------------- READING SKILLS ------------------------

@login_required
def skills_list(request):
    if not is_superstudent(request.user):
        return redirect("home")
    skills = ReadingSkill.objects.all()
    return render(request, "myapp/skills_list.html", {"skills": skills})


@login_required
def skills_create(request):
    if not is_superstudent(request.user):
        return redirect("home")
    if request.method == "POST":
        ReadingSkill.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
        )
        return redirect("skills_list")
    return render(request, "myapp/skills_form.html")


@login_required
def skills_edit(request, id):
    if not is_superstudent(request.user):
        return redirect("home")

    skill = ReadingSkill.objects.get(id=id)

    if request.method == "POST":
        skill.title = request.POST["title"]
        skill.description = request.POST["description"]
        skill.save()
        return redirect("skills_list")

    return render(request, "myapp/skills_form.html", {"skill": skill})


@login_required
def skills_delete(request, id):
    if not is_superstudent(request.user):
        return redirect("home")

    ReadingSkill.objects.get(id=id).delete()
    return redirect("skills_list")


@login_required
@require_POST
def save_test_score(request, test_type):
    """
    Universal function to save score for any test:
    listening, speaking, reading, writing etc.
    """
    try:
        score = int(request.POST.get("score", 0))
    except:
        score = 0

    TestResult.objects.create(
        user=request.user,
        test_type=test_type,
        score=score,
        date_taken=timezone.now()
    )

    messages.success(request, f"{test_type.capitalize()} Test saved! Score: {score}")
    return redirect("tests")
# -------------------- VOCABULARY ------------------------

@login_required
def vocab_list(request):
    if not is_superstudent(request.user):
        return redirect("home")
    words = VocabularyWord.objects.all()
    return render(request, "myapp/vocab_list.html", {"words": words})


@login_required
def vocab_create(request):
    if not is_superstudent(request.user):
        return redirect("home")
    if request.method == "POST":
        VocabularyWord.objects.create(
            word=request.POST["word"],
            meaning=request.POST["meaning"],
            example=request.POST.get("example", "")
        )
        return redirect("vocab_list")

    return render(request, "myapp/vocab_form.html")

# -------------------- PDF READING ------------------------

@login_required
def pdf_list(request):
    if not is_superstudent(request.user):
        return redirect("home")
    pdfs = ReadingPDF.objects.all()
    return render(request, "myapp/pdf_list.html", {"pdfs": pdfs})


@login_required
def pdf_create(request):
    if not is_superstudent(request.user):
        return redirect("home")

    if request.method == "POST":
        ReadingPDF.objects.create(
            title=request.POST["title"],
            pdf_file=request.FILES["pdf_file"]
        )
        return redirect("pdf_list")

    return render(request, "myapp/pdf_form.html")

# ========== UPDATE THIS VIEW ==========
# Landing Page
def landing(request):
    # Check if the user was redirected here because a session expired
    if request.method == 'GET' and 'next' in request.GET:
        if not request.user.is_authenticated:
             messages.warning(request, 'Your session has expired. Please log in or register to continue.')
    return render(request, 'myapp/landing.html')

# Home Page
def home(request):
    return render(request, 'myapp/home.html')

# Register from landing page
def register_employee(request):
    if request.method == 'POST':
        fullname = request.POST.get('name')
        username = request.POST.get('department')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # ✅ Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('landing')

        # ✅ Check duplicates
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('landing')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('landing')

        # ✅ Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = fullname
        user.save()

        # ✅ Also save into Employee table (optional)
        Employee.objects.create(
            name=fullname,
            department=username,   # saving username in department field
            email=email,
            password=password
        )

        messages.success(request, "Registration successful! You can now login.")
        return redirect('login')

    return redirect('home')

# Success Page
def success_page(request):
    return render(request, 'myapp/success.html')

# About Page
def about_page(request):
    return render(request, 'myapp/about.html')

# Features Page
def feature_page(request):
    return render(request, 'myapp/features.html')

# Contact Page
def contact_page(request):
    return render(request, 'myapp/contact.html')

# Country Details Page
def country_detail(request, code):
    country_data = {
        "uk": {
            "name": "United Kingdom",
            "flag": "https://flagcdn.com/w80/gb.png",
            "description": "The UK is known for world-class education, global opportunities, and top-ranked universities.",
            
            "universities": [
                {"name": "University of Oxford", "website": "https://www.ox.ac.uk"},
                {"name": "University of Cambridge", "website": "https://www.cam.ac.uk"},
                {"name": "Imperial College London", "website": "https://www.imperial.ac.uk"},
                {"name": "University College London (UCL)", "website": "https://www.ucl.ac.uk"},
            ],

            "best_courses": [
                "Business & Management",
                "Computer Science",
                "Medicine",
                "Data Science",
                "Engineering"
            ],

            "scholarships": [
                "Chevening Scholarship",
                "Commonwealth Scholarship",
                "GREAT Scholarship",
                "Rhodes Scholarship"
            ],

            "cost_of_living": "£900 – £1,400 per month",
            "tuition_fees": "£10,000 – £38,000 per year (depending on course)",
            "visa_requirements": [
                "Offer letter from UK university",
                "Proof of funds",
                "IELTS/TOEFL Score",
                "CAS Letter",
                "Tuberculosis Test"
            ]
        },

        "us": {
            "name": "United States",
            "flag": "https://flagcdn.com/w80/us.png",
            "description": "The USA offers flexible education, research opportunities, and top QS-ranked universities.",
            
            "universities": [
                {"name": "Harvard University", "website": "https://www.harvard.edu"},
                {"name": "Stanford University", "website": "https://www.stanford.edu"},
                {"name": "MIT", "website": "https://www.mit.edu"},
                {"name": "UC Berkeley", "website": "https://www.berkeley.edu"},
            ],

            "best_courses": [
                "Computer Science",
                "AI & Machine Learning",
                "Business Analytics",
                "Aerospace Engineering",
                "Biotechnology"
            ],

            "scholarships": [
                "Fulbright Scholarship",
                "Stanford Knight-Hennessy Scholarship",
                "Harvard Financial Aid",
                "AAUW International Scholarship"
            ],

            "cost_of_living": "$1,000 – $1,800 per month",
            "tuition_fees": "$20,000 – $55,000 per year",
            "visa_requirements": [
                "I-20 Form",
                "SEVIS Fee Payment",
                "Financial Proof",
                "Valid Passport",
                "Academic Transcripts"
            ]
        },

        "ca": {
            "name": "Canada",
            "flag": "https://flagcdn.com/w80/ca.png",
            "description": "Canada is known for safe living, PR opportunities, and globally recognized degrees.",
            
            "universities": [
                {"name": "University of Toronto", "website": "https://www.utoronto.ca"},
                {"name": "McGill University", "website": "https://www.mcgill.ca"},
                {"name": "University of British Columbia", "website": "https://www.ubc.ca"},
                {"name": "University of Waterloo", "website": "https://uwaterloo.ca"},
            ],

            "best_courses": [
                "Computer Science",
                "Cybersecurity",
                "Business Management",
                "Mechanical Engineering",
                "Nursing"
            ],

            "scholarships": [
                "Vanier Graduate Scholarship",
                "Lester B. Pearson Scholarship",
                "UBC International Scholars",
                "Ontario Graduate Scholarship"
            ],

            "cost_of_living": "CAD $900 – $1,400 per month",
            "tuition_fees": "CAD $15,000 – $40,000 per year",
            "visa_requirements": [
                "Proof of funds",
                "Medical exam",
                "Offer letter",
                "Biometrics",
                "English proficiency"
            ]
        },

        "au": {
            "name": "Australia",
            "flag": "https://flagcdn.com/w80/au.png",
            "description": "Australia provides high-quality education, part-time work, and post-study visa options.",
            
            "universities": [
                {"name": "University of Melbourne", "website": "https://www.unimelb.edu.au"},
                {"name": "Australian National University", "website": "https://www.anu.edu.au"},
                {"name": "University of Sydney", "website": "https://www.sydney.edu.au"},
                {"name": "Monash University", "website": "https://www.monash.edu"},
            ],

            "best_courses": [
                "Nursing",
                "Information Technology",
                "Data Science",
                "Engineering",
                "MBA"
            ],

            "scholarships": [
                "Australia Awards Scholarship",
                "Destination Australia Scholarship",
                "ANU Global Scholarships",
                "Monash International Merit Scholarship"
            ],

            "cost_of_living": "AUD $1,200 – $1,800 per month",
            "tuition_fees": "AUD $20,000 – $45,000 per year",
            "visa_requirements": [
                "GTE Statement",
                "COE Letter",
                "Overseas Health Cover (OSHC)",
                "Financial Proof"
            ]
        },

        "de": {
            "name": "Germany",
            "flag": "https://flagcdn.com/w80/de.png",
            "description": "Germany offers world-class education with low or no tuition fees, especially for engineering and research programs.",
            
            "universities": [
                {"name": "Technical University of Munich", "website": "https://www.tum.de"},
                {"name": "Heidelberg University", "website": "https://www.uni-heidelberg.de"},
                {"name": "RWTH Aachen University", "website": "https://www.rwth-aachen.de"},
                {"name": "Humboldt University of Berlin", "website": "https://www.hu-berlin.de"},
            ],

            "best_courses": [
                "Mechanical Engineering",
                "Automobile Engineering",
                "Robotics & AI",
                "Computer Science",
                "Chemical Engineering"
            ],

            "scholarships": [
                "DAAD Scholarship",
                "Erasmus Scholarship",
                "Heinrich Böll Foundation Scholarship",
                "Deutschlandstipendium"
            ],

            "cost_of_living": "€800 – €1,000 per month",
            "tuition_fees": "Mostly Free (Public Universities) | Private: €5,000 – €20,000 per year",
            "visa_requirements": [
                "Blocked account (€11,208)",
                "Health insurance",
                "University admission letter",
                "Academic records"
            ]
        },

        "fr": {
            "name": "France",
            "flag": "https://flagcdn.com/w80/fr.png",
            "description": "France is known for high-quality education, strong cultural heritage, and top business schools.",
            
            "universities": [
                {"name": "Sorbonne University", "website": "https://www.sorbonne-universite.fr"},
                {"name": "École Polytechnique", "website": "https://www.polytechnique.edu"},
                {"name": "Sciences Po", "website": "https://www.sciencespo.fr"},
                {"name": "Université PSL", "website": "https://www.univ-psl.fr"},
            ],

            "best_courses": [
                "Fashion Designing",
                "Business Management",
                "International Relations",
                "Engineering"
            ],

            "scholarships": [
                "Eiffel Excellence Scholarship",
                "Campus France Scholarships",
                "École Polytechnique Scholarships"
            ],

            "cost_of_living": "€900 – €1,500 per month",
            "tuition_fees": "€3,000 – €12,000 per year",
            "visa_requirements": [
                "Campus France registration",
                "Financial proof",
                "University acceptance letter",
                "Medical insurance"
            ]
        },
        "de": {
    "name": "Germany",
    "flag": "https://flagcdn.com/w80/de.png",
    "description": "Germany offers world-class education with low or no tuition fees, especially for engineering and research programs.",

    "universities": [
        {"name": "Technical University of Munich", "website": "https://www.tum.de"},
        {"name": "Heidelberg University", "website": "https://www.uni-heidelberg.de"},
        {"name": "RWTH Aachen University", "website": "https://www.rwth-aachen.de"},
        {"name": "Humboldt University of Berlin", "website": "https://www.hu-berlin.de"},
    ],

    "best_courses": [
        "Mechanical Engineering",
        "Automobile Engineering",
        "Robotics & AI",
        "Data Science",
        "Computer Science"
    ],

    "scholarships": [
        "DAAD Scholarship",
        "Deutschlandstipendium",
        "Heinrich Böll Foundation Scholarship",
        "Erasmus Scholarship"
    ],

    "cost_of_living": "€850 – €1,100 per month",
    "tuition_fees": "Public Universities: Free or €1,500/year • Private: €5,000 – €20,000/year",

    "visa_requirements": [
        "Blocked Account (€11,208)",
        "Health Insurance",
        "University Admission Letter",
        "Academic Transcripts",
        "English/German Proficiency Certificate"
    ]
},

"fr": {
    "name": "France",
    "flag": "https://flagcdn.com/w80/fr.png",
    "description": "France is known for high-quality education, strong cultural heritage, and top business schools.",

    "universities": [
        {"name": "Sorbonne University", "website": "https://www.sorbonne-universite.fr"},
        {"name": "École Polytechnique", "website": "https://www.polytechnique.edu"},
        {"name": "Sciences Po", "website": "https://www.sciencespo.fr"},
        {"name": "Université PSL", "website": "https://www.univ-psl.fr"},
    ],

    "best_courses": [
        "Fashion Designing",
        "Business & Management",
        "International Relations",
        "Engineering",
        "Culinary Arts"
    ],

    "scholarships": [
        "Eiffel Excellence Scholarship",
        "Campus France Scholarships",
        "Charpak Scholarship",
        "École Polytechnique Scholarships"
    ],

    "cost_of_living": "€900 – €1,600 per month",
    "tuition_fees": "€3,000 – €12,000 per year",

    "visa_requirements": [
        "Campus France Registration",
        "University Acceptance Letter",
        "Medical Insurance",
        "Financial Proof",
        "Academic Records"
    ]
},

"nz": {
    "name": "New Zealand",
    "flag": "https://flagcdn.com/w80/nz.png",
    "description": "New Zealand offers a friendly environment, research-based education, and excellent post-study work opportunities.",

    "universities": [
        {"name": "University of Auckland", "website": "https://www.auckland.ac.nz"},
        {"name": "University of Otago", "website": "https://www.otago.ac.nz"},
        {"name": "Victoria University of Wellington", "website": "https://www.wgtn.ac.nz"},
        {"name": "Massey University", "website": "https://www.massey.ac.nz"},
    ],

    "best_courses": [
        "Agriculture",
        "Environmental Science",
        "Business",
        "Data Science",
        "Information Technology"
    ],

    "scholarships": [
        "New Zealand International Excellence Award",
        "University of Auckland Scholarships",
        "Victoria Tongarewa Scholarship",
        "Commonwealth Scholarship (NZ)"
    ],

    "cost_of_living": "NZD $1,200 – $1,800 per month",
    "tuition_fees": "NZD $20,000 – $40,000 per year",

    "visa_requirements": [
        "Offer Letter",
        "Proof of Funds",
        "Medical Test",
        "Police Verification",
        "English Proficiency (IELTS/TOEFL)"
    ]
},

"ie": {
    "name": "Ireland",
    "flag": "https://flagcdn.com/w80/ie.png",
    "description": "Ireland is a growing education hub for technology, business, and research with strong EU job market opportunities.",

    "universities": [
        {"name": "Trinity College Dublin", "website": "https://www.tcd.ie"},
        {"name": "University College Dublin", "website": "https://www.ucd.ie"},
        {"name": "University of Galway", "website": "https://www.universityofgalway.ie"},
        {"name": "University College Cork", "website": "https://www.ucc.ie"},
    ],

    "best_courses": [
        "Computer Science",
        "Cybersecurity",
        "Pharmaceutical Science",
        "Business",
        "Finance"
    ],

    "scholarships": [
        "Government of Ireland Scholarship",
        "UCD Global Excellence Scholarship",
        "Trinity Foundation Scholarship",
        "NUI Galway Merit Scholarship"
    ],

    "cost_of_living": "€900 – €1,400 per month",
    "tuition_fees": "€10,000 – €25,000 per year",

    "visa_requirements": [
        "Proof of Funds",
        "Offer Letter",
        "Private Medical Insurance",
        "Academic Documents",
        "English Test Score"
    ]
},

"sg": {
    "name": "Singapore",
    "flag": "https://flagcdn.com/w80/sg.png",
    "description": "Singapore is known for top global universities, strong safety, and Asia’s leading technology & business hub.",

    "universities": [
        {"name": "National University of Singapore (NUS)", "website": "https://nus.edu.sg"},
        {"name": "Nanyang Technological University (NTU)", "website": "https://www.ntu.edu.sg"},
        {"name": "Singapore Management University (SMU)", "website": "https://www.smu.edu.sg"},
        {"name": "James Cook University Singapore", "website": "https://www.jcu.edu.sg"},
    ],

    "best_courses": [
        "Engineering",
        "Computer Science",
        "Business",
        "Finance & Banking",
        "Logistics & Supply Chain"
    ],

    "scholarships": [
        "NUS Global Scholarship",
        "NTU Nanyang Scholarship",
        "SMU Merit Scholarship",
        "Singapore International Graduate Award (SINGA)"
    ],

    "cost_of_living": "SGD $1,200 – $2,000 per month",
    "tuition_fees": "SGD $15,000 – $45,000 per year",

    "visa_requirements": [
        "Student Pass Approval",
        "Offer Letter",
        "Financial Proof",
        "Medical Examination",
        "English Proficiency"
    ]
},

"ae": {
    "name": "United Arab Emirates (UAE)",
    "flag": "https://flagcdn.com/w80/ae.png",
    "description": "The UAE offers world-class campuses, tax-free salaries, a modern lifestyle, and excellent business opportunities.",

    "universities": [
        {"name": "Khalifa University", "website": "https://www.ku.ac.ae"},
        {"name": "NYU Abu Dhabi", "website": "https://nyuad.nyu.edu"},
        {"name": "University of Dubai", "website": "https://www.ud.ac.ae"},
        {"name": "American University of Sharjah", "website": "https://www.aus.edu"},
    ],

    "best_courses": [
        "AI & Robotics",
        "Aviation",
        "Business Management",
        "Civil Engineering",
        "Hospitality Management"
    ],

    "scholarships": [
        "Khalifa University Scholarship",
        "AUS International Student Scholarship",
        "NYUAD Full-Ride Scholarship",
        "University of Dubai Merit Scholarship"
    ],

    "cost_of_living": "AED 3,000 – 6,000 per month",
    "tuition_fees": "AED 40,000 – 90,000 per year",

    "visa_requirements": [
        "Offer Letter",
        "Medical Test",
        "Emirates ID Registration",
        "Financial Proof",
        "Valid Passport"
    ]
},

"ch": {
    "name": "Switzerland",
    "flag": "https://flagcdn.com/w80/ch.png",
    "description": "Switzerland is famous for top-class research, hospitality programs, and a high standard of living.",

    "universities": [
        {"name": "ETH Zurich", "website": "https://ethz.ch"},
        {"name": "EPFL", "website": "https://www.epfl.ch"},
        {"name": "University of Zurich", "website": "https://www.uzh.ch"},
        {"name": "University of Geneva", "website": "https://www.unige.ch"},
    ],

    "best_courses": [
        "Hospitality Management",
        "Banking & Finance",
        "International Relations",
        "Engineering",
        "Pharmaceutical Sciences"
    ],

    "scholarships": [
        "ETH Excellence Scholarship",
        "EPFL Excellence Fellowship",
        "Swiss Government Excellence Scholarship"
    ],

    "cost_of_living": "CHF 1,800 – 2,500 per month",
    "tuition_fees": "CHF 1,000 – 5,000 per year",

    "visa_requirements": [
        "Proof of Funds",
        "Health Insurance",
        "Offer Letter",
        "Motivation Letter",
        "Academic Records"
    ]
},

"it": {
    "name": "Italy",
    "flag": "https://flagcdn.com/w80/it.png",
    "description": "Italy combines rich culture with affordable education and some of Europe’s oldest universities.",

    "universities": [
        {"name": "University of Bologna", "website": "https://www.unibo.it"},
        {"name": "Sapienza University of Rome", "website": "https://www.uniroma1.it"},
        {"name": "University of Milan", "website": "https://www.unimi.it"},
        {"name": "Politecnico di Milano", "website": "https://www.polimi.it"},
    ],

    "best_courses": [
        "Fashion Designing",
        "Architecture",
        "Art & Culture",
        "Engineering",
        "Business Studies"
    ],

    "scholarships": [
        "DSU Scholarship",
        "Invest Your Talent in Italy",
        "Politecnico di Milano Merit Scholarship",
        "EDISU Piemonte Scholarship"
    ],

    "cost_of_living": "€700 to €1,200 per month",
    "tuition_fees": "€1,000 to €4,000 per year",

    "visa_requirements": [
        "Visa Application Form",
        "Financial Proof",
        "Accommodation Proof",
        "University Enrollment Letter",
        "Medical Insurance"
    ]
},


        # Add similar structure for remaining countries...
    }

    data = country_data.get(code.lower())
    if not data:
        data = {
            "name": "Not Found",
            "flag": "",
            "description": "Country details not available.",
            "universities": [],
            "best_courses": [],
            "scholarships": [],
            "cost_of_living": "",
            "tuition_fees": "",
            "visa_requirements": []
        }

    return render(request, "myapp/country.html", {"country": data})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please register first.")
            return redirect("login")
    return render(request, "myapp/login.html")

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("landing")

@login_required
def tests_page(request):
    return render(request, "myapp/tests.html")

@login_required
def notes_page(request):
    return render(request, "myapp/notes.html")

@login_required
def profile_page(request):
    user = request.user
    context = {
        "full_name": user.first_name,
        "username": user.username,
        "email": user.email,
        "date_joined": user.date_joined,
    }
    return render(request, "myapp/profile.html", context)

@login_required
def take_test(request, test_type):
    if request.method == "POST":
        score = int(request.POST.get("score", 0))  
        TestResult.objects.create(
            user=request.user,
            test_type=test_type,
            score=score
        )
        messages.success(request, f"{test_type.capitalize()} Test submitted! Your score: {score}")
        return redirect("tests")
    return render(request, "myapp/take_test.html", {"test_type": test_type})

# ========== THIS IS THE SINGLE, CORRECT VIEW FOR THE APPLY NOW FORM ==========
@login_required
def apply_now_view(request):
    if request.method == 'POST':
        # Create a new Application object and save it to the database
        Application.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            father_name=request.POST.get('father_name'),
            mobile=request.POST.get('mobile'),
            education=request.POST.get('education'),
            country=request.POST.get('country')
        )
        
        # Redirect to the existing success page
        return redirect('employee_success')

    # If GET request, just show the form page
    return render(request, 'myapp/applynow.html')

@login_required
def reading_test(request):
    return render(request, "myapp/reading.html")


@login_required
def writing_test(request):
    return render(request, "myapp/writing.html")
# ==============================================================================

#Writing_page,Listning_Page,Speaking_Page

def writing_notes(request):
    notes, created = WritingNotes.objects.get_or_create(user=request.user)

    if request.method == "POST":
        notes.text = request.POST.get("notes")
        notes.save()
        return redirect("writing_notes")

    return render(request, "myapp/writing_notes.html", {"notes": notes})

def listening_view(request):
    return render(request, "myapp/listening.html")   # uses your new listening UI

def speaking_view(request):
    return render(request, "myapp/speaking.html")    # uses your new speaking UI




def is_superstudent(user):
    try:
        return user.profile.role == "superstudent"
    except:
        return False