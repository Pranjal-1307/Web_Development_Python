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

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # ✅ Added password field

    def __str__(self):
        return f"{self.name} ({self.department})"
