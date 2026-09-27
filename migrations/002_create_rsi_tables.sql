-- RSI Engine Database Schema
-- Recursive Self-Improvement system tables

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Improvement cycles
CREATE TABLE IF NOT EXISTS improvement_cycles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_number INTEGER NOT NULL,
    trigger_reason TEXT NOT NULL,
    trigger_type VARCHAR(50) NOT NULL, -- manual, automatic, scheduled, performance
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, running, completed, failed, cancelled
    auto_approve BOOLEAN DEFAULT false,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    failed_at TIMESTAMP NULL,
    error_message TEXT NULL,
    total_mutations INTEGER DEFAULT 0,
    successful_mutations INTEGER DEFAULT 0,
    failed_mutations INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mutations (code changes)
CREATE TABLE IF NOT EXISTS mutations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_id UUID NOT NULL REFERENCES improvement_cycles(id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    mutation_type VARCHAR(50) NOT NULL, -- addition, deletion, modification, refactoring
    old_content TEXT NULL,
    new_content TEXT NULL,
    diff_text TEXT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, approved, rejected, applied, failed
    risk_level VARCHAR(20) DEFAULT 'medium', -- low, medium, high, critical
    safety_check_passed BOOLEAN DEFAULT false,
    constitutional_check_passed BOOLEAN DEFAULT false,
    goal_drift_score FLOAT DEFAULT 0.0,
    approval_required BOOLEAN DEFAULT false,
    approved_by UUID NULL,
    approved_at TIMESTAMP NULL,
    applied_at TIMESTAMP NULL,
    rollback_available BOOLEAN DEFAULT false,
    rollback_id UUID NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Safety constraint violations
CREATE TABLE IF NOT EXISTS safety_violations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_id UUID NOT NULL REFERENCES improvement_cycles(id) ON DELETE CASCADE,
    mutation_id UUID NULL REFERENCES mutations(id) ON DELETE SET NULL,
    constraint_type VARCHAR(100) NOT NULL,
    constraint_id VARCHAR(100) NOT NULL,
    violation_severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    violation_description TEXT NOT NULL,
    blocked BOOLEAN DEFAULT true,
    resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Goal drift measurements
CREATE TABLE IF NOT EXISTS goal_drift_measurements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_id UUID NOT NULL REFERENCES improvement_cycles(id) ON DELETE CASCADE,
    measurement_type VARCHAR(50) NOT NULL, -- semantic, lexical, structural, distributional
    drift_score FLOAT NOT NULL,
    threshold FLOAT NOT NULL,
    is_violation BOOLEAN DEFAULT false,
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rollback history
CREATE TABLE IF NOT EXISTS rollback_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_id UUID NOT NULL REFERENCES improvement_cycles(id) ON DELETE CASCADE,
    mutation_id UUID NOT NULL REFERENCES mutations(id) ON DELETE CASCADE,
    rollback_reason TEXT NOT NULL,
    rollback_type VARCHAR(50) NOT NULL, -- manual, automatic, emergency
    restored_content TEXT NOT NULL,
    rollback_status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, completed, failed
    performed_by UUID NULL,
    performed_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System state snapshots
CREATE TABLE IF NOT EXISTS system_state_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_id UUID NOT NULL REFERENCES improvement_cycles(id) ON DELETE CASCADE,
    snapshot_type VARCHAR(50) NOT NULL, -- pre_cycle, post_cycle, checkpoint
    state_data JSONB NOT NULL,
    file_hashes JSONB DEFAULT '{}',
    database_schema_version VARCHAR(50) NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RSI configuration
CREATE TABLE IF NOT EXISTS rsi_configuration (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value JSONB NOT NULL,
    config_type VARCHAR(50) NOT NULL, -- safety, performance, resources, limits
    is_active BOOLEAN DEFAULT true,
    is_mutable BOOLEAN DEFAULT false, -- Whether RSI can modify this config
    modified_by_rsi BOOLEAN DEFAULT false,
    modified_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Improvement history log
CREATE TABLE IF NOT EXISTS improvement_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_id UUID NOT NULL REFERENCES improvement_cycles(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- started, completed, failed, blocked, approved
    event_description TEXT NOT NULL,
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_improvement_cycles_status ON improvement_cycles(status);
CREATE INDEX IF NOT EXISTS idx_improvement_cycles_number ON improvement_cycles(cycle_number);
CREATE INDEX IF NOT EXISTS idx_improvement_cycles_created ON improvement_cycles(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_mutations_cycle ON mutations(cycle_id);
CREATE INDEX IF NOT EXISTS idx_mutations_status ON mutations(status);
CREATE INDEX IF NOT EXISTS idx_mutations_risk ON mutations(risk_level);
CREATE INDEX IF NOT EXISTS idx_mutations_file ON mutations(file_path);

CREATE INDEX IF NOT EXISTS idx_safety_violations_cycle ON safety_violations(cycle_id);
CREATE INDEX IF NOT EXISTS idx_safety_violations_mutation ON safety_violations(mutation_id);
CREATE INDEX IF NOT EXISTS idx_safety_violations_type ON safety_violations(constraint_type);

CREATE INDEX IF NOT EXISTS idx_goal_drift_cycle ON goal_drift_measurements(cycle_id);
CREATE INDEX IF NOT EXISTS idx_goal_drift_type ON goal_drift_measurements(measurement_type);

CREATE INDEX IF NOT EXISTS idx_rollback_cycle ON rollback_history(cycle_id);
CREATE INDEX IF NOT EXISTS idx_rollback_mutation ON rollback_history(mutation_id);

CREATE INDEX IF NOT EXISTS idx_state_snapshots_cycle ON system_state_snapshots(cycle_id);
CREATE INDEX IF NOT EXISTS idx_state_snapshots_type ON system_state_snapshots(snapshot_type);

CREATE INDEX IF NOT EXISTS idx_rsi_config_active ON rsi_configuration(is_active);
CREATE INDEX IF NOT EXISTS idx_rsi_config_mutable ON rsi_configuration(is_mutable);

CREATE INDEX IF NOT EXISTS idx_improvement_history_cycle ON improvement_history(cycle_id);
CREATE INDEX IF NOT EXISTS idx_improvement_history_type ON improvement_history(event_type);
CREATE INDEX IF NOT EXISTS idx_improvement_history_created ON improvement_history(created_at DESC);

-- Trigger for updated_at
CREATE TRIGGER update_rsi_config_updated_at BEFORE UPDATE ON rsi_configuration
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to get current goal drift index
CREATE OR REPLACE FUNCTION get_current_goal_drift()
RETURNS TABLE (
    semantic_drift FLOAT,
    lexical_drift FLOAT,
    structural_drift FLOAT,
    distributional_drift FLOAT,
    total_gdi FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COALESCE(AVG(CASE WHEN measurement_type = 'semantic' THEN drift_score END), 0.0) as semantic_drift,
        COALESCE(AVG(CASE WHEN measurement_type = 'lexical' THEN drift_score END), 0.0) as lexical_drift,
        COALESCE(AVG(CASE WHEN measurement_type = 'structural' THEN drift_score END), 0.0) as structural_drift,
        COALESCE(AVG(CASE WHEN measurement_type = 'distributional' THEN drift_score END), 0.0) as distributional_drift,
        COALESCE(AVG(drift_score), 0.0) as total_gdi
    FROM goal_drift_measurements
    WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '24 hours';
END;
$$ LANGUAGE plpgsql;