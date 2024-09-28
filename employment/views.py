from django.shortcuts import render, redirect
from .models import Profile, Job, Skill, LearnEarnOpportunity
from django.views.decorators.csrf import csrf_protect




@csrf_protect 
def personal_info(request):
    if request.method == 'POST':
        # Handle personal information submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        education = request.POST.get('education')
        
        # Create a new Profile instance and save it to the database
        profile = Profile(name=name, email=email, phone_number=phone_number, skills=skills, experience=experience, education=education)
        profile.save()
        
        return redirect('salary_estimation')
    else:
        return render(request, 'personal_info.html')
@csrf_protect 
def salary_estimation(request):
    # Retrieve user's profile from the database
    profile = Profile.objects.get(user=request.user)
    
    # Estimate salary range based on user's profile
    salary_range = estimate_salary_range(profile)
    
    return render(request, 'salary_estimation.html', {'salary_range': salary_range})

def estimate_salary_range(obj):
    print(obj)
    return 10000

@csrf_protect 
def work_now(request):
    # Retrieve on-demand remote jobs from the database
    jobs = Job.objects.filter(category='on-demand')
    return render(request, 'work_now.html', {'jobs': jobs})

@csrf_protect 
def find_jobs(request):
    if request.method == 'POST':
        # Retrieve search and filter criteria from the form
        title = request.POST.get('title')
        skills = request.POST.get('skills')
        experience_level = request.POST.get('experience_level')
        
        # Retrieve job listings from the database based on search and filter criteria
        jobs = Job.objects.filter(title__icontains=title, skills_required__icontains=skills, experience_required=experience_level)
    else:
        jobs = Job.objects.all()
    
    skills = Skill.objects.all().values_list('name', flat=True).distinct()
    experience_levels = Job.objects.values_list('experience_required', flat=True).distinct()
    
    return render(request, 'find_jobs.html', {'jobs': jobs, 'skills': skills, 'experience_levels': experience_levels})
@csrf_protect 
def job_details(request, job_id):
    # Retrieve the job details from the database based on the job_id
    job = Job.objects.get(id=job_id)
    
    # Retrieve user's profile from the database
    profile = Profile.objects.get(user=request.user)
    
    # Check if the user's profile matches the job requirements
    is_matched = check_job_match(profile, job)
    
    # Retrieve recommended skills for the job
    recommended_skills = get_recommended_skills(job)
    
    return render(request, 'job_details.html', {'job': job, 'is_matched': is_matched, 'recommended_skills': recommended_skills})
@csrf_protect 
def profile(request):
    # Retrieve the user's profile from the database
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Handle profile updates
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        education = request.POST.get('education')
        
        # Update the profile fields
        profile.name = name
        profile.email = email
        profile.phone_number = phone_number
        profile.skills = skills
        profile.experience = experience
        profile.education = education
        profile.save()
        
        return redirect('profile')
    else:
        return render(request, 'profile.html', {'profile': profile})
@csrf_protect 
def enhance_resume(request):
    # Retrieve the user's profile from the database
    profile = Profile.objects.get(user=request.user)
    
    # Retrieve the target job title from the form
    target_job_title = request.POST.get('target_job_title')
    
    # Generate an improved resume based on the user's profile and target job title
    enhanced_resume = generate_enhanced_resume(profile, target_job_title)
    
    # Provide the enhanced resume for download
    # Implement the logic to generate and serve the enhanced resume file
    
    return redirect('profile')
@csrf_protect 
def upskill(request):
    # Retrieve skills and learning opportunities from the database
    skill_categories = {}
    skills = Skill.objects.all()
    for skill in skills:
        if skill.category not in skill_categories:
            skill_categories[skill.category] = []
        skill_categories[skill.category].append(skill)
    
    learn_earn_opportunities = LearnEarnOpportunity.objects.all()
    
    return render(request, 'upskill.html', {'skill_categories': skill_categories, 'learn_earn_opportunities': learn_earn_opportunities})