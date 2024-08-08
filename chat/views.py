import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from cryptography.fernet import Fernet
from django.conf import settings

from .models import Message


# Create your views here.
# Home page
@login_required
def index(request):
    """
    Render the home page with a list of users, excluding the current user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered home page with the list of users.
    """
    users = User.objects.exclude(id=request.user.id)  # Exclude current user from list
    return render(request, 'index.html', {'users': users})


# signup page
def user_signup(request):
    """
    Handle user signup. If the request method is POST, process the form data and create a new user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The signup page with the signup form, or redirect to the login page on success.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


# login page
def user_login(request):
    """
    Handle user login. If the request method is POST, authenticate and log in the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The login page with the login form, or redirect to the home page on success.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# logout page
def user_logout(request):
    """
    Log out the current user and redirect to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirect to the login page.
    """
    logout(request)
    return redirect('login')


@login_required
def get_messages(request, user_id):
    """
    Get messages between the current user and a specified user, and return them as JSON.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user to get messages with.

    Returns:
        JsonResponse: JSON response containing the list of messages.
    """
    # Get messages between the current user and the selected user
    messages = Message.objects.filter(
        sender_id=request.user.id, receiver_id=user_id
    ).union(
        Message.objects.filter(sender_id=user_id, receiver_id=request.user.id)
    ).order_by('timestamp')

    # Mark messages as read
    Message.objects.filter(receiver=request.user, read=False).update(read=True)

    messages_list = [{'text': message.decrypt_message(), 'sender': message.sender.username,
                      'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for message in messages]

    return JsonResponse({'messages': messages_list})


@csrf_exempt
@login_required
def send_message(request):
    """
   Handle sending a message. Encrypt the message text and save it to the database.

   Args:
       request (HttpRequest): The HTTP request object.

   Returns:
       JsonResponse: JSON response with the sent message, or an error message.
   """
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        message_text = data.get('message')

        try:
            receiver = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)

        cipher = Fernet(settings.FERNET_KEY)
        encrypt_message = cipher.encrypt(message_text.encode())

        message = Message(sender=request.user, receiver=receiver, encrypted_text=encrypt_message)
        message.save()

        # Return the message back to the front-end
        return JsonResponse({
            'message': {
                'text': message.text,
                'sender': request.user.username,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_user_list_with_unread_count(request):
    """
    Get a list of users with the count of unread messages for the current user, and return as JSON.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: JSON response containing the list of users and their unread message count.
    """
    users = User.objects.exclude(id=request.user.id)
    user_list = []
    for user in users:
        unread_count = Message.objects.filter(
            sender=user.id,
            read=False
        ).count()
        user_list.append({
            'id': user.id,
            'username': user.username,
            'unread_messages': unread_count
        })
    return JsonResponse({'users': user_list})
