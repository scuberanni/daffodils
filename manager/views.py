from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from userapp.models import UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import admin
from django.http import HttpRequest





def home(request):
    return render(request, 'home.html')

def custom_admin_view(request: HttpRequest):
    return admin.site.admin_view(lambda req: req)(request)

@login_required
def dashboard(request):
    if request.user.username == 'daffodils':
        return render(request, 'dashboard.html')
    else:
        return HttpResponseForbidden("Access denied: You are not authorized to view this page.")

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