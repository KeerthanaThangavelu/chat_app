## Chat Application

This project is a web-based chat application developed using Django . The application provides features of User Authentication, Real-Time Messaging, User Interface, and Message Encryption.

## Objectives
-	User Authentication: Implement user registration, login, and logout.
-	Real-Time Messaging: Enable real-time messaging between users with encryption.
-	User Interface: Develop a responsive and intuitive user interface.
-	Message Encryption: Ensure messages are encrypted during storage and decrypted during retrieval.

### Technical Requirements

#### Technologies Used

- *Django*: Web framework for building the application.
- *SQLite*: Default database for development (can be replaced with PostgreSQL, MySQL, etc. for production).
- *HTML/CSS*: Frontend design and styling.

### System Architecture and Design

- *Models*: Defines the structure of the chat user information and encrypted messages.
- *Views*: Handles the business logic and interactions.
- *Templates*: Renders HTML pages to be displayed to the user.
- *URLs*: Maps URL paths to the corresponding views.

## Project Structure

    .
    ├── templates                           
    │   ├── signup.html                     # Template for signup of users.
    │   ├── index.html                      # Template to display and send messages and the user list. 
    │   ├── login.html                      # Template for login page.
    │   └── base.html                       # Base template that other templates extend.
    ├── admin.py                            # Configuration for the Django admin interface.
    ├── apps.py                             # Configuration for the chat app.
    ├── forms.py                            # Forms for logging in and signup models.
    ├── models.py                           # Contains the Message models.
    ├── tests.py                            # Unit tests for the views in the chat app.
    ├── urls.py                             # URL routing for the chat app.
    └── views.py                            # View functions for user creation,login, send message, read message, logout.

## Getting Started

### Prerequisites

- Python 3.x
- Django 5.0.7

### Installation
1. Clone the repository/Download project file
```
cd chat_app
```
2. Create and Activate Virtual Environment
```
pip install vitualenv python -m venv env
source env/bin/ativate # On Windows use `env\Scripts\activate`
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. . Run migration
``` 
python manage.py migrate
```
5. Create Super User
```
python manage.py createsuperuser
```
6. Run the development server
```
python manage.py runserver
```
7. Open your browser and navigate to `http://localhost:8000/chat/login/` to access the application.

### Usage

- Access the application at http://127.0.0.1:8000/
- Sign up new user 
- Login with the created user 
- Navigate through the application view all the signed up contacts and chat.

### Testing

Unit tests are provided to ensure the functionality of the application. To run the tests:

```
python manage.py test chat
```
