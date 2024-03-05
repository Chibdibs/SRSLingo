import firebase_admin
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from firebase_admin import auth, credentials

from SRSLingo.settings import FIREBASE_CONFIG
from base.forms import UserRegisterForm
# from models import CustomUser as User
from django.contrib.auth import login

# Initialize Firebase Admin
cred = credentials.Certificate("srslingo-firebase-adminsdk-i3v0c-109f95bbf5.json")
firebase_admin.initialize_app(cred)


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


@csrf_exempt
@require_POST
def verify_token(request):
    id_token = request.POST.get('token')
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')
        email = decoded_token.get('email')

        User = get_user_model()
        user, created = User.objects.get_or_create(username=uid, defaults={'email': email})

        # Optionally set user details here
        if created:
            user.email = email  # Example: set email on user object if newly created
            user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return JsonResponse({'message': 'User logged in successfully'})

    except ValueError:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def home(request):
    return render(request, 'home.html')


@login_required()
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')  # Assumes you have a named URL 'home' for your homepage
    return render(request, 'landing.html')
