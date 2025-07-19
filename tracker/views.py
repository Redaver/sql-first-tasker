# tracker/views.py

from rest_framework import generics
from django.utils import timezone
from .models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import connection
from .serializers import DueSoonSerializer
from .serializers import TaskStatusSerializer



class TaskSetStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = TaskStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']

        with connection.cursor() as cursor:
            cursor.execute("SELECT task_set_status(%s, %s);", [pk, new_status])

        return Response({'id': pk, 'status': new_status}, status=status.HTTP_200_OK)

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
