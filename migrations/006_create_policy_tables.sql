-- Policy Engine Database Schema
-- Governance, policy enforcement, and access control

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Policies
CREATE TABLE IF NOT EXISTS policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) UNIQUE NOT NULL,
    display_name VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    policy_type VARCHAR(50) NOT NULL, -- access_control, data_privacy, resource_limit, safety, compliance
    category VARCHAR(50) NOT NULL, -- security, privacy, governance, operational
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, deprecated, disabled
    is_enforced BOOLEAN DEFAULT true,
    priority INTEGER DEFAULT 5, -- 1-10, higher = more important
    policy_rules JSONB NOT NULL,
    conditions JSONB DEFAULT '{}',
    actions JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Policy evaluations
CREATE TABLE IF NOT EXISTS policy_evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID NOT NULL REFERENCES policies(id) ON DELETE CASCADE,
    user_id UUID NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID NULL,
    action_type VARCHAR(50) NOT NULL, -- read, write, execute, delete, admin
    context_data JSONB NOT NULL,
    evaluation_result VARCHAR(20) NOT NULL, -- allowed, denied, conditional
    denial_reason TEXT NULL,
    conditions_matched TEXT[] DEFAULT '{}',
    evaluation_time_ms INTEGER NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Policy violations
CREATE TABLE IF NOT EXISTS policy_violations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID NOT NULL REFERENCES policies(id) ON DELETE CASCADE,
    evaluation_id UUID NULL REFERENCES policy_evaluations(id) ON DELETE SET NULL,
    user_id UUID NULL,
    violation_type VARCHAR(50) NOT NULL, -- access_denied, resource_limit, safety_breach, compliance_failure
    violation_severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    violation_description TEXT NOT NULL,
    was_blocked BOOLEAN DEFAULT true,
    remediation_action TEXT NULL,
    remediation_status VARCHAR(50) DEFAULT 'none', -- none, attempted, completed, failed
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL
);

-- Roles
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    role_type VARCHAR(50) NOT NULL, -- system, user, service, admin
    permissions JSONB NOT NULL,
    is_system_role BOOLEAN DEFAULT false,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User roles
CREATE TABLE IF NOT EXISTS user_roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    assigned_by UUID NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, role_id)
);

-- Resource access control
CREATE TABLE IF NOT EXISTS resource_acl (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID NOT NULL,
    access_type VARCHAR(50) NOT NULL, -- read, write, execute, admin, owner
    principal_type VARCHAR(50) NOT NULL, -- user, role, service, public
    principal_id UUID NULL,
    conditions JSONB DEFAULT '{}',
    is_granted BOOLEAN DEFAULT true,
    granted_by UUID NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(resource_type, resource_id, principal_type, principal_id, access_type)
);

-- Audit logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NULL,
    service_id VARCHAR(100) NULL,
    action_type VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NULL,
    resource_id UUID NULL,
    action_data JSONB DEFAULT '{}',
    result VARCHAR(50) NOT NULL, -- success, failure, partial
    error_message TEXT NULL,
    ip_address INET NULL,
    user_agent TEXT NULL,
    session_id UUID NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compliance rules
CREATE TABLE IF NOT EXISTS compliance_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_name VARCHAR(200) UNIQUE NOT NULL,
    compliance_type VARCHAR(50) NOT NULL, -- gdpr, hipaa, soc2, pci_dss, custom
    description TEXT NOT NULL,
    rule_definition JSONB NOT NULL,
    severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    is_active BOOLEAN DEFAULT true,
    check_frequency VARCHAR(50) DEFAULT 'daily', -- realtime, hourly, daily, weekly
    last_checked_at TIMESTAMP NULL,
    last_compliance_status VARCHAR(50) NULL, -- compliant, non_compliant, unknown
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compliance checks
CREATE TABLE IF NOT EXISTS compliance_checks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID NOT NULL REFERENCES compliance_rules(id) ON DELETE CASCADE,
    check_status VARCHAR(50) NOT NULL, -- passed, failed, warning, error
    check_details JSONB NOT NULL,
    violations_detected INTEGER DEFAULT 0,
    remediation_required BOOLEAN DEFAULT false,
    checked_by UUID NULL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_policies_name ON policies(name);
CREATE INDEX IF NOT EXISTS idx_policies_type ON policies(policy_type);
CREATE INDEX IF NOT EXISTS idx_policies_category ON policies(category);
CREATE INDEX IF NOT EXISTS idx_policies_status ON policies(status);
CREATE INDEX IF NOT EXISTS idx_policies_priority ON policies(priority DESC);

CREATE INDEX IF NOT EXISTS idx_policy_evaluations_policy ON policy_evaluations(policy_id);
CREATE INDEX IF NOT EXISTS idx_policy_evaluations_user ON policy_evaluations(user_id);
CREATE INDEX IF NOT EXISTS idx_policy_evaluations_resource ON policy_evaluations(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_policy_evaluations_result ON policy_evaluations(evaluation_result);
CREATE INDEX IF NOT EXISTS idx_policy_evaluations_created ON policy_evaluations(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_policy_violations_policy ON policy_violations(policy_id);
CREATE INDEX IF NOT EXISTS idx_policy_violations_user ON policy_violations(user_id);
CREATE INDEX IF NOT EXISTS idx_policy_violations_type ON policy_violations(violation_type);
CREATE INDEX IF NOT EXISTS idx_policy_violations_severity ON policy_violations(violation_severity);
CREATE INDEX IF NOT EXISTS idx_policy_violations_resolved ON policy_violations(resolved_at);

CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(name);
CREATE INDEX IF NOT EXISTS idx_roles_type ON roles(role_type);

CREATE INDEX IF NOT EXISTS idx_user_roles_user ON user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role ON user_roles(role_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_active ON user_roles(is_active);
CREATE INDEX IF NOT EXISTS idx_user_roles_expires ON user_roles(expires_at) WHERE expires_at IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_resource_acl_resource ON resource_acl(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_resource_acl_principal ON resource_acl(principal_type, principal_id);
CREATE INDEX IF NOT EXISTS idx_resource_acl_granted ON resource_acl(is_granted);
CREATE INDEX IF NOT EXISTS idx_resource_acl_expires ON resource_acl(expires_at) WHERE expires_at IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_service ON audit_logs(service_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_result ON audit_logs(result);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created ON audit_logs(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_compliance_rules_type ON compliance_rules(compliance_type);
CREATE INDEX IF NOT EXISTS idx_compliance_rules_active ON compliance_rules(is_active);
CREATE INDEX IF NOT EXISTS idx_compliance_rules_severity ON compliance_rules(severity);

CREATE INDEX IF NOT EXISTS idx_compliance_checks_rule ON compliance_checks(rule_id);
CREATE INDEX IF NOT EXISTS idx_compliance_checks_status ON compliance_checks(check_status);
CREATE INDEX IF NOT EXISTS idx_compliance_checks_checked ON compliance_checks(checked_at DESC);

-- Triggers for updated_at
CREATE TRIGGER update_policies_updated_at BEFORE UPDATE ON policies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_roles_updated_at BEFORE UPDATE ON roles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_compliance_rules_updated_at BEFORE UPDATE ON compliance_rules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to check user permissions
CREATE OR REPLACE FUNCTION check_user_permission(
    p_user_id UUID,
    p_resource_type VARCHAR(100),
    p_resource_id UUID,
    p_action_type VARCHAR(50)
) RETURNS BOOLEAN AS $$
DECLARE
    has_permission BOOLEAN := false;
BEGIN
    -- Check direct user access
    SELECT EXISTS (
        SELECT 1 FROM resource_acl
        WHERE resource_type = p_resource_type
        AND resource_id = p_resource_id
        AND principal_type = 'user'
        AND principal_id = p_user_id
        AND access_type = p_action_type
        AND is_granted = true
        AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
    ) INTO has_permission;
    
    -- If no direct permission, check role-based permissions
    IF NOT has_permission THEN
        SELECT EXISTS (
            SELECT 1 FROM resource_acl ra
            JOIN user_roles ur ON ra.principal_id = ur.role_id
            WHERE ra.resource_type = p_resource_type
            AND ra.resource_id = p_resource_id
            AND ra.principal_type = 'role'
            AND ur.user_id = p_user_id
            AND ra.access_type = p_action_type
            AND ra.is_granted = true
            AND ur.is_active = true
            AND (ur.expires_at IS NULL OR ur.expires_at > CURRENT_TIMESTAMP)
            AND (ra.expires_at IS NULL OR ra.expires_at > CURRENT_TIMESTAMP)
        ) INTO has_permission;
    END IF;
    
    -- If still no permission, check public access
    IF NOT has_permission THEN
        SELECT EXISTS (
            SELECT 1 FROM resource_acl
            WHERE resource_type = p_resource_type
            AND resource_id = p_resource_id
            AND principal_type = 'public'
            AND access_type = p_action_type
            AND is_granted = true
            AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
        ) INTO has_permission;
    END IF;
    
    RETURN has_permission;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;