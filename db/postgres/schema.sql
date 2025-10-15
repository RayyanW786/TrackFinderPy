DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
    CREATE TYPE user_role AS ENUM ('user', 'admin');
  END IF;
END$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ingest_status') THEN
    CREATE TYPE ingest_status AS ENUM ('queued','running','done','error');
  END IF;
END$$;


DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_enum e
    JOIN pg_type t ON t.oid = e.enumtypid
    WHERE t.typname = 'user_role' AND e.enumlabel = 'user'
  ) THEN
    ALTER TYPE user_role ADD VALUE 'user';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_enum e
    JOIN pg_type t ON t.oid = e.enumtypid
    WHERE t.typname = 'user_role' AND e.enumlabel = 'admin'
  ) THEN
    ALTER TYPE user_role ADD VALUE 'admin';
  END IF;
END$$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_enum e
    JOIN pg_type t ON t.oid = e.enumtypid
    WHERE t.typname = 'ingest_status' AND e.enumlabel = 'queued'
  ) THEN
    ALTER TYPE ingest_status ADD VALUE 'queued';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_enum e
    JOIN pg_type t ON t.oid = e.enumtypid
    WHERE t.typname = 'ingest_status' AND e.enumlabel = 'running'
  ) THEN
    ALTER TYPE ingest_status ADD VALUE 'running';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_enum e
    JOIN pg_type t ON t.oid = e.enumtypid
    WHERE t.typname = 'ingest_status' AND e.enumlabel = 'done'
  ) THEN
    ALTER TYPE ingest_status ADD VALUE 'done';
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_enum e
    JOIN pg_type t ON t.oid = e.enumtypid
    WHERE t.typname = 'ingest_status' AND e.enumlabel = 'error'
  ) THEN
    ALTER TYPE ingest_status ADD VALUE 'error';
  END IF;
END$$;


CREATE TABLE IF NOT EXISTS users(
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role user_role NOT NULL DEFAULT 'user',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS songs(
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title TEXT NOT NULL,
  artist TEXT NOT NULL,
  duration_sec INT,
  source_url TEXT,
  created_by BIGINT REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ingest_jobs(
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  song_id BIGINT REFERENCES songs(id) ON DELETE CASCADE,
  status ingest_status NOT NULL DEFAULT 'queued',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
