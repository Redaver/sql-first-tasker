import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client(db):
    return APIClient()

@pytest.fixture
def demo_data(db):
    """Raw SQL seed a user, project és task táblákba."""
    from django.db import connection
    from django.utils import timezone

    now = timezone.now()
    cursor = connection.cursor()

    # 1) init.sql szerinti "user" tábla
    cursor.execute("""
        INSERT INTO "user"(email, full_name)
        VALUES ('a@b.com', 'A B') RETURNING id;
    """)
    user_id = cursor.fetchone()[0]

    # 2) project hivatkozva a fenti user_id-re
    cursor.execute("""
        INSERT INTO project(name, owner_id)
        VALUES ('P', %s) RETURNING id;
    """, [user_id])
    project_id = cursor.fetchone()[0]

    # 3) task hivatkozva a fenti project_id-re
    cursor.execute("""
        INSERT INTO task(project_id, title, due_at)
        VALUES (%s, 'T', %s) RETURNING id;
    """, [project_id, now])
    task_id = cursor.fetchone()[0]

    return {"user_id": user_id, "project_id": project_id, "task_id": task_id}

def test_due_soon_empty(api_client):
    resp = api_client.get('/api/due-soon/')
    assert resp.status_code == 200
    assert resp.json() == []

def test_due_soon_with_task(api_client, demo_data):
    resp = api_client.get('/api/due-soon/')
    data = resp.json()
    assert isinstance(data, list) and len(data) == 1
    assert data[0]['id'] == demo_data["task_id"]
    assert data[0]['title'] == 'T'
