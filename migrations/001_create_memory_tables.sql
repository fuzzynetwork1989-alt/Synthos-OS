-- Create memory tables for Synthos-OS

-- Memory entries table
CREATE TABLE IF NOT EXISTS memory_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ttl INTEGER
);

-- Create indexes for better search performance
CREATE INDEX idx_memory_entries_content ON memory_entries USING gin(to_tsvector('english', content));
CREATE INDEX idx_memory_entries_tags ON memory_entries USING gin(tags);
CREATE INDEX idx_memory_entries_created_at ON memory_entries(created_at DESC);

-- Create table for memory statistics
CREATE TABLE IF NOT EXISTS memory_stats (
    id SERIAL PRIMARY KEY,
    total_entries INTEGER DEFAULT 0,
    total_size_bytes BIGINT DEFAULT 0,
    last_cleanup TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert initial stats
INSERT INTO memory_stats (total_entries, total_size_bytes) 
VALUES (0, 0) 
ON CONFLICT DO NOTHING;

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for memory_entries
CREATE TRIGGER update_memory_entries_updated_at 
    BEFORE UPDATE ON memory_entries 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();