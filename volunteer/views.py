from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VolunteerForm
from .models import Volunteer # Though not directly used in this version of views, good to have for future model interactions

def volunteer_signup_view(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            if request.user.is_authenticated:
                volunteer.user = request.user
            volunteer.save()
            messages.success(request, "Thank you for signing up to volunteer! We appreciate your commitment and will be in touch soon regarding available opportunities.")
            return redirect('volunteer_thank_you') # Ensure this URL name is defined in urls.py
        else:
            messages.error(request, "Please correct the errors below.")
    else: # GET request
        if request.user.is_authenticated and request.user.first_name and request.user.last_name:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                # Email and phone are not standard User model fields, so not pre-filled from request.user directly
            }
            form = VolunteerForm(initial=initial_data)
        else:
            form = VolunteerForm()
            
    return render(request, 'volunteer/volunteer_signup.html', {'form': form})

def volunteer_thank_you_view(request):
    return render(request, 'volunteer/volunteer_thank_you.html')
