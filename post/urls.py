from django.urls import path
from .views import register_user, login_user, PostDetailView, ProtectedView, PostListCreateView 

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post_list_create'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('protected/', ProtectedView.as_view(), name='protected_view'),
]























