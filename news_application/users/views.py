from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    """
    Handle new user registration with custom user creation.
    
    Processes registration forms using the CustomUserCreationForm,
    validates user input, creates new user accounts, and provides
    success feedback before redirecting to the login page.
    
    Args:
        request: HTTP request object containing registration form data
        
    Returns:
        HttpResponse: Registration form template or redirect to login page
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})