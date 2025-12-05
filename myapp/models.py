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
    role = models.CharField(
        max_length=20,
        choices=[('student', 'Student'), ('superstudent', 'Super Student')],
        default='student'
    )

    def __str__(self):
        return f"{self.user.username} Profile"

class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # ✅ Added password field

    class Meta:
        verbose_name = "User"
        verbose_name_plural="Users"

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
    

class WritingNotes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Writing Notes"


############################################################################################################################33
class ReadingPassage(models.Model):
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    passage_text = models.TextField()

    def __str__(self):
        return self.title


class ReadingQuestion(models.Model):
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Q: {self.question_text[:40]}"


class WritingTask1(models.Model):
    title = models.CharField(max_length=255)
    prompt = models.TextField()

    def __str__(self):
        return self.title


class WritingTask2(models.Model):
    topic = models.CharField(max_length=255)
    question = models.TextField()

    def __str__(self):
        return self.topic


################################################################################################
class ListeningAudio(models.Model):
    """
    Represents an audio file (point to static path or store in FileField).
    We'll reference static file names like static/audio/CGtoIELTS_01.mp3
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    filename = models.CharField(max_length=255, help_text="Relative static path, e.g. audio/CGtoIELTS_01.mp3")
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)

    def audio_url(self):
        # templates can use: {{ audio.audio_url }}
        return f"{self.filename}"

    def __str__(self):
        return self.title


class ListeningQuestion(models.Model):
    """
    Questions tied to a ListeningAudio instance.
    type: 'mcq' or 'fill' or 'short' (we accept text-based answers).
    For mcq: store options in the options JSON field (list of strings) and the answer key index.
    """
    QTYPE_CHOICES = (
        ('mcq', 'Multiple choice'),
        ('fill', 'Fill in the blank'),
        ('short', 'Short answer'),
    )
    audio = models.ForeignKey(ListeningAudio, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    qtype = models.CharField(max_length=10, choices=QTYPE_CHOICES, default='short')
    # For mcq: options stored as a JSON string; for simplicity use newline-separated options
    options = models.TextField(blank=True, help_text="For MCQ: newline separated options")
    correct_answer = models.CharField(max_length=512, help_text="For mcq store the exact option text. For fill/short store canonical answer (lowercase).")

    points = models.PositiveSmallIntegerField(default=1)

    def get_options_list(self):
        return [o.strip() for o in self.options.splitlines() if o.strip()]

    def __str__(self):
        return f"[{self.audio}] {self.text[:60]}"


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # FIX: Only save profile if it exists
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


class ReadingSkill(models.Model):
        title = models.CharField(max_length=200)
        description = models.TextField()
        updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
        return self.title


class VocabularyWord(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=255)
    example = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word


class ReadingPDF(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to="reading_pdfs/")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


