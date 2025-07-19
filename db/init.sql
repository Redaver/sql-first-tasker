CREATE TABLE "user" (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT
);

CREATE TABLE project (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  owner_id BIGINT REFERENCES "user"(id)
);

CREATE TABLE task (
  id BIGSERIAL PRIMARY KEY,
  project_id BIGINT REFERENCES project(id),
  title TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'todo',
  priority SMALLINT DEFAULT 3,
  due_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE comment (
  id BIGSERIAL PRIMARY KEY,
  task_id BIGINT REFERENCES task(id),
  author_id BIGINT REFERENCES "user"(id),
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- eseménynapló tábla
CREATE TABLE IF NOT EXISTS task_event (
  id BIGSERIAL PRIMARY KEY,
  task_id BIGINT REFERENCES task(id),
  event TEXT,
  happened_at TIMESTAMPTZ DEFAULT now()
);

-- státusz‑váltó függvény
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

