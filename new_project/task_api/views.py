from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    # Override get_queryset to ensure users can only see their own tasks
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(created_by=user)  # Tasks belonging to the logged-in user



