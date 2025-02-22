from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Abstract Base Class for shared content fields
class ContentBase(models.Model):
    content = models.TextField(blank=False)  # Shared content field
    
    class Meta:
        abstract = True  # This class won't create a database table

# User model
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, blank=False)
    email = models.EmailField(max_length=50, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# Reaction Strategy Pattern
class ReactionStrategy:
    def react(self, user, post):
        raise NotImplementedError()

class ThumbsUp(ReactionStrategy):
    def react(self, user, post):
        post.liked_by.add(user)
        print(f"{user.username} gave a thumbs-up to the post.")

class Heart(ReactionStrategy):
    def react(self, user, post):
        post.liked_by.add(user)
        print(f"{user.username} gave a heart to the post.")

class Clap(ReactionStrategy):
    def react(self, user, post):
        post.liked_by.add(user)
        print(f"{user.username} clapped for the post.")

# Post Factory Pattern for different post types
class PostFactory:
    @staticmethod
    def create_post(post_type, content, author):
        if post_type == "text":
            return TextPost(content=content, author=author)
        elif post_type == "image":
            return ImagePost(content=content, author=author)
        else:
            raise ValueError("Unknown post type")

# Post Model (TextPost subclass)
class Post(ContentBase):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=False)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

    # Add a reaction using a Strategy Pattern
    def add_reaction(self, user, strategy: ReactionStrategy):
        strategy.react(user, self)

# Image Post Model (Inheriting from Post for extension)
class ImagePost(Post):
    image_url = models.URLField()

    def __str__(self):
        return f"Image Post by {self.author.username} at {self.created_at}"

# Text Post Model (Inheriting from Post)
class TextPost(Post):
    def __str__(self):
        return f"Text Post by {self.author.username} at {self.created_at}"

# Comment Model (Uses ContentBase as abstract parent)
class Comment(ContentBase):
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, blank=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"

# Observer Pattern using Django signals
@receiver(post_save, sender=Comment)
def notify_post_author(sender, instance, **kwargs):
    post = instance.post
    author = post.author
    print(f"Notify {author.username} that their post was commented on by {instance.author.username}")




