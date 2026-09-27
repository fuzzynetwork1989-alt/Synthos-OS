-- Workflow Engine Database Schema
-- Workflow orchestration and automation

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Workflow definitions
CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) UNIQUE NOT NULL,
    display_name VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL, -- automation, data_processing, ai_pipeline, monitoring
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, deprecated, disabled
    is_public BOOLEAN DEFAULT false,
    owner_id UUID NULL,
    workflow_definition JSONB NOT NULL,
    input_schema JSONB NOT NULL,
    output_schema JSONB NOT NULL,
    timeout_seconds INTEGER DEFAULT 300,
    retry_policy JSONB DEFAULT '{}',
    error_handling JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflow executions
CREATE TABLE IF NOT EXISTS workflow_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    user_id UUID NULL,
    session_id UUID NULL,
    execution_type VARCHAR(50) NOT NULL, -- manual, scheduled, triggered, api
    input_data JSONB NOT NULL,
    output_data JSONB NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, running, completed, failed, cancelled, timeout
    current_step VARCHAR(100) NULL,
    total_steps INTEGER NULL,
    completed_steps INTEGER DEFAULT 0,
    error_message TEXT NULL,
    execution_time_ms INTEGER NULL,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    timeout_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflow steps
CREATE TABLE IF NOT EXISTS workflow_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id UUID NOT NULL REFERENCES workflow_executions(id) ON DELETE CASCADE,
    step_id VARCHAR(100) NOT NULL,
    step_name VARCHAR(200) NOT NULL,
    step_type VARCHAR(50) NOT NULL, -- task, condition, parallel, loop, subworkflow
    step_definition JSONB NOT NULL,
    input_data JSONB NULL,
    output_data JSONB NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, running, completed, failed, skipped, cancelled
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    error_message TEXT NULL,
    execution_time_ms INTEGER NULL,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Task definitions (atomic workflow units)
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) UNIQUE NOT NULL,
    display_name VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    task_type VARCHAR(50) NOT NULL, -- python_script, shell_command, api_call, tool_execution, data_transform
    implementation JSONB NOT NULL,
    timeout_seconds INTEGER DEFAULT 60,
    retry_policy JSONB DEFAULT '{}',
    resource_requirements JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Task executions
CREATE TABLE IF NOT EXISTS task_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    workflow_step_id UUID NULL REFERENCES workflow_steps(id) ON DELETE SET NULL,
    input_data JSONB NOT NULL,
    output_data JSONB NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, running, completed, failed, timeout, cancelled
    error_message TEXT NULL,
    exit_code INTEGER NULL,
    execution_time_ms INTEGER NULL,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflow schedules
CREATE TABLE IF NOT EXISTS workflow_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    schedule_name VARCHAR(200) NOT NULL,
    schedule_type VARCHAR(50) NOT NULL, -- cron, interval, event_based
    schedule_expression VARCHAR(200) NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',
    is_active BOOLEAN DEFAULT true,
    last_run_at TIMESTAMP NULL,
    next_run_at TIMESTAMP NULL,
    run_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    input_template JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflow triggers
CREATE TABLE IF NOT EXISTS workflow_triggers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    trigger_type VARCHAR(50) NOT NULL, -- web, event, time, condition
    trigger_config JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    trigger_count INTEGER DEFAULT 0,
    last_triggered_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflow variables
CREATE TABLE IF NOT EXISTS workflow_variables (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    variable_name VARCHAR(100) NOT NULL,
    variable_value JSONB NOT NULL,
    variable_type VARCHAR(50) NOT NULL, -- string, number, boolean, json, array
    is_secret BOOLEAN DEFAULT false,
    is_global BOOLEAN DEFAULT false,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(workflow_id, variable_name)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_workflows_name ON workflows(name);
CREATE INDEX IF NOT EXISTS idx_workflows_category ON workflows(category);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
CREATE INDEX IF NOT EXISTS idx_workflows_owner ON workflows(owner_id);

CREATE INDEX IF NOT EXISTS idx_workflow_executions_workflow ON workflow_executions(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_user ON workflow_executions(user_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_type ON workflow_executions(execution_type);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_created ON workflow_executions(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_workflow_steps_execution ON workflow_steps(execution_id);
CREATE INDEX IF NOT EXISTS idx_workflow_steps_status ON workflow_steps(status);
CREATE INDEX IF NOT EXISTS idx_workflow_steps_step_id ON workflow_steps(step_id);

CREATE INDEX IF NOT EXISTS idx_tasks_name ON tasks(name);
CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(task_type);

CREATE INDEX IF NOT EXISTS idx_task_executions_task ON task_executions(task_id);
CREATE INDEX IF NOT EXISTS idx_task_executions_step ON task_executions(workflow_step_id);
CREATE INDEX IF NOT EXISTS idx_task_executions_status ON task_executions(status);

CREATE INDEX IF NOT EXISTS idx_workflow_schedules_workflow ON workflow_schedules(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_schedules_active ON workflow_schedules(is_active);
CREATE INDEX IF NOT EXISTS idx_workflow_schedules_next_run ON workflow_schedules(next_run_at);

CREATE INDEX IF NOT EXISTS idx_workflow_triggers_workflow ON workflow_triggers(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_triggers_type ON workflow_triggers(trigger_type);
CREATE INDEX IF NOT EXISTS idx_workflow_triggers_active ON workflow_triggers(is_active);

CREATE INDEX IF NOT EXISTS idx_workflow_variables_workflow ON workflow_variables(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_variables_name ON workflow_variables(variable_name);
CREATE INDEX IF NOT EXISTS idx_workflow_variables_global ON workflow_variables(is_global);

-- Triggers for updated_at
CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflow_schedules_updated_at BEFORE UPDATE ON workflow_schedules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflow_triggers_updated_at BEFORE UPDATE ON workflow_triggers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflow_variables_updated_at BEFORE UPDATE ON workflow_variables
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to get workflows ready for execution
CREATE OR REPLACE FUNCTION get_ready_workflows()
RETURNS TABLE (
    workflow_id UUID,
    workflow_name VARCHAR(200),
    schedule_id UUID,
    input_template JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ws.workflow_id,
        w.name as workflow_name,
        ws.id as schedule_id,
        ws.input_template
    FROM workflow_schedules ws
    JOIN workflows w ON ws.workflow_id = w.id
    WHERE ws.is_active = true
      AND w.status = 'active'
      AND ws.next_run_at <= CURRENT_TIMESTAMP
    ORDER BY ws.next_run_at ASC;
END;
$$ LANGUAGE plpgsql;