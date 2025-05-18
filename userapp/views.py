

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login, logout
import urllib.parse
import webbrowser  # for optional testing
from django.shortcuts import get_object_or_404
from django import forms

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
            try:
                user_profile = user.userprofile
                if user_profile.is_approved:
                    login(request, user)
                    next_url = request.GET.get('next', 'user_dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, "Your account is not approved yet.")
                    return redirect('user_login')
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found. Contact admin.")
                return redirect('user_login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('user_login')

    return render(request, 'userapp/login.html')

@require_GET
def user_logout(request):
    logout(request)
    return redirect('home') 


@login_required(login_url='/user/login/')
def user_dashboard(request):
    user_id = request.user.id
    return render(request, 'userapp/user_dashboard.html', {'user_id': user_id})

@login_required
def view_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('home')  # or show an error page 

    return render(request, 'userapp/view_profile.html', {'profile': profile})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'batch', 'n_adult', 'n_child', 'photo']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']

@login_required
def edit_profile(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    user = profile.user

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('view_profile')
    else:
        u_form = UserForm(instance=user)
        p_form = UserProfileForm(instance=profile)

    return render(request, 'userapp/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    })

@login_required
def user_detail(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    return render(request, 'userapp/user_detail.html', {'profile': profile})

@login_required
def user_class_a(request):
    users = UserProfile.objects.filter(batch="10A", is_approved=True)
    return render(request, 'userapp/class.html', {'users': users})

@login_required
def user_class_b(request):
    users = UserProfile.objects.filter(batch="10B", is_approved=True)
    return render(request, 'userapp/class.html', {'users': users})

@login_required
def user_class_c(request):
    users = UserProfile.objects.filter(batch="10C", is_approved=True) 
    return render(request, 'userapp/class.html', {'users': users})

@login_required
def user_class_d(request):
    users = UserProfile.objects.filter(batch="10D", is_approved=True)
    return render(request, 'userapp/class.html', {'users': users})