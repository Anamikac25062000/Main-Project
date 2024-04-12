from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, JobListing, JobApplication, AddJob

class UserRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30, required=True)
    user_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True) 
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=(('job_seeker', 'Job Seeker'), ('employer', 'Employer/Recruiter')), widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ['full_name', 'user_name', 'email', 'password', 'confirm_password', 'user_type']

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["user_name"] 
        user.email = self.cleaned_data["email"]
        user.full_name = self.cleaned_data["full_name"] 
        if commit:
            user.save()
            if self.cleaned_data['user_type'] == 'job_seeker':
                UserProfile.objects.create(user=user, full_name=user.username, is_job_seeker=True)
            elif self.cleaned_data['user_type'] == 'employer':
                UserProfile.objects.create(user=user, full_name=user.username, is_employer=True)
        return user

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['resume']

# class JobListingForm(forms.ModelForm):
#     class Meta:
#         model = JobListing
#         fields = [
#             'title',
#             'description',
#             'required_qualifications',
#             'desired_qualifications',
#             'responsibilities',
#             'application_deadline',
#             'salary_range',
#             'location',
#             'employment_type',
#             'company_benefits',
#             'how_to_apply',
#             'other_information',
#         ]

class JobApplicationForm(forms.ModelForm):
    resume = forms.FileField()
    cover_letter = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'full_name', 'resume', 'other_information']

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'full_name','company', 'other_information']

class AddJobForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = [
            'title',
            'description',
            'required_qualifications',
            'desired_qualifications',
            'responsibilities',
            'application_deadline',
            'salary_range',
            'location',
            'employment_type',
            'company_benefits',
            'how_to_apply',
            'other_information',
        ]
