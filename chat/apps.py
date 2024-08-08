from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
        Configuration class for the 'chat' application.

        Attributes:
            default_auto_field (str): Specifies the default auto field type for primary keys.
            name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
