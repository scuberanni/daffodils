from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from userapp.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib import admin
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.parse
import webbrowser  # for optional testing
from django.shortcuts import get_object_or_404
from django import forms



from functools import wraps

def daffodils_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.username == 'daffodils':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied: You are not authorized to view this page.")
    return _wrapped_view





def home(request):
    return render(request, 'home.html')

def custom_admin_view(request: HttpRequest):
    return admin.site.admin_view(lambda req: req)(request)

@daffodils_required
def dashboard(request):
    return render(request, 'dashboard.html')

@daffodils_required
def register_new(request):
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

        # Prepare context with all data to refill except error field(s)
        context = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'phone': phone,
            'batch': batch,
            'n_adult':n_adult,
            'n_child':n_child,

        }

        # Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            context['password1'] = ''
            context['password2'] = ''
            return render(request, 'register_new.html', context)

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            context['username'] = ''
            return render(request, 'register_new.html', context)

        # Phone exists check
        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already used.")
            context['phone'] = ''
            return render(request, 'register_new.html', context)

        # Batch validation
        if not batch:
            messages.error(request, "Batch is required.")
            return render(request, 'register_new.html', context)

        # Create user & profile
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

        return redirect('dashboard')

    return render(request, 'register_new.html')

@daffodils_required
def users_list(request):
    users = UserProfile.objects.all().order_by('is_approved', 'batch')
    return render(request, 'users_list.html', {'users': users})

@daffodils_required
def gallery(request):
    users = UserProfile.objects.all().order_by('batch')[:50]  # limit to first 50
    return render(request, 'gallery.html', {'users': users})



@daffodils_required
def approve_user(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)

    if not profile.is_approved:
        profile.is_approved = True
        profile.save()

        # Send WhatsApp message (open WhatsApp Web with pre-filled message)
        phone = profile.phone
        message = urllib.parse.quote("Hi {}, your registration has been approved. Welcome! to daffodils".format(profile.user.first_name or profile.user.username))
        whatsapp_url = f"https://wa.me/{phone}?text={message}"

        # You can open the URL in a new tab for local testing (desktop)
        # webbrowser.open(whatsapp_url)

        messages.success(request, f"User '{profile.user.username}' approved successfully.")
        return HttpResponseRedirect(whatsapp_url)  # Or redirect to user list after approval
    else:
        messages.info(request, "User is already approved.")
        return redirect('users_list')
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'batch', 'n_adult', 'n_child', 'photo']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email']

@daffodils_required
def edit_user_profile(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    user = profile.user

    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('users list')
    else:
        u_form = UserForm(instance=user)
        p_form = UserProfileForm(instance=profile)

    return render(request, 'edit_user.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    })