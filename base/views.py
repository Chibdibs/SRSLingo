from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from SRSLingo.settings import FIREBASE_CONFIG
from base.forms import UserRegisterForm


@login_required
def home(request):
    return render(request, 'home.html')


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')  # Assumes you have a named URL 'home' for your homepage
    return render(request, 'landing.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already has an account.')
                return render(request, 'registration/register.html', {'form': form, 'email_exists': True})
            else:
                form.save()
                return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def my_view(request):
    context = {'firebase_config': FIREBASE_CONFIG,
               }
    return render(request, 'base.html', context)
