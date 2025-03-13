from django.urls import path, include
from .views import (
    PostListCreateView, 
    PostRetrieveUpdateDeleteView, 
    LikePostView, 
    UnlikePostView, 
    CommentPostView,
    PostCommentsView,
    SingletonConfigView
)
from .views import NewsFeedView

urlpatterns = [
    
    path("posts/", PostListCreateView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostRetrieveUpdateDeleteView.as_view(), name="post-detail"),
    path("posts/<int:post_id>/like/", LikePostView.as_view(), name="like-post"),
    path("posts/<int:post_id>/unlike/", UnlikePostView.as_view(), name="unlike-post"),
    path("posts/<int:post_id>/comment/", CommentPostView.as_view(), name="comment-post"),
    path("posts/<int:post_id>/comments/", PostCommentsView.as_view(), name="post-comments"),
    path("singleton/", SingletonConfigView.as_view(), name="singleton"),
    path("feed/", NewsFeedView.as_view(), name="news-feed"),
    

    
    path("auth/", include("dj_rest_auth.urls")), 
    path("auth/registration/", include("dj_rest_auth.registration.urls")),  
    path("auth/social/", include("allauth.socialaccount.urls")),  
]







