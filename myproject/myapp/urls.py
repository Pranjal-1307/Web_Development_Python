from django.urls import path
from . import views

urlpatterns = [
path('', views.landing, name='landing'), # This will route the URL to the 'landing' view
path('home/', views.home, name='home'),
path("login/", views.login_user, name="login"),   # 👈 new
path("logout/", views.logout_user, name="logout"), # 👈 new
path('register/', views.register_employee, name='employee_register'),
path('success/', views.success_page, name='employee_success'),
path('about/', views.about_page, name='employee_about'), 
path('features/', views.feature_page, name='employee_feature'),  
path('contact/', views.contact_page, name='employee_contact'),
path("country/<str:code>/", views.country_detail, name="country_detail"), 
]

