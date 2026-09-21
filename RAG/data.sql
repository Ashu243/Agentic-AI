CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    source TEXT,
    page INTEGER,
    section TEXT,
    embedding VECTOR(1536)
);

CREATE TABLE documents_local (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    source TEXT,
    page INTEGER,
    section TEXT,
    embedding VECTOR(384)
);

CREATE INDEX documents_local_embedding_hnsw
ON documents_local
USING hnsw (embedding vector_cosine_ops);

CREATE INDEX documents_embedding_hnsw
ON documents
USING hnsw (embedding vector_cosine_ops); -- creating an HNSW index