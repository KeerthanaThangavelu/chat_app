from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings


class Message(models.Model):
    """
    A model representing a message sent between users.

    Attributes:
        sender (ForeignKey): The user who sends the message.
        receiver (ForeignKey): The user who receives the message.
        encrypted_text (BinaryField): The encrypted text of the message.
        timestamp (DateTimeField): The time when the message was created.
        read (BooleanField): A flag indicating if the message has been read.
    """
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    encrypted_text = models.BinaryField()  # Store encrypted text
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def encrypt_message(self, text):
        """
        Encrypt the message text using a symmetric key.

        Args:
            text (str): The plaintext message to be encrypted.

        Returns:
            bytes: The encrypted message as bytes.
        """
        cipher = Fernet(settings.FERNET_KEY)
        return cipher.encrypt(text.encode())

    def decrypt_message(self):
        """
        Decrypt the encrypted message text.

        Returns:
            str: The decrypted message as a string.
        """
        cipher = Fernet(settings.FERNET_KEY)
        return cipher.decrypt(self.encrypted_text).decode()

    def save(self, *args, **kwargs):
        """
        Override the save method to encrypt the message text before saving.
        Only encrypts the message if it is new (does not have a primary key).

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.pk:  # Only encrypt if this is a new message
            self.encrypted_text = self.encrypt_message(self.text)
        super().save(*args, **kwargs)

    @property
    def text(self):
        """
        Property to get the decrypted message text.

        Returns:
            str: The decrypted message text.
        """
        return self.decrypt_message()
