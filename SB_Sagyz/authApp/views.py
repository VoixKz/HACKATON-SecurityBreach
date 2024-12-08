from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'authApp/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authApp/register.html', {'form': form})

def login_view(request):
    form = CustomUserLoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'authApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')