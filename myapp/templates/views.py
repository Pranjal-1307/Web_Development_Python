from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from models import Employee, TestResult, Application
from django.contrib.auth.decorators import login_required

# ========== PUBLIC PAGES ==========

def landing(request):
    return render(request, 'myapp/landing.html')

def home(request):
    return render(request, 'myapp/home.html')

def about_page(request):
    return render(request, 'myapp/about.html')

def feature_page(request):
    return render(request, 'myapp/features.html')

def contact_page(request):
    return render(request, 'myapp/contact.html')


# ========== USER AUTH ==========

def register_employee(request):
    if request.method == 'POST':
        fullname = request.POST.get('name')
        username = request.POST.get('department')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('landing')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('landing')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('landing')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = fullname
        user.save()

        Employee.objects.create(
            name=fullname,
            department=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful! Login now.")
        return redirect('login')

    return redirect('home')


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
            messages.error(request, "Invalid username or password!")
            return redirect("login")
    return render(request, "myapp/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("landing")


# ========== COUNTRY DETAILS ==========

def country_detail(request, code):

    country_data = {
        "us": {
            "name": "United States",
            "flag": "https://flagcdn.com/w80/us.png",
            "description": "The USA offers flexible education and top research universities.",
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
                "Knight-Hennessy Scholarship",
                "Harvard Aid Program",
                "AAUW Scholarship"
            ],
            "cost_of_living": "$1,000 – $1,800 per month",
            "tuition_fees": "$20,000 – $55,000 per year",
            "visa_requirements": [
                "I-20 Form",
                "SEVIS Fee",
                "Financial Proof",
                "Passport",
                "Academic Transcripts"
            ]
        },

        # ------------ Add all your other countries here (Germany, France, UAE, Italy, etc.) ------------
        # NOTE: Your full country_data from previous message goes here exactly as it is.

    }

    data = country_data.get(code.lower(), {
        "name": "Not Found",
        "flag": "",
        "description": "Country details not available.",
        "universities": [],
        "best_courses": [],
        "scholarships": [],
        "cost_of_living": "",
        "tuition_fees": "",
        "visa_requirements": []
    })

    return render(request, "myapp/country.html", {"country": data})


# ========== USER PROTECTED PAGES ==========

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
        messages.success(request, f"{test_type.upper()} Test submitted! Score: {score}")
        return redirect("tests")
    return render(request, "myapp/take_test.html", {"test_type": test_type})


@login_required
def apply_now_view(request):
    if request.method == 'POST':
        Application.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            father_name=request.POST.get('father_name'),
            mobile=request.POST.get('mobile'),
            education=request.POST.get('education'),
            country=request.POST.get('country')
        )
        return redirect('employee_success')

    return render(request, 'myapp/applynow.html')


def success_page(request):
    return render(request, 'myapp/success.html')


@login_required
def reading_test(request):
    return render(request, "myapp/reading.html")

@login_required
def writing_test(request):
    return render(request, "myapp/writing.html")
