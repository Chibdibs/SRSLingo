import json
import firebase_admin
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from firebase_admin import auth, credentials

from SRSLingo.settings import FIREBASE_CONFIG
from base.forms import UserRegisterForm
from django.contrib.auth import login
# from models import CustomUser as User


# Initialize Firebase Admin
cred = credentials.Certificate("srslingo-firebase-adminsdk-i3v0c-109f95bbf5.json")
firebase_admin.initialize_app(cred)


@login_required
def home(request):
    return render(request, 'home.html')


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')


def my_view(request):
    context = {'firebase_config': FIREBASE_CONFIG,
               }
    return render(request, 'base.html', context)


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


@csrf_exempt
@require_POST
def verify_token(request):
    # Parse the request body to JSON
    data = json.loads(request.body)
    id_token = data.get('token')

    try:
        # Verify the ID token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')
        email = decoded_token.get('email')

        # Use Django's get_user_model to reference the active user model
        user_model = get_user_model()
        # Get or create a user in your Django auth model
        user, created = user_model.objects.get_or_create(username=uid, defaults={'email': email})

        # If the user was created, you may want to set additional fields
        if created:
            user.email = email
            # Set other fields if necessary, like user.first_name, user.last_name, etc.
            user.save()

        # Use Django's built-in backend for authentication
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Return a successful login response
        return JsonResponse({'message': 'User logged in successfully'}, status=200)

    except ValueError:
        # Handle the case where the token is invalid
        return JsonResponse({'error': 'Invalid token'}, status=400)
    except Exception as e:
        # Catch any other exceptions and return an error
        return JsonResponse({'error': str(e)}, status=500)


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect authenticated users to the home page
        return super().get(request, *args, **kwargs)
