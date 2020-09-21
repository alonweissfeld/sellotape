from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

def create_user_with_streams(username, streams):
    """
    Create a user with the given streams.
    """
    return User.objects.create(username=username)

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
        create_user_with_streams(username, [])

        url = reverse('main_app:user', args=(username,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No streams are available.")
        self.assertQuerysetEqual(response.context['future_streams'], [])
        self.assertQuerysetEqual(response.context['previous_streams'], [])
