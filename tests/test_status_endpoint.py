import pytest
from rest_framework.test import APIClient
from django.utils import timezone   # legyen itt
# ne használd get_user_model a demo felhasználóhoz, csak raw SQL

@pytest.fixture
def api_client(db):
    return APIClient()

@pytest.fixture
def auth_client(api_client, db):
    # seed auth felhasználó (django auth_user), ha JWT-hez szükséges
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_user(username='admin', password='adminpass')

    # kérj tokent
    resp = api_client.post(
        '/api/token/',
        {'username':'admin','password':'adminpass'},
        format='json'
    )
    token = resp.json()['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

def test_set_status(auth_client, db):
    # seed a külön táblákba
    from django.db import connection
    now = timezone.now()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO "user"(email, full_name)
        VALUES ('x@y','X Y') RETURNING id;
    """)
    user_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO project(name, owner_id)
        VALUES ('P', %s) RETURNING id;
    """, [user_id])
    project_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO task(project_id, title, due_at)
        VALUES (%s, 'X', %s) RETURNING id;
    """, [project_id, now])
    task_id = cursor.fetchone()[0]

    # végpont meghívása
    resp = auth_client.post(
        f'/api/tasks/{task_id}/actions/set_status/',
        {'status':'in_progress'},
        format='json'
    )
    assert resp.status_code == 200
    assert resp.json()['status'] == 'in_progress'
