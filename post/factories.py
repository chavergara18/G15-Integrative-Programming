from .models import Post, User

class PostFactory:
    @staticmethod
    def create_post(post_type, content, user):
        # You can define different types of post creation logic based on the 'post_type'
        if post_type == "text":
            # Create a text post
            post = Post(content=content, author=user, post_type="text")
        elif post_type == "image":
            # Logic for image post creation (example)
            post = Post(content=content, author=user, post_type="image")
        elif post_type == "video":
            # Logic for video post creation (example)
            post = Post(content=content, author=user, post_type="video")
        else:
            raise ValueError("Invalid post type")

        return post
