from django.urls import path
from .views import get_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]