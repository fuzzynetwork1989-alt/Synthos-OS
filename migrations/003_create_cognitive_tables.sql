-- Cognitive Engine Database Schema
-- Reasoning, planning, and context management

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Reasoning sessions
CREATE TABLE IF NOT EXISTS reasoning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NULL,
    session_type VARCHAR(50) NOT NULL, -- chain_of_thought, tree_of_thoughts, analogical, causal
    query TEXT NOT NULL,
    context TEXT NULL,
    reasoning_method VARCHAR(50) NOT NULL,
    max_steps INTEGER DEFAULT 5,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, processing, completed, failed
    result TEXT NULL,
    confidence_score FLOAT NULL,
    processing_time_ms INTEGER NULL,
    token_usage INTEGER NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL
);

-- Reasoning steps
CREATE TABLE IF NOT EXISTS reasoning_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES reasoning_sessions(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    step_type VARCHAR(50) NOT NULL, -- analysis, inference, synthesis, validation
    step_description TEXT NOT NULL,
    step_result TEXT NULL,
    confidence FLOAT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Planning sessions
CREATE TABLE IF NOT EXISTS planning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NULL,
    goal TEXT NOT NULL,
    current_state JSONB NOT NULL,
    target_state JSONB NULL,
    constraints TEXT[] DEFAULT '{}',
    planning_algorithm VARCHAR(50) NOT NULL, -- forward_chaining, backward_chaining, hierarchical
    max_depth INTEGER DEFAULT 5,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, processing, completed, failed
    plan JSONB NULL,
    estimated_time TEXT NULL,
    resource_requirements JSONB NULL,
    confidence_score FLOAT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL
);

-- Plan steps
CREATE TABLE IF NOT EXISTS plan_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES planning_sessions(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    action_description TEXT NOT NULL,
    dependencies INTEGER[] DEFAULT '{}', -- Array of step numbers this depends on
    estimated_duration TEXT NULL,
    required_resources JSONB NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, in_progress, completed, failed, skipped
    result JSONB NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL
);

-- Context windows
CREATE TABLE IF NOT EXISTS context_windows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NULL,
    session_id UUID NULL,
    context_type VARCHAR(50) NOT NULL, -- conversation, task, project, system
    context_data JSONB NOT NULL,
    max_length INTEGER DEFAULT 10,
    current_length INTEGER DEFAULT 0,
    priority FLOAT DEFAULT 0.5,
    expires_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Context entries
CREATE TABLE IF NOT EXISTS context_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    window_id UUID NOT NULL REFERENCES context_windows(id) ON DELETE CASCADE,
    entry_type VARCHAR(50) NOT NULL, -- message, memory, system_state, tool_result
    entry_data JSONB NOT NULL,
    importance FLOAT DEFAULT 0.5,
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge base
CREATE TABLE IF NOT EXISTS knowledge_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    knowledge_type VARCHAR(50) NOT NULL, -- fact, rule, procedure, concept
    category VARCHAR(100) NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source TEXT NULL,
    confidence FLOAT DEFAULT 1.0,
    validity_period_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validity_period_end TIMESTAMP NULL,
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge relationships
CREATE TABLE IF NOT EXISTS knowledge_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID NOT NULL REFERENCES knowledge_entries(id) ON DELETE CASCADE,
    target_id UUID NOT NULL REFERENCES knowledge_entries(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL, -- related_to, instance_of, part_of, causes, enables
    strength FLOAT DEFAULT 0.5,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, target_id, relationship_type)
);

-- Cognitive performance metrics
CREATE TABLE IF NOT EXISTS cognitive_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_type VARCHAR(50) NOT NULL, -- reasoning_accuracy, planning_efficiency, context_retrieval
    metric_value FLOAT NOT NULL,
    metric_unit VARCHAR(20) NULL,
    session_id UUID NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_reasoning_sessions_user ON reasoning_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_reasoning_sessions_status ON reasoning_sessions(status);
CREATE INDEX IF NOT EXISTS idx_reasoning_sessions_type ON reasoning_sessions(session_type);
CREATE INDEX IF NOT EXISTS idx_reasoning_sessions_created ON reasoning_sessions(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_reasoning_steps_session ON reasoning_steps(session_id);
CREATE INDEX IF NOT EXISTS idx_reasoning_steps_number ON reasoning_steps(step_number);

CREATE INDEX IF NOT EXISTS idx_planning_sessions_user ON planning_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_planning_sessions_status ON planning_sessions(status);
CREATE INDEX IF NOT EXISTS idx_planning_sessions_algorithm ON planning_sessions(planning_algorithm);

CREATE INDEX IF NOT EXISTS idx_plan_steps_session ON plan_steps(session_id);
CREATE INDEX IF NOT EXISTS idx_plan_steps_number ON plan_steps(step_number);
CREATE INDEX IF NOT EXISTS idx_plan_steps_status ON plan_steps(status);

CREATE INDEX IF NOT EXISTS idx_context_windows_user ON context_windows(user_id);
CREATE INDEX IF NOT EXISTS idx_context_windows_session ON context_windows(session_id);
CREATE INDEX IF NOT EXISTS idx_context_windows_type ON context_windows(context_type);
CREATE INDEX IF NOT EXISTS idx_context_windows_priority ON context_windows(priority DESC);

CREATE INDEX IF NOT EXISTS idx_context_entries_window ON context_entries(window_id);
CREATE INDEX IF NOT EXISTS idx_context_entries_type ON context_entries(entry_type);
CREATE INDEX IF NOT EXISTS idx_context_entries_importance ON context_entries(importance DESC);

CREATE INDEX IF NOT EXISTS idx_knowledge_entries_type ON knowledge_entries(knowledge_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_entries_category ON knowledge_entries(category);
CREATE INDEX IF NOT EXISTS idx_knowledge_entries_tags ON knowledge_entries USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_knowledge_entries_created ON knowledge_entries(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_knowledge_relationships_source ON knowledge_relationships(source_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_relationships_target ON knowledge_relationships(target_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_relationships_type ON knowledge_relationships(relationship_type);

CREATE INDEX IF NOT EXISTS idx_cognitive_metrics_type ON cognitive_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_cognitive_metrics_session ON cognitive_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_cognitive_metrics_created ON cognitive_metrics(created_at DESC);

-- Triggers for updated_at
CREATE TRIGGER update_context_windows_updated_at BEFORE UPDATE ON context_windows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_knowledge_entries_updated_at BEFORE UPDATE ON knowledge_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to clean expired context windows
CREATE OR REPLACE FUNCTION clean_expired_contexts()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM context_windows
    WHERE expires_at IS NOT NULL AND expires_at < CURRENT_TIMESTAMP;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;