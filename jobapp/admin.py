from django.contrib import admin
from .models import UserProfile, JobListing, JobApplication

admin.site.register(UserProfile)
admin.site.register(JobListing)
admin.site.register(JobApplication)