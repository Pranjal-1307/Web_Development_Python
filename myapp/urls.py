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
    # ADD THIS NEW URL PATTERN
    path('applynow/', views.apply_now_view, name='apply_now'),
    path("reading/", views.reading_test, name="reading"),
    # ... existing paths ...
    path("writing/", views.writing_test, name="writing"),
    #Writing_notes
    path("notes/writing/", views.writing_notes, name="writing_notes"),
    # FIXED ORDER — specific paths first
    path("tests/listening/", views.listening_view, name="listening"),
    path("tests/speaking/", views.speaking_view, name="speaking"),
    # generic test route LAST
    path("tests/<str:test_type>/", views.take_test, name="take_test"),
    path("submit/<str:test_type>/", views.save_test_score, name="save_test_score"),


    #Notes
    # NOTES CRUD
    path("notes/list/", views.notes_list, name="notes_list"),
    path("notes/create/", views.notes_create, name="notes_create"),
    path("notes/edit/<int:id>/", views.notes_edit, name="notes_edit"),
    path("notes/delete/<int:id>/", views.notes_delete, name="notes_delete"),

    
    # Reading Skills CRUD
    path("content-admin/skills/", views.skills_list, name="skills_list"),
    path("content-admin/skills/create/", views.skills_create, name="skills_create"),
    path("content-admin/skills/edit/<int:id>/", views.skills_edit, name="skills_edit"),
    path("content-admin/skills/delete/<int:id>/", views.skills_delete, name="skills_delete"),

    # Vocabulary CRUD
    path("content-admin/vocab/", views.vocab_list, name="vocab_list"),
    path("content-admin/vocab/create/", views.vocab_create, name="vocab_create"),
    path("content-admin/vocab/edit/<int:id>/", views.vocab_edit, name="vocab_edit"),
    path("content-admin/vocab/delete/<int:id>/", views.vocab_delete, name="vocab_delete"),

    # Reading PDF CRUD
    path("content-admin/pdf/", views.pdf_list, name="pdf_list"),
    path("content-admin/pdf/create/", views.pdf_create, name="pdf_create"),
    path("content-admin/pdf/edit/<int:id>/", views.pdf_edit, name="pdf_edit"),
    path("content-admin/pdf/delete/<int:id>/", views.pdf_delete, name="pdf_delete"),

]