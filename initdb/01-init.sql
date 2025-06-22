CREATE EXTENSION IF NOT EXISTS "pgcrypto"; 
CREATE EXTENSION IF NOT EXISTS "pgvector";

CREATE TABLE IF NOT EXISTS chat_history
(
    rag_id       uuid NOT NULL,
    message_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    message_type text NOT NULL CHECK (message_type IN ('assistant', 'user')),
    text         text NOT NULL
);

CREATE TABLE IF NOT EXISTS rag_settings
(
    rag_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt      text    NOT NULL,
    document_id uuid
);

CREATE TABLE IF NOT EXISTS document_embeddings
(
    document_id uuid NOT NULL,
    chunk_index int  NOT NULL,
    content     text NOT NULL,
    embedding   vector(1536),
    CONSTRAINT pk_document_embeddings PRIMARY KEY (document_id, chunk_index)
);
