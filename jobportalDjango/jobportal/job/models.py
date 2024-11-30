from django.db import models
from django.contrib.auth.models import User
from django.forms import forms


# Create your models here.
class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=1, null=True)
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.user.username


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10, null=True)
    company = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=15, null=True)
    status = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=100)
    salary = models.FloatField(max_length=20)
    image = models.FileField()
    description = models.CharField(max_length=300)
    experience = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    creationdate = models.DateField()
    shortlisted_candidates = models.ManyToManyField('Application', related_name='shortlisted_jobs', blank=True)

    def __str__(self):
        return f"{self.title} - {self.location}"


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    experience_level = models.CharField(max_length=50)
    cover_letter = models.FileField(upload_to='cover_letter/')
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)

class RecruiterFeedback(models.Model):
    company = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback from {self.company}"



class JobSeekerFeedback(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback from {self.full_name}"