from django.contrib import admin
from .models import UserProfile, JobListing, JobApplication, AddJob

admin.site.register(UserProfile)
admin.site.register(JobListing)
admin.site.register(JobApplication)
admin.site.register(AddJob)