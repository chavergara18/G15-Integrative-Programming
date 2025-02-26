from .models import Post

class PostFactory:
    @staticmethod
    def create_post(author, title, content):
        return Post.objects.create(author=author, title=title, content=content)


