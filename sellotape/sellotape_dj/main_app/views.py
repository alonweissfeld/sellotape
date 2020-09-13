from datetime import datetime
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

    # Check if there is a live stream at the moment.
    live_stream = None
    for s in streams:
        if not s['ended_on']:
            live_stream = s
            break

    # Filter streams data based on the current time of serving the page.
    now = datetime.now()
    future_streams = [s for s in streams if s['airs_on'] > now]
    previous_streams = [s for s in streams if s not in future_streams]

    if live_stream in previous_streams:
        previous_streams.remove(live_stream)

    context = {
        'profile': profile,
        'future_streams': future_streams,
        'previous_streams': previous_streams,
        'live_stream': live_stream,
    }
    return render(request, 'sellotape/user.html', context)
