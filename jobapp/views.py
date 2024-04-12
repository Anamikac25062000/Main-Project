from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, JobApplicationForm, ResumeUploadForm, UserProfileForm, AddJobForm, EmployerProfileForm, JobListing
from .models import UserProfile, JobListing, JobApplication, Notification
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    user_profile = request.user.userprofile
    if user_profile.is_job_seeker:
        return render(request, 'job_seeker_profile.html', {'user_profile': user_profile})
    elif user_profile.is_employer:
        return render(request, 'employer_profile.html', {'user_profile': user_profile})
    elif request.user.is_staff:
        return render(request, 'admin_profile.html', {'user_profile': user_profile})
    else:
        pass

@login_required
def job_seeker_profile(request):
    user_profile = request.user.userprofile
    job_applications = JobApplication.objects.filter(applicant=request.user)
    applied_job_ids = [application.job.id for application in job_applications]
    return render(request, 'job_seeker_profile.html', {'user_profile': user_profile, 'applied_job_ids': applied_job_ids})

# def upload_resume(request):
#     if request.method == 'POST':
#         # Assuming the form field for the resume is named 'resume'
#         resume_file = request.FILES.get('resume')
#         if resume_file:
#             # Get the user's profile
#             user_profile = request.user.userprofile
#             # Save the uploaded resume to the user's profile
#             user_profile.resume = resume_file
#             user_profile.save()
#             return redirect('job_seeker_profile')  # Redirect to the profile page after successful upload
#     return render(request, 'upload_resume.html')  # Render the upload resume template if not a POST request

@login_required
def update_job_seeker_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def all_jobs(request):
    # Get all job listings
    job_listings = JobListing.objects.all()
    
    return render(request, 'all_jobs.html', {'job_listings': job_listings})

# @login_required
# def apply_for_job(request, job_id):
#     job = get_object_or_404(JobListing, pk=job_id)
#     # applicant = get_object_or_404(JobApplication, pk=)
#     if request.method == 'POST':
#         form = JobApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.job = job
#             application.applicant = request.user
#             application.created_by = job.created_by
#             application.save()
#             # if request.user.userprofile.is_employer==True:
#             applicant_email = request.user.email
#             employer_email = job.created_by.email
#             print("Employer Email:", employer_email)
#             print(applicant_email)
#             # else:
#                 # print('error')
#             # notification_content = f"New application received for job: {job.title}"
#             # create_notification(employer, notification_content)
#             return redirect('all_jobs') 
#     else:
#         form = JobApplicationForm()
#     return render(request, 'apply_job.html', {'form': form, 'job': job})
    
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobListing, pk=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            
            # Set the created_by field of the JobApplication to the creator of the JobListing
            
            application.save()
            
            # Get applicant's email
            applicant_email = request.user.email
            applicant_subject = f"Application for {job.title}"
            applicant_message = f'You have successfull applied for the {job.title}.'
            send_mail(applicant_subject, applicant_message, settings.EMAIL_HOST_USER, [applicant_email])
            
            employer_email = job.employer.email
            employer_subject = f"Application for {job.title}"
            employer_message = f'{request.user.username} applied for the {job.title}.'
            send_mail(employer_subject, employer_message, settings.EMAIL_HOST_USER, [employer_email])


            
            return redirect('all_jobs')
    else:
        form = JobApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})

@login_required
def search_jobs(request):
    keyword = request.GET.get('keyword', '')
    location = request.GET.get('location', '')
    industry = request.GET.get('industry', '')

    job_listings = JobListing.objects.filter(title__icontains=keyword, location__icontains=location, industry__icontains=industry)
    
    if job_listings:
        return render(request, 'search_results.html', {'job_listings': job_listings})
    else:
        return render(request, 'no_results.html')
    
@login_required
def applied_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    
    # Check if the user has already submitted an application for this job
    existing_application = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            if existing_application:
                messages.error(request, 'You have already submitted an application for this job.')
            else:
                application = form.save(commit=False)
                application.job = job
                application.applicant = request.user
                application.save()
                messages.success(request, 'Application submitted successfully!')
                return redirect('home')
    else:
        form = JobApplicationForm()
    return render(request, 'applied_job.html', {'form': form, 'job': job})
    
@login_required
def view_applied_jobs(request):
    user = request.user
    job_applications = JobApplication.objects.filter(applicant=user)
    return render(request, 'view_applied_jobs.html', {'job_applications': job_applications})

@login_required
def application_status(request):
    job_applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'application_status.html', {'job_applications': job_applications})

@login_required
def employer_profile(request):
    user_profile = request.user.userprofile
    return render(request, 'employer_profile.html', {'user_profile': user_profile})

@login_required
def update_employer_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            print(user_profile.company)
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = EmployerProfileForm(instance=user_profile)
    return render(request, 'update_employer_profile.html', {'form': form})

# @login_required
# def add_jobs(request):
#     if request.method == 'POST':
#         form = AddJobForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.employer = request.user
#             job.save()
#             messages.success(request, 'Job created successfully!')
#             return redirect('job_listing') 
#     else:
#         form = AddJobForm()
#     return render(request, 'add_job.html', {'form': form})

# def job_listing(request):
#     # Fetch all job listings
#     job_listings = JobListing.objects.all()
    
#     return render(request, 'job_listing.html', {'job_listings': job_listings})

@login_required
def add_jobs(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            # Assign the current user to the employer field
            job.employer = request.user
            job.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_listing') 
    else:
        form = AddJobForm()
    return render(request, 'add_job.html', {'form': form})

def job_listing(request):
    job_listings = JobListing.objects.all()
    return render(request, 'job_listing.html', {'job_listings': job_listings})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id, employer=request.user)
    if request.method == 'POST':
        form = AddJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('profile')
    else:
        form = AddJobForm(instance=job)
    return render(request, 'edit_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('profile')
    return render(request, 'delete_job.html', {'job': job})

def view_job_seeker_applications(request):
    # Retrieve all job applications
    job_applications = JobApplication.objects.all()
    
    return render(request, 'view_applications.html', {'job_applications': job_applications})

@login_required
def admin_profile(request):
    user_profile = request.user.userprofile
    return render(request, 'admin_profile.html', {'user_profile': user_profile})

@login_required
def manage_users(request):
    job_seekers = User.objects.filter(userprofile__is_job_seeker=True)
    employers = User.objects.filter(userprofile__is_employer=True)
    return render(request, 'manage_users.html', {'job_seekers': job_seekers, 'employers': employers})

@login_required
def view_jobs(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_listing') 
    else:
        form = JobListingForm()
    return render(request, 'job_listing.html', {'form': form})

@login_required
def view_all_applications(request):
    job_applications = JobApplication.objects.all()
    return render(request, 'view_applications.html', {'job_applications': job_applications})
    
@login_required
def delete_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if application.applicant == request.user:
        application.delete()
        messages.success(request, 'Application deleted successfully!')
    return redirect('view_applied_jobs')

def create_notification(recipient, content):
    Notification.objects.create(recipient=recipient, content=content)