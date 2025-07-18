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
