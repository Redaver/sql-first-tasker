from django.contrib import admin
from django.urls import path
from tracker.views import DueSoonListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/due-soon/', DueSoonListView.as_view(), name='due-soon'),
]
