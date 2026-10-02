-- Memory Engine Database Schema
-- Core memory storage and retrieval system

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Memory entries table
CREATE TABLE IF NOT EXISTS memory_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    embedding vector(1536), -- For OpenAI embeddings, adjust size based on model
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    memory_type VARCHAR(50) DEFAULT 'episodic', -- episodic, semantic, procedural
    importance_score FLOAT DEFAULT 0.5,
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    user_id UUID NULL,
    session_id UUID NULL
);

-- Memory relationships table
CREATE TABLE IF NOT EXISTS memory_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_memory_id UUID NOT NULL REFERENCES memory_entries(id) ON DELETE CASCADE,
    target_memory_id UUID NOT NULL REFERENCES memory_entries(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL, -- related, causal, temporal, semantic
    strength FLOAT DEFAULT 0.5,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_memory_id, target_memory_id, relationship_type)
);

-- Memory context windows
CREATE TABLE IF NOT EXISTS memory_contexts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NULL,
    session_id UUID NULL,
    context_type VARCHAR(50) NOT NULL, -- conversation, task, project
    context_data JSONB NOT NULL,
    memory_ids UUID[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Memory search history
CREATE TABLE IF NOT EXISTS memory_search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NULL,
    query TEXT NOT NULL,
    query_embedding vector(1536),
    results_count INTEGER,
    search_time_ms FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_memory_entries_type ON memory_entries(memory_type);
CREATE INDEX IF NOT EXISTS idx_memory_entries_user ON memory_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_memory_entries_session ON memory_entries(session_id);
CREATE INDEX IF NOT EXISTS idx_memory_entries_created ON memory_entries(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memory_entries_importance ON memory_entries(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_memory_entries_expires ON memory_entries(expires_at) WHERE expires_at IS NOT NULL;

-- Vector similarity search index
CREATE INDEX IF NOT EXISTS idx_memory_entries_embedding ON memory_entries USING ivfflat (embedding vector_cosine_ops);

-- Relationship indexes
CREATE INDEX IF NOT EXISTS idx_memory_relationships_source ON memory_relationships(source_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_relationships_target ON memory_relationships(target_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_relationships_type ON memory_relationships(relationship_type);

-- Context indexes
CREATE INDEX IF NOT EXISTS idx_memory_contexts_user ON memory_contexts(user_id);
CREATE INDEX IF NOT EXISTS idx_memory_contexts_session ON memory_contexts(session_id);
CREATE INDEX IF NOT EXISTS idx_memory_contexts_type ON memory_contexts(context_type);

-- Search history indexes
CREATE INDEX IF NOT EXISTS idx_memory_search_history_user ON memory_search_history(user_id);
CREATE INDEX IF NOT EXISTS idx_memory_search_history_created ON memory_search_history(created_at DESC);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_memory_entries_updated_at BEFORE UPDATE ON memory_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_memory_contexts_updated_at BEFORE UPDATE ON memory_contexts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to clean expired memories
CREATE OR REPLACE FUNCTION clean_expired_memories()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM memory_entries
    WHERE expires_at IS NOT NULL AND expires_at < CURRENT_TIMESTAMP;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;