from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_job_seeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    company = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    password = models.CharField(max_length=50, default=0)
    other_information = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.full_name
    
class JobListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_qualifications = models.TextField()
    desired_qualifications = models.TextField()
    responsibilities = models.TextField()
    application_deadline = models.DateField()
    salary_range = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50)
    company_benefits = models.TextField()
    how_to_apply = models.TextField()
    other_information = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.title
        
class JobApplication(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='job_applications/', null=True, blank=True)
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Rejected', 'Rejected'),
        ('Shortlisted', 'Shortlisted'),
        ('Hired', 'Hired'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    

class AddJob(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_qualifications = models.TextField()
    desired_qualifications = models.TextField()
    responsibilities = models.TextField()
    application_deadline = models.DateField()
    salary_range = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50)
    company_benefits = models.TextField()
    how_to_apply = models.TextField()
    other_information = models.CharField(max_length=255, blank=True)
    