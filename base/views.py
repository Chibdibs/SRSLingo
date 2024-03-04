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
from models import CustomUser as User
from django.contrib.auth import login

# Initialize Firebase Admin
cred = credentials.Certificate('path/to/your/firebase-adminsdk.json')
default_app = firebase_admin.initialize_app(cred)

# Inside your verify_token view
user, created = User.objects.get_or_create(firebase_uid=uid,
                                           defaults={'email': decoded_token.get('email'), 'username': uid})
# Log the user in
login(request, user, backend='django.contrib.auth.backends.ModelBackend')


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


def verify_token(request):
    id_token = request.POST.get("idToken")
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        # Create session, login user, or whatever you need
        return HttpResponse("User authenticated; UID: " + uid)
    except ValueError:
        # Handle error: invalid token
        return HttpResponse("Authentication failed.", status=401)


@csrf_exempt
@require_POST
def verify_token(request):
    data = json.loads(request.body)
    id_token = data.get('token')

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Optionally, check if the user already exists in your database
        User = get_user_model()
        user, created = User.objects.get_or_create(username=uid, defaults={'email': decoded_token.get('email')})

        # Log the user in
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend to avoid errors
        login(request, user)

        return JsonResponse({'message': 'User logged in successfully'})
    except ValueError:
        # Token is invalid
        return JsonResponse({'error': 'The provided token is invalid'}, status=400)
    except firebase_admin.auth.AuthError as e:
        # Handle AuthError
        return JsonResponse({'error': str(e)}, status=400)
