from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from cryptography.fernet import Fernet
import json

from .models import Message
from .forms import SignupForm, LoginForm


class ChatAppTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case environment. This includes creating test users and
        setting up the test client for sending requests.
        """
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.user3 = User.objects.create_user(username='user3', password='pass3')

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.signup_url = reverse('signup')
        self.home_url = reverse('home')
        self.get_messages_url = reverse('get_messages', args=[self.user2.id])
        self.send_message_url = reverse('send_message')
        self.get_user_list_url = reverse('user_list')

    def login_user(self, username, password):
        """
        Helper method to log in a user.
        """
        self.client.post(self.login_url, {'username': username, 'password': password})

    def test_index_view(self):
        """
        Test the index view to ensure it returns the home page and excludes the current user.
        """
        self.login_user('user1', 'pass1')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertNotIn(self.user1, response.context['users'])

    def test_user_signup_view(self):
        """
        Test the user signup view to ensure a new user can register successfully.
        """
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_user_login_view(self):
        """
        Test the user login view to ensure a user can log in with correct credentials.
        """
        response = self.client.post(self.login_url, {
            'username': 'user1',
            'password': 'pass1'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.url == self.home_url)

    def test_user_logout_view(self):
        """
        Test the user logout view to ensure a user can log out successfully.
        """
        self.login_user('user1', 'pass1')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful logout
        self.assertTrue(response.url == self.login_url)

    def test_get_messages_view(self):
        """
        Test the get_messages view to ensure it returns the messages between users as JSON.
        """
        self.login_user('user1', 'pass1')
        cipher = Fernet(settings.FERNET_KEY)
        message_text = 'Hello, user2!'
        encrypted_message = cipher.encrypt(message_text.encode())
        Message.objects.create(sender=self.user1, receiver=self.user2, encrypted_text=encrypted_message)

        response = self.client.get(reverse('get_messages', args=[self.user2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['messages'][0]['text'], message_text)

    def test_send_message_view(self):
        """
        Test the send_message view to ensure a message can be sent and saved correctly.
        """
        self.login_user('user1', 'pass1')
        message_text = 'Hello, user2!'

        response = self.client.post(
            self.send_message_url,
            json.dumps({'user_id': self.user2.id, 'message': message_text}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message']['text'], message_text)

    def test_get_user_list_with_unread_count_view(self):
        """
        Test the get_user_list_with_unread_count view to ensure it returns users with unread message counts.
        """
        self.login_user('user1', 'pass1')
        cipher = Fernet(settings.FERNET_KEY)
        message_text = 'Hello, user1!'
        encrypted_message = cipher.encrypt(message_text.encode())
        Message.objects.create(sender=self.user2, receiver=self.user1, encrypted_text=encrypted_message)

        response = self.client.get(self.get_user_list_url)
        self.assertEqual(response.status_code, 200)
        users_list = response.json()['users']
        self.assertIn('unread_messages', users_list[0])
        self.assertEqual(users_list[0]['unread_messages'], 1)
