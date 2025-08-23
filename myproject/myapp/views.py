'''NO DATA RETRIVE JUST SHOW
from django.shortcuts import redirect, render


# Create your views here.
from django.http import HttpResponse
def home(request):
     return render(request, 'myapp/home.html')
def register_employee(request):
    # Just display the form page (basic)
    if request.method == 'POST':
        # handle form submission here if you have a form
        return redirect('employee_success')
    return render(request, 'myapp/register.html')
def success_page(request):
    return render(request, 'myapp/success.html')
    '''

'''DATA RETRIVE DATA STORED '''
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Employee


# Landing Page
def landing(request):
    return render(request, 'myapp/landing.html')


# Home Page
def home(request):
    return render(request, 'myapp/home.html')


# Register from landing page
def register_employee(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
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
            login(request, user)   # login user
            messages.success(request, "Logged in successfully!")
            return redirect("home")   # ✅ redirect to home
        else:
            messages.error(request, "Invalid username or password. Please register first.")
            return redirect("login")  # reload login page

    return render(request, "myapp/login.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "⚠ User not registered. Please register first.")
            return redirect("login")

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("landing")


'''
from django.shortcuts import redirect, render
from .models import Employee

def home(request):
    return render(request, 'myapp/home.html')

def register_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        department = request.POST.get('department')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Optional: check if passwords match
        if password1 != password2:
            return render(request, 'myapp/register.html', {
                'error': "Passwords do not match!"
            })

        # Save employee in database
        Employee.objects.create(
            name=name,
            department=department,
            email=email,
            password1=password1,
            password2=password2
        )

        return redirect('employee_success')

    return render(request, 'myapp/register.html')

def success_page(request):
    return render(request, 'myapp/success.html')
'''