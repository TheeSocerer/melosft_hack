from django.urls import path
from . import views

urlpatterns = [
    path('', views.personal_info, name='personal_info'),
    path('salary-estimation/', views.salary_estimation, name='salary_estimation'),
    path('work-now/', views.work_now, name='work_now'),
    path('find-jobs/', views.find_jobs, name='find_jobs'),
    path('job-details/<int:job_id>/', views.job_details, name='job_details'),
    path('profile/', views.profile, name='profile'),
    path('enhance-resume/', views.enhance_resume, name='enhance_resume'),
    path('upskill/', views.upskill, name='upskill'),
]