# tracker/views.py

from rest_framework import generics
from django.utils import timezone
from .models import Task
from .serializers import DueSoonSerializer

class DueSoonListView(generics.ListAPIView):
    serializer_class = DueSoonSerializer

    def get_queryset(self):
        # közvetlen lekérdezés a táblákra, materializált nézet nélkül
        now = timezone.now()
        later = now + timezone.timedelta(hours=48)
        sql = """
        SELECT
          t.*,
          p.name AS project_name
        FROM task t
        JOIN project p ON p.id = t.project_id
        WHERE t.status <> 'done'
          AND t.due_at BETWEEN %s AND %s
        ORDER BY t.due_at
        """
        return Task.objects.raw(sql, [now, later])
