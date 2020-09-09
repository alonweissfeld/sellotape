from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    return render(request, 'sellotape/index.html')

def user(request, username):
    # Get the query set profile for the passed username
    qs = User.objects.filter(username=username)
    if not qs.exists():
        raise Http404

    profile = qs.first()
    context = {
        'username': username,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email
    }
    return render(request, 'sellotape/user.html', context)
