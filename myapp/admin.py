from django.contrib import admin
# Register your models here.
from .models import Employee,TestResult , Application ,Notes,Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    search_fields = ("user__username", "role")
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "updated_at")
    search_fields = ("title", "content", "user__username")
# Register the Employee model to make it visible in the admin panel
@admin.register(Employee) # CHANGE: Added a simple registration for the Employee model
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department')
    search_fields = ('name', 'email')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_type', 'score', 'date_taken')
    list_filter = ('test_type', 'date_taken')
    search_fields = ('user__username', 'test_type')


# Define a custom admin class for the Application model
class ApplicationAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('name', 'user', 'country', 'education', 'created_at')
    
    # Fields to add to the filter sidebar
    list_filter = ('country', 'education')
    
    # Fields to include in the search bar
    search_fields = ('name', 'father_name', 'user__username')
    
    # Make the admin view read-only (optional, but safer)
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

# Register the Application model with its custom admin class
admin.site.register(Application, ApplicationAdmin)

from .models import ReadingSkill, VocabularyWord, ReadingPDF

admin.site.register(ReadingSkill)
admin.site.register(VocabularyWord)
admin.site.register(ReadingPDF)




