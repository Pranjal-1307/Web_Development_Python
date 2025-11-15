from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path("login/", views.login_user, name="login"),  
    path("logout/", views.logout_user, name="logout"), 
    path('register/', views.register_employee, name='employee_register'),
    path('success/', views.success_page, name='employee_success'),
    path('about/', views.about_page, name='employee_about'), 
    path('features/', views.feature_page, name='employee_feature'),  
    path('contact/', views.contact_page, name='employee_contact'),
    path("country/<str:code>/", views.country_detail, name="country_detail"), 
    path("tests/", views.tests_page, name="tests"),
    path("notes/", views.notes_page, name="notes"),
    path("profile/", views.profile_page, name="profile"),
    path("tests/<str:test_type>/", views.take_test, name="take_test"),
    
    # ADD THIS NEW URL PATTERN
    path('applynow/', views.apply_now_view, name='apply_now'),
    path("reading/", views.reading_test, name="reading"),
    # ... existing paths ...
    path("writing/", views.writing_test, name="writing"),

]