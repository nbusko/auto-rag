CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ---------------- users & auth ------------------
CREATE TABLE IF NOT EXISTS users
(
    user_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name    text      NOT NULL,
    email        text      NOT NULL UNIQUE,
    organization text,
    rag_id       uuid      NOT NULL,
    role         text      NOT NULL DEFAULT 'owner'
);

CREATE TABLE IF NOT EXISTS user_credentials
(
    user_id       uuid PRIMARY KEY REFERENCES users (user_id) ON DELETE CASCADE,
    password_hash text NOT NULL
);

-- --------------- RAG & chat ---------------------
CREATE TABLE IF NOT EXISTS chat_history
(
    rag_id       uuid NOT NULL,
    message_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    message_type text NOT NULL CHECK (message_type IN ('assistant', 'user')),
    user_id      uuid,
    text         text NOT NULL
);

CREATE TABLE IF NOT EXISTS rag_settings
(
    rag_id              uuid PRIMARY KEY,
    prompt              text    NOT NULL,     -- prompt_generation
    document_id         uuid,
    top_k               int     NOT NULL DEFAULT 3,
    temperature         numeric NOT NULL DEFAULT 0.7,
    threshold           numeric NOT NULL DEFAULT 0.0,

    llm_model           text    NOT NULL DEFAULT 'gpt-4o-mini',

    prompt_retrieve     text,
    prompt_augmentation text,
    prompt_split        text,
    prompt_table        text,

    split_method        text    NOT NULL DEFAULT 'batch',     -- 'batch' | 'llm'
    batch_size          int     NOT NULL DEFAULT 1000
);

-- ---------- NEW : public share links ------------
CREATE TABLE IF NOT EXISTS share_links
(
    token      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rag_id     uuid NOT NULL,
    enabled    boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document_embeddings
(
    document_id uuid NOT NULL,
    chunk_index int  NOT NULL,
    content     text NOT NULL,
    embedding   vector(312),
    CONSTRAINT pk_document_embeddings PRIMARY KEY (document_id, chunk_index)
);