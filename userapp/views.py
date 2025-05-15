

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        batch = request.POST.get('batch', '')
        n_adult = request.POST.get('n_adult', '')
        n_child = request.POST.get('n_child', '')
        photo = request.FILES.get('photo')

        context = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'phone': phone,
            'batch': batch,
            'n_adult':n_adult,
            'n_child':n_child,

        }

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            context['password1'] = ''
            context['password2'] = ''
            return render(request, 'userapp/register.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            context['username'] = ''
            return render(request, 'userapp/register.html', context)

        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already used.")
            context['phone'] = ''
            return render(request, 'userapp/register.html', context)

        if not batch:
            messages.error(request, "Batch is required.")
            return render(request, 'userapp/register.html', context)

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = full_name
        user.save()

        UserProfile.objects.create(
            user=user,
            phone=phone,
            batch=batch,
            photo=photo,
            n_adult=n_adult,
            n_child=n_child,
            is_approved=False
        )

        messages.success(request, "Registration successful. Awaiting approval.")
        return redirect('approval_status', username=username)

    return render(request, 'userapp/register.html')


def approval_status(request, username):
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        is_approved = profile.is_approved
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        is_approved = False

    return render(request, 'userapp/approval_status.html', {
        'is_approved': is_approved,
        'username': username
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', 'user_dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Your account is not approved yet.")
                return redirect('user_login')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('user_login')

    return render(request, 'userapp/login.html')

@login_required(login_url='/user/login/')
def user_dashboard(request):
    user_id = request.user.id
    return render(request, 'userapp/user_dashboard.html', {'user_id': user_id})