-- Tool Execution Engine Database Schema
-- Tool management, execution, and sandboxing

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tool registry
CREATE TABLE IF NOT EXISTS tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL, -- file, code, system, network, database, ai
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, deprecated, disabled
    is_sandboxed BOOLEAN DEFAULT true,
    requires_auth BOOLEAN DEFAULT false,
    required_permissions TEXT[] DEFAULT '{}',
    execution_timeout INTEGER DEFAULT 30, -- seconds
    max_memory_mb INTEGER DEFAULT 512,
    resource_requirements JSONB DEFAULT '{}',
    input_schema JSONB NOT NULL,
    output_schema JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tool executions
CREATE TABLE IF NOT EXISTS tool_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    user_id UUID NULL,
    session_id UUID NULL,
    execution_type VARCHAR(50) NOT NULL, -- synchronous, asynchronous, streaming
    input_parameters JSONB NOT NULL,
    output_result JSONB NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, running, completed, failed, timeout, cancelled
    error_message TEXT NULL,
    exit_code INTEGER NULL,
    execution_time_ms INTEGER NULL,
    memory_used_mb INTEGER NULL,
    cpu_used_percent FLOAT NULL,
    sandbox_id UUID NULL,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    timeout_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Execution logs
CREATE TABLE IF NOT EXISTS execution_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id UUID NOT NULL REFERENCES tool_executions(id) ON DELETE CASCADE,
    log_level VARCHAR(20) NOT NULL, -- debug, info, warning, error, critical
    log_message TEXT NOT NULL,
    log_data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sandbox sessions
CREATE TABLE IF NOT EXISTS sandbox_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id UUID NULL REFERENCES tool_executions(id) ON DELETE SET NULL,
    sandbox_type VARCHAR(50) NOT NULL, -- container, vm, process, restricted
    resource_limits JSONB NOT NULL,
    network_policy VARCHAR(50) DEFAULT 'restricted', -- none, restricted, full
    file_system_policy VARCHAR(50) DEFAULT 'isolated', -- isolated, restricted, full
    status VARCHAR(50) NOT NULL DEFAULT 'created', -- created, running, stopped, failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    stopped_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}'
);

-- Tool permissions
CREATE TABLE IF NOT EXISTS tool_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    user_id UUID NULL,
    role_id UUID NULL,
    permission_type VARCHAR(50) NOT NULL, -- execute, configure, view_logs, manage
    is_granted BOOLEAN DEFAULT false,
    granted_by UUID NULL,
    granted_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tool_id, user_id, permission_type),
    UNIQUE(tool_id, role_id, permission_type)
);

-- Tool dependencies
CREATE TABLE IF NOT EXISTS tool_dependencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    dependency_type VARCHAR(50) NOT NULL, -- system_package, python_package, npm_package, system_service
    dependency_name VARCHAR(200) NOT NULL,
    dependency_version VARCHAR(100) NULL,
    is_required BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tool_id, dependency_type, dependency_name)
);

-- Tool usage statistics
CREATE TABLE IF NOT EXISTS tool_usage_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    stat_type VARCHAR(50) NOT NULL, -- daily, weekly, monthly
    execution_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    avg_execution_time_ms FLOAT NULL,
    avg_memory_used_mb FLOAT NULL,
    last_execution_at TIMESTAMP NULL,
    stat_date DATE NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tool_id, stat_type, stat_date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tools_name ON tools(name);
CREATE INDEX IF NOT EXISTS idx_tools_category ON tools(category);
CREATE INDEX IF NOT EXISTS idx_tools_status ON tools(status);
CREATE INDEX IF NOT EXISTS idx_tools_sandboxed ON tools(is_sandboxed);

CREATE INDEX IF NOT EXISTS idx_tool_executions_tool ON tool_executions(tool_id);
CREATE INDEX IF NOT EXISTS idx_tool_executions_user ON tool_executions(user_id);
CREATE INDEX IF NOT EXISTS idx_tool_executions_session ON tool_executions(session_id);
CREATE INDEX IF NOT EXISTS idx_tool_executions_status ON tool_executions(status);
CREATE INDEX IF NOT EXISTS idx_tool_executions_created ON tool_executions(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_execution_logs_execution ON execution_logs(execution_id);
CREATE INDEX IF NOT EXISTS idx_execution_logs_level ON execution_logs(log_level);
CREATE INDEX IF NOT EXISTS idx_execution_logs_timestamp ON execution_logs(timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_sandbox_sessions_execution ON sandbox_sessions(execution_id);
CREATE INDEX IF NOT EXISTS idx_sandbox_sessions_status ON sandbox_sessions(status);
CREATE INDEX IF NOT EXISTS idx_sandbox_sessions_type ON sandbox_sessions(sandbox_type);

CREATE INDEX IF NOT EXISTS idx_tool_permissions_tool ON tool_permissions(tool_id);
CREATE INDEX IF NOT EXISTS idx_tool_permissions_user ON tool_permissions(user_id);
CREATE INDEX IF NOT EXISTS idx_tool_permissions_role ON tool_permissions(role_id);
CREATE INDEX IF NOT EXISTS idx_tool_permissions_granted ON tool_permissions(is_granted);

CREATE INDEX IF NOT EXISTS idx_tool_dependencies_tool ON tool_dependencies(tool_id);
CREATE INDEX IF NOT EXISTS idx_tool_dependencies_type ON tool_dependencies(dependency_type);

CREATE INDEX IF NOT EXISTS idx_tool_usage_stats_tool ON tool_usage_stats(tool_id);
CREATE INDEX IF NOT EXISTS idx_tool_usage_stats_type ON tool_usage_stats(stat_type);
CREATE INDEX IF NOT EXISTS idx_tool_usage_stats_date ON tool_usage_stats(stat_date);

-- Triggers for updated_at
CREATE TRIGGER update_tools_updated_at BEFORE UPDATE ON tools
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tool_usage_stats_updated_at BEFORE UPDATE ON tool_usage_stats
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update tool usage statistics
CREATE OR REPLACE FUNCTION update_tool_usage_stats()
RETURNS VOID AS $$
BEGIN
    -- Update daily stats
    INSERT INTO tool_usage_stats (tool_id, stat_type, execution_count, success_count, failure_count, avg_execution_time_ms, avg_memory_used_mb, last_execution_at, stat_date)
    SELECT 
        tool_id,
        'daily',
        COUNT(*),
        COUNT(*) FILTER (WHERE status = 'completed'),
        COUNT(*) FILTER (WHERE status IN ('failed', 'timeout')),
        AVG(execution_time_ms) FILTER (WHERE execution_time_ms IS NOT NULL),
        AVG(memory_used_mb) FILTER (WHERE memory_used_mb IS NOT NULL),
        MAX(completed_at) FILTER (WHERE completed_at IS NOT NULL),
        CURRENT_DATE
    FROM tool_executions
    WHERE DATE(created_at) = CURRENT_DATE
    GROUP BY tool_id
    ON CONFLICT (tool_id, stat_type, stat_date) 
    DO UPDATE SET
        execution_count = EXCLUDED.execution_count,
        success_count = EXCLUDED.success_count,
        failure_count = EXCLUDED.failure_count,
        avg_execution_time_ms = EXCLUDED.avg_execution_time_ms,
        avg_memory_used_mb = EXCLUDED.avg_memory_used_mb,
        last_execution_at = EXCLUDED.last_execution_at,
        updated_at = CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;