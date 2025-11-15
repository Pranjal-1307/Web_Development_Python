'''
from django.db import models
class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.name} ({self.department})"
# Create your models here.
'''
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics/", default="default.png")

    def __str__(self):
        return f"{self.user.username} Profile"

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # ✅ Added password field

    def __str__(self):
        return f"{self.name} ({self.department})"



class TestResult(models.Model):
    TEST_CHOICES = [
        ('listening', 'Listening'),
        ('reading', 'Reading'),
        ('writing', 'Writing'),
        ('speaking', 'Speaking'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=20, choices=TEST_CHOICES)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test_type} ({self.score})"
    

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    education = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - Applied for {self.country}'