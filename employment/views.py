from django.shortcuts import render, redirect
from .models import Profile, Job, Skill, LearnEarnOpportunity
import random
import http.client
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
import os
import json


xrapidapikey = os.getenv('x-rapidapi-key')

def personal_info(request):
    if request.method == 'POST':
        # Handle personal information submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        skills = request.POST.get('skills')
        experience = request.POST.get('linkedin_link')
        
        # Perform basic form validations
        if not name or not email:
            error_message = "Name and email are required fields."
            return render(request, 'personal_info.html', {'error_message': error_message})
        
        # Update or create the user's profile
        profile = Profile(name=name, email=email, phone_number=phone_number, skills=skills, experience=experience)

        profile.save()

        return redirect(request, 'salary_estimation')
    else:
        return render(request, 'personal_info.html')


def salary_estimation(request):
    # Retrieve the profile for the currently logged-in user
    profile = Profile.objects.filter(name=request.name).first()
    
    if profile:
        # Estimate salary range based on user's profile
        salary_range = estimate_salary_range()
        
        # Fetch LinkedIn profile data if a URL is provided
        linkedin_data = None
        if profile.experience:
            linkedin_data = fetch_linkedin_data(profile.experience)
        
        context = {
            'salary_range': salary_range,
            'linkedin_data': linkedin_data,
        }
        return render(request, 'find_jobs.html', context)
    else:
        # Redirect to the personal information form if no profile exists for the user
        return redirect('personal_info')


def estimate_salary_range():
    min_salary = random.randint(60000, 120000)
    max_salary = random.randint(min_salary, 160000)
    return f"{min_salary:,} - {max_salary:,}"



def work_now(request):
    # Retrieve on-demand remote jobs from the database
    jobs = Job.objects.filter(category='on-demand')
    return render(request, 'work_now.html', {'jobs': jobs})





def find_jobs(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', 'Digital')
        location = request.GET.get('location', 'Johannesburg')
        
        conn = http.client.HTTPSConnection("jobs-api14.p.rapidapi.com")
        
        headers = {
            'x-rapidapi-key': "040ba80d01msh9967db2271b9ddcp14f293jsncd7b2a5be4c9",
            'x-rapidapi-host': "jobs-api14.p.rapidapi.com"
        }
        
        conn.request("GET", str(f"/list?query={search_query}&location={location}&distance=10&language=en_GB&remoteOnly=false&datePosted=month&employmentTypes=fulltime%3Bparttime%3Bintern%3Bcontractor&index=0").strip().replace(' ', '_'), headers=headers)
        
        res = conn.getresponse()
        data = res.read()

        
        jobs_data = json.loads(data.decode("utf-8"))
        jobs = jobs_data['jobs']
        description_limit = 150
        for job in jobs:
            if len(job['description']) > description_limit:
                job['description'] = job['description'][:description_limit] + '...'
    
    return render(request, 'find_jobs.html', {'jobs': jobs, 'search_query': search_query, 'location': location})
        
        
def fetch_linkedin_data(url):
    conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "040ba80d01msh9967db2271b9ddcp14f293jsncd7b2a5be4c9",
        'x-rapidapi-host': "linkedin-data-api.p.rapidapi.com"
    }
    
    conn.request("GET", f"/get-profile-data-by-url?url={url}", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    return json.loads(data.decode("utf-8"))


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

def profile(request):
    # Retrieve the user's profile from the database
    profile = Profile.objects.get(name=request.name)
    
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