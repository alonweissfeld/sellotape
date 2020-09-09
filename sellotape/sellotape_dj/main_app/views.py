from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def index(request):
    return render(request, 'sellotape/index.html')

def user(request, username):
    # Get the profile for the passed username or raise 404 if not found.
    profile = get_object_or_404(User, username=username)
    
    context = {
        'profile': profile,
    }
    return render(request, 'sellotape/user.html', context)
