from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

def get_default_user():
    """Returns the ID of the first available user as the default."""
    user = get_user_model().objects.first()
    return user.id if user else None  # Return ID or None to avoid issues

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=get_default_user  # Ensures a valid user ID
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title






