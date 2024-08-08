from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Define a custom form class for user sign-up, inheriting from UserCreationForm
class SignupForm(UserCreationForm):
    """
        Form for creating a new user account. Inherits from UserCreationForm
        to leverage built-in user creation functionalities.

        Attributes:
            model (User): The User model to use for this form.
            fields (list): Fields to include in the form ('username', 'password1', 'password2').
            error_messages (dict): Custom error messages for form validation.
    """

    class Meta:
        # Specify the model to use for this form (User model)
        model = User
        # Define the fields to include in the form
        fields = ['username', 'password1', 'password2']
        # Custom error messages
        error_messages = {
            'username': {
                'required': 'Username is required.',  # Error message when username is not provided
                'max_length': 'Username is too long.',  # Error message when username exceeds max length
                'invalid': 'Enter a valid username.',  # Error message when username is invalid
            },
        }


# Define a custom form class for user login, inheriting from Django's Form class
class LoginForm(forms.Form):
    """
        Form for user login. Inherits from Django's Form class.

        Attributes:
            username (CharField): Field for entering the username.
            password (CharField): Field for entering the password with a PasswordInput widget.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
