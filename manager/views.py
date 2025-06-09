from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from userapp.models import UserProfile,TeacherProfile,events,EventPhoto,EventVideo
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
from userapp.forms import TeacherProfileForm,EventPhotoForm,EventVideoForm



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
    users = UserProfile.objects.all().order_by('batch')
    return render(request, 'gallery.html', {'users': users})

@daffodils_required
def approve_user(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)

    if not profile.is_approved:
        profile.is_approved = True
        profile.save()

        # Send WhatsApp message (open WhatsApp Web with pre-filled message)
        phone = profile.phone
        message = urllib.parse.quote("Hi {}, Your Registration has been Approved. Welcome! to Daffodils Rewind_2025".format(profile.user.first_name or profile.user.username))
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

@daffodils_required
def teachers(request):
    users = TeacherProfile.objects.all()
    return render(request, 'teacher.html', {'users': users})

@daffodils_required
def add_teacher_profile(request):
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teachers')  # replace with your success page/view name
    else:
        form = TeacherProfileForm()
    return render(request, 'add_teacher_profile.html', {'form': form})

@daffodils_required
def edit_teacher_profile(request, pk):
    teacher = get_object_or_404(TeacherProfile, pk=pk)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers')  # Adjust this to your main teacher list view
    else:
        form = TeacherProfileForm(instance=teacher)
    
    return render(request, 'edit_teacher.html', {'form': form, 'teacher': teacher})

@daffodils_required
def table(request): 
    profiles = UserProfile.objects.all().order_by('is_approved', 'batch')
    return render(request, 'table.html', {'profiles': profiles})

@daffodils_required
def event(request): 
    profiles = events.objects.all()
    return render(request, 'event.html', {'profiles': profiles})

@daffodils_required
def add_event(request): 
    return render(request, 'add_event.html')

@daffodils_required
def register_event(request):
    if request.method == 'POST':
        name1 = request.POST.get('name', '')
        photo1 = request.FILES.get('photo')

        events.objects.create(
            name=name1,
            photo=photo1,

        )

        return redirect('event')

    return render(request, 'add_event.html')

@daffodils_required
def add_event_photo(request):
    if request.method == 'POST':
        form = EventPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo uploaded successfully!")
            return redirect('gallery')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventPhotoForm()

    return render(request, 'add_event_photo.html', {'form': form})

@daffodils_required
def photos(request): 
    profiles = EventPhoto.objects.all()
    return render(request, 'photos.html', {'profiles': profiles})

@daffodils_required
def event_photos_detail(request, pk):
    video = get_object_or_404(EventPhoto, pk=pk)
    return render(request, 'event_photos_detail.html', {'video': video})

@daffodils_required
def edit_event_photos(request, pk):
    video_obj = get_object_or_404(EventPhoto, pk=pk)
    if request.method == 'POST':
        form = EventPhotoForm(request.POST, request.FILES, instance=video_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Video updated successfully!")
            return redirect('photos')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventPhotoForm(instance=video_obj)
    return render(request, 'event_photo_edit.html', {'form': form, 'title': 'Edit photo'})

@daffodils_required
def delete_event_photos(request, pk):
    video_obj = get_object_or_404(EventPhoto, pk=pk)
    if request.method == 'POST':
        video_obj.delete()
        messages.success(request, "photo deleted successfully!")
        return redirect('photos')
    return render(request, 'confirm_delete_photo.html', {'video': video_obj})

@daffodils_required
def add_event_video(request):
    if request.method == 'POST':
        form = EventVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Video uploaded successfully!")
            return redirect('gallery')  # Adjust if you have a separate video gallery
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventVideoForm()

    return render(request, 'add_event_video.html', {'form': form})

@daffodils_required
def videos(request): 
    profiles = EventVideo.objects.all()
    return render(request, 'videos.html', {'profiles': profiles})

@daffodils_required
def event_video_detail(request, pk):
    video = get_object_or_404(EventVideo, pk=pk)
    return render(request, 'event_video_detail.html', {'video': video})

@daffodils_required
def edit_event_video(request, pk):
    video_obj = get_object_or_404(EventVideo, pk=pk)
    if request.method == 'POST':
        form = EventVideoForm(request.POST, request.FILES, instance=video_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Video updated successfully!")
            return redirect('videos')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventVideoForm(instance=video_obj)
    return render(request, 'event_video_edit.html', {'form': form, 'title': 'Edit Video'})

@daffodils_required
def delete_event_video(request, pk):
    video_obj = get_object_or_404(EventVideo, pk=pk)
    if request.method == 'POST':
        video_obj.delete()
        messages.success(request, "Video deleted successfully!")
        return redirect('videos')
    return render(request, 'confirm_delete.html', {'video': video_obj})

@daffodils_required
def event_detail(request,pk): 
    event = get_object_or_404(events, pk=pk)
    return render(request, 'event_details.html', {'event': event})

@daffodils_required
def photos_event(request, event_name):
    event = get_object_or_404(events, name=event_name)
    photos = EventPhoto.objects.filter(event=event).order_by('-updated_date')
    return render(request, 'event_photos.html', {'event': event, 'profiles': photos})

@daffodils_required
def videos_event(request, event_name):
    event = get_object_or_404(events, name=event_name)
    videos = EventVideo.objects.filter(event=event).order_by('-updated_date')
    return render(request, 'event_videos.html', {'event': event, 'profiles': videos})

@daffodils_required
def event_video_details(request, pk):
    video = get_object_or_404(EventVideo, pk=pk)
    return render(request, 'event_video_detail1.html', {'video': video})

@daffodils_required
def event_photos_details(request, pk):
    video = get_object_or_404(EventPhoto, pk=pk)
    return render(request, 'event_photos_detail1.html', {'video': video})