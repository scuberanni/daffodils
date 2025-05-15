from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    if request.user.username == 'daffodils':
        return render(request, 'dashboard.html')
    else:
        return HttpResponseForbidden("Access denied: You are not authorized to view this page.")
