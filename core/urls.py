from django.contrib import admin
from django.urls import path
from tracker.views import DueSoonListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tracker.views import TaskSetStatusView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/due-soon/', DueSoonListView.as_view(), name='due-soon'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/tasks/<int:pk>/actions/set_status/', TaskSetStatusView.as_view(), name='task_set_status'),
]
