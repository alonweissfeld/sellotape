from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Stream
from django.contrib.auth.models import User

def create_user(username):
    """
    Create a user for the test db by a given username.
    """
    return User.objects.create(username=username)

def create_streams(streams):
    """
    Create streams for the test db.
    """
    for stream in streams:
        Stream.objects.create(**stream)

class UserViewTests(TestCase):
    def test_user_does_not_exist(self):
        """
        If user does not exist, it returns a 404.
        """
        url = reverse('main_app:user', args=('non-exist',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_no_streams(self):
        """
        If no streams are available, an appropriate message is displayed.
        """
        username = 'darth-vader'
        create_user(username)

        url = reverse('main_app:user', args=(username,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No streams are available.")
        self.assertQuerysetEqual(response.context['future_streams'], [])
        self.assertQuerysetEqual(response.context['previous_streams'], [])
        self.assertTemplateUsed(response, 'sellotape/user.html')

    def test_finds_live_stream(self):
        """
        If there is a live stream happening at the moment,
        it should be passed to the response context.
        """
        username = 'darth-vader'
        user = create_user(username)
        
        now = timezone.now()
        streams = [
            {
                'author': user,
                'airs_on': now.replace(hour=(now.hour - 1)),
                'ends_on': now.replace(hour=(now.hour + 1)),
                'title': 'Live Stream',
                'added_on': now
            },
        ]
        create_streams(streams)

        url = reverse('main_app:user', args=(username,))
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['live_stream'])
        self.assertEqual(response.context['live_stream'].title, 'Live Stream')

    def test_splits_streams(self):
        """
        The view should split future and previous streams based on the current time
        and the streams data.
        """
        username = 'darth-vader'
        user = create_user(username)

        now = timezone.now()
        streams = [
            {
                'author': user,
                'airs_on': now.replace(year=(now.year + 1)),
                'ends_on': None,
                'title': 'Future Stream',
                'added_on': now
            },
            {
                'author': user,
                'airs_on': now.replace(year=(now.year - 1)),
                'ends_on': now.replace(hour=now.hour),
                'title': 'Previous Stream',
                'added_on': now
              }

        ]
        create_streams(streams)

        url = reverse('main_app:user', args=(username,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        future_streams = response.context['future_streams']
        previous_streams = response.context['previous_streams']
        
        self.assertTrue(len(future_streams))
        self.assertTrue(len(previous_streams))
        self.assertEqual(future_streams[0].title, 'Future Stream')
        self.assertEqual(previous_streams[0].title, 'Previous Stream')
