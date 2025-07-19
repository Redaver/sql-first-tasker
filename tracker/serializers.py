# tracker/serializers.py

from rest_framework import serializers
from .models import Task



class TaskStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('todo','todo'),
        ('in_progress','in_progress'),
        ('done','done'),
    ])

class DueSoonSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Task
        # ügyelj rá, hogy az mv_due_soon view-hez tartozó Task modell is tartalmazza a project_name mezőt
        fields = ['id', 'title', 'status', 'due_at', 'project_name']
