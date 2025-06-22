-- Включение расширения pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Создание таблицы History
CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    chat_id VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    message_role VARCHAR(50) NOT NULL CHECK (message_role IN ('assistant', 'user')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chat_id, message_id)
);

-- Создание таблицы Params
CREATE TABLE IF NOT EXISTS params (
    id SERIAL PRIMARY KEY,
    chat_id VARCHAR(255) NOT NULL UNIQUE,
    prompt_id VARCHAR(255) NOT NULL,
    document_id VARCHAR(255) NOT NULL,
    top_k INTEGER DEFAULT 5,
    temperature FLOAT DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 1000,
    model_name VARCHAR(100) DEFAULT 'gpt-3.5-turbo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы Docs
CREATE TABLE IF NOT EXISTS docs (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(255) NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(312), -- Размерность для rubert-tiny-turbo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, chunk_index)
);

-- Создание индексов для оптимизации
CREATE INDEX IF NOT EXISTS idx_history_chat_id ON history(chat_id);
CREATE INDEX IF NOT EXISTS idx_params_chat_id ON params(chat_id);
CREATE INDEX IF NOT EXISTS idx_docs_document_id ON docs(document_id);
CREATE INDEX IF NOT EXISTS idx_docs_embedding ON docs USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Создание функции для обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Создание триггера для автоматического обновления updated_at
CREATE TRIGGER update_params_updated_at BEFORE UPDATE ON params
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();