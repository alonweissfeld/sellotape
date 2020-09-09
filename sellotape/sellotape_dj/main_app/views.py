from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def index(request):
    return render(request, 'sellotape/index.html')

def user(request, username):
    # Get the profile for the passed username or raise 404 if not found.
    profile = get_object_or_404(User, username=username)

    # TODO: query the user streams once the strams table is merged.
    streams = []
    is_live = len(streams) and streams[0]['ended_on'] == None
    live_link = is_live and streams[0]['link']
    
    context = {
        'profile': profile,
        'streams': streams,
        'live_link': live_link,
    }
    return render(request, 'sellotape/user.html', context)
