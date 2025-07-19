import pytest
from django.db import connection, ProgrammingError

# A sima CREATE TABLE DDL-eket split‑elve töltjük be:
def _load_tables(cursor, sql):
    # Vegyük ki belőle a függvényblokkot:
    parts = sql.split('$$')
    # parts[0]: minden a függvény előtt
    # parts[1]: a függvény törzse
    # parts[2]: minden a függvény után
    table_sql, func_body, _ = parts
    for stmt in table_sql.split(';'):
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt + ';')

# A függvényt egyszerre, dollar‑quote‑kal együtt:
FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION task_set_status(_task BIGINT, _new TEXT)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
  UPDATE task
    SET status = _new
    WHERE id = _task;

  INSERT INTO task_event(task_id, event)
    VALUES (_task, 'STATUS_' || upper(_new));

  PERFORM pg_notify('task_channel', _task || ':' || _new);
END;
$$;
"""

@pytest.fixture(scope='session', autouse=True)
def load_init_sql(django_db_setup, django_db_blocker):
    path = 'db/init.sql'
    with django_db_blocker.unblock():
        sql = open(path, encoding='utf-8').read()
        cursor = connection.cursor()
        # 1) táblák + nézetek, CREATE TABLE stb.
        try:
            _load_tables(cursor, sql)
        except ProgrammingError as e:
            # Ha már van, átlépjük
            connection.rollback()
        # 2) task_event tábla (ha init.sql‑ben van, nem kell, de biztosra megyünk)
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_event (
              id BIGSERIAL PRIMARY KEY,
              task_id BIGINT REFERENCES task(id),
              event TEXT,
              happened_at TIMESTAMPTZ DEFAULT now()
            );
            """)
        except ProgrammingError:
            connection.rollback()
        # 3) PL/pgSQL függvény telepítése
        try:
            cursor.execute(FUNCTION_SQL)
        except ProgrammingError:
            connection.rollback()
