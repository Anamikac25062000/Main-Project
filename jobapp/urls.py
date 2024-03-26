from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('job_seeker_profile/', views.job_seeker_profile, name='job_seeker_profile'),
    path('update_job_seeker_profile/', views.update_job_seeker_profile, name='update_job_seeker_profile'),
    path('profile/', views.profile, name='profile'),
    path('all_jobs/', views.all_jobs, name='all_jobs'),
    path('job_search/', views.search_jobs, name='job_search'),
    path('apply_for_job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('job_listing/', views.job_listing, name='job_listing'),
    path('applied_job/<int:job_id>/', views.applied_job, name='applied_job'),
    path('application_status/', views.application_status, name='application_status'),
    
    path('view_applied_jobs/', views.view_applied_jobs, name='view_applied_jobs'),
    path('delete_application/<int:application_id>/', views.delete_application, name='delete_application'),
    path('employer_profile/', views.employer_profile, name='employer_profile'),
    path('update_employer_profile/', views.update_employer_profile, name='update_employer_profile'),
    path('add_jobs/', views.add_jobs, name='add_jobs'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('view_jobs/', views.view_jobs, name='view_jobs'),
    path('view_applications/', views.view_all_applications, name='view_applications'),
    path('view_job_seeker_applications/', views.view_job_seeker_applications, name='view_job_seeker_applications'),
]
