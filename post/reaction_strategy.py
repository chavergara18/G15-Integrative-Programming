# post/reaction_strategy.py

class ReactionStrategy:
    def react(self, post, user):
        raise NotImplementedError("Each strategy must implement the react method.")


class ThumbsUp(ReactionStrategy):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThumbsUp, cls).__new__(cls)
        return cls._instance

    def react(self, post, user):
        # Add the logic to react with thumbs up (e.g., save reaction in the DB)
        pass


class Heart(ReactionStrategy):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Heart, cls).__new__(cls)
        return cls._instance

    def react(self, post, user):
        # Add the logic to react with heart
        pass


class Clap(ReactionStrategy):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Clap, cls).__new__(cls)
        return cls._instance

    def react(self, post, user):
        # Add the logic to react with clap
        pass
