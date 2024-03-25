from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

    path('update_job_seeker_profile/', views.update_job_seeker_profile, name='update_job_seeker_profile'),
    path('job_search/', views.search_jobs, name='job_search'),
    path('job_listings/', views.add_jobs, name='job_listings'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('application_status/', views.application_status, name='application_status'),
    path('view_applied_jobs/', views.view_applied_jobs, name='view_applied_jobs'),
    path('delete_application/<int:application_id>/', views.delete_application, name='delete_application')

    path('update_employer_profile/', views.update_employer_profile, name='update_employer_profile'),
    path('post_new_job/', views.add_jobs, name='post_new_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('view_applications/', views.view_applications, name='view_applications'),

    path('manage_users/', views.manage_users, name='manage_users'),
    path('view_jobs/', views.view_jobs, name='view_jobs'),
    path('view_applications/', views.view_applications, name='view_applications'),
]
