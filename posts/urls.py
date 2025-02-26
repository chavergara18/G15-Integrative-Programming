from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDeleteView, SingletonConfigView  

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
    path('singleton/', SingletonConfigView.as_view(), name='singleton'), 
]




