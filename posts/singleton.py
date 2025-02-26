class SingletonMeta(type):
    """A metaclass for implementing Singleton Pattern"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class PostConfigManager(metaclass=SingletonMeta):
    """Singleton class to manage post configurations"""
    def __init__(self):
        self.settings = {"max_posts_per_user": 10, "allow_comments": True}



