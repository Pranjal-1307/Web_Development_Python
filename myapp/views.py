'''DATA RETRIVE DATA STORED '''
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Employee, TestResult, Application
from django.contrib.auth.decorators import login_required

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
            "description": "Study in the UK with globally recognized universities and IELTS-friendly admission processes.",
            "universities": ["University of Oxford", "University of Cambridge", "Imperial College London"],
        },
        "us": {
            "name": "United States",
            "flag": "https://flagcdn.com/w80/us.png",
            "description": "The USA offers world-class education, research opportunities, and diverse culture.",
            "universities": ["Harvard University", "MIT", "Stanford University"],
        },
        "ca": {
            "name": "Canada",
            "flag": "https://flagcdn.com/w80/ca.png",
            "description": "Canada is known for affordable education, safety, and post-study work opportunities.",
            "universities": ["University of Toronto", "McGill University", "University of British Columbia"],
        },
        "au": {
            "name": "Australia",
            "flag": "https://flagcdn.com/w80/au.png",
            "description": "Australia provides high-quality education, vibrant lifestyle, and scholarships for international students.",
            "universities": ["University of Melbourne", "Australian National University", "University of Sydney"],
        },
        "in": {
            "name": "India",
            "flag": "https://flagcdn.com/w80/in.png",
            "description": "India offers a growing number of English-taught programs and affordable education options.",
            "universities": ["IITs", "Delhi University", "IIMs"],
        },
    }
    data = country_data.get(code.lower())
    if not data:
        data = {"name": "Not Found", "flag": "", "description": "Country details not available.", "universities": []}
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