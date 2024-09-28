from .models import CustomUser
from django import forms

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect 
def register_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        
        # Check if the phone number is already registered
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number already registered.')
        else:
            # Create a new user
            user = CustomUser.objects.create_user(phone_number=phone_number, password=password)
            login(request, user)  # Log the user in after registration
            return redirect('personal_info')  # Redirect to a home page or dashboard
    return render(request, 'register.html')


@csrf_protect 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('personal_info')  # Redirect to a success page
        else:
            form.add_error(None, 'Invalid phone number or password')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')
