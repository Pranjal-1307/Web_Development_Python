from django.urls import path
from models import views

urlpatterns = [

    # Public Pages
    path('', views.home, name="home"),
    path('landing/', views.landing, name="landing"),
    path('about/', views.about_page, name="about"),
    path('features/', views.feature_page, name="features"),
    path('contact/', views.contact_page, name="contact"),

    # Auth
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_employee, name="register_employee"),

    # Country Page
    path('country/<str:code>/', views.country_detail, name="country_detail"),

    # User Pages
    path('tests/', views.tests_page, name="tests"),
    path('notes/', views.notes_page, name="notes"),
    path('profile/', views.profile_page, name="profile"),
    path('take-test/<str:test_type>/', views.take_test, name="take_test"),

    # Apply
    path('apply-now/', views.apply_now_view, name="apply_now"),
    path('success/', views.success_page, name="employee_success"),

    # IELTS Tests
    path('reading/', views.reading_test, name="reading_test"),
    path('writing/', views.writing_test, name="writing_test"),
]
