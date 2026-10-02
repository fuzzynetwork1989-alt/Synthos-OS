-- Evaluation Engine Database Schema
-- Benchmarking, testing, and performance evaluation

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Benchmarks
CREATE TABLE IF NOT EXISTS benchmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) UNIQUE NOT NULL,
    display_name VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    benchmark_type VARCHAR(50) NOT NULL, -- reasoning, coding, knowledge, safety, performance
    category VARCHAR(50) NOT NULL, -- general, domain_specific, custom
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active', -- active, deprecated, disabled
    evaluation_criteria JSONB NOT NULL,
    test_cases JSONB NOT NULL,
    scoring_rules JSONB NOT NULL,
    baseline_score FLOAT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Benchmark executions
CREATE TABLE IF NOT EXISTS benchmark_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    benchmark_id UUID NOT NULL REFERENCES benchmarks(id) ON DELETE CASCADE,
    model_id VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    execution_type VARCHAR(50) NOT NULL, -- manual, scheduled, ci_cd, regression
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, running, completed, failed, cancelled
    total_score FLOAT NULL,
    passed_count INTEGER DEFAULT 0,
    failed_count INTEGER DEFAULT 0,
    skipped_count INTEGER DEFAULT 0,
    execution_time_ms INTEGER NULL,
    environment JSONB DEFAULT '{}',
    config JSONB DEFAULT '{}',
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Test case results
CREATE TABLE IF NOT EXISTS test_case_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    execution_id UUID NOT NULL REFERENCES benchmark_executions(id) ON DELETE CASCADE,
    test_case_id VARCHAR(100) NOT NULL,
    test_case_name TEXT NOT NULL,
    status VARCHAR(50) NOT NULL, -- passed, failed, skipped, error
    score FLOAT NULL,
    max_score FLOAT NULL,
    output_data JSONB NULL,
    expected_output JSONB NULL,
    actual_output JSONB NULL,
    error_message TEXT NULL,
    execution_time_ms INTEGER NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evaluation metrics
CREATE TABLE IF NOT EXISTS evaluation_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    metric_type VARCHAR(50) NOT NULL, -- accuracy, precision, recall, f1, latency, throughput
    unit VARCHAR(20) NULL,
    aggregation_method VARCHAR(50) NOT NULL, -- average, weighted_average, median, max, min
    is_higher_better BOOLEAN DEFAULT true,
    target_value FLOAT NULL,
    threshold_value FLOAT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Metric measurements
CREATE TABLE IF NOT EXISTS metric_measurements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_id UUID NOT NULL REFERENCES evaluation_metrics(id) ON DELETE CASCADE,
    execution_id UUID NOT NULL REFERENCES benchmark_executions(id) ON DELETE CASCADE,
    value FLOAT NOT NULL,
    unit VARCHAR(20) NULL,
    context_data JSONB DEFAULT '{}',
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance baselines
CREATE TABLE IF NOT EXISTS performance_baselines (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    baseline_name VARCHAR(200) UNIQUE NOT NULL,
    baseline_type VARCHAR(50) NOT NULL, -- model, system, service
    target_id VARCHAR(100) NOT NULL,
    target_version VARCHAR(50) NOT NULL,
    baseline_values JSONB NOT NULL,
    measurement_conditions JSONB DEFAULT '{}',
    established_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Regression tests
CREATE TABLE IF NOT EXISTS regression_tests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_name VARCHAR(200) UNIQUE NOT NULL,
    test_description TEXT NOT NULL,
    test_type VARCHAR(50) NOT NULL, -- functional, performance, security, compatibility
    severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    baseline_execution_id UUID NULL,
    baseline_results JSONB NULL,
    threshold_percentage FLOAT DEFAULT 5.0, -- Allow 5% regression
    is_active BOOLEAN DEFAULT true,
    schedule VARCHAR(50) DEFAULT 'manual', -- manual, daily, weekly, on_commit
    last_run_at TIMESTAMP NULL,
    last_status VARCHAR(50) NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Regression test results
CREATE TABLE IF NOT EXISTS regression_test_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    regression_test_id UUID NOT NULL REFERENCES regression_tests(id) ON DELETE CASCADE,
    execution_id UUID NOT NULL REFERENCES benchmark_executions(id) ON DELETE CASCADE,
    baseline_value FLOAT NULL,
    current_value FLOAT NULL,
    regression_percentage FLOAT NULL,
    is_regression BOOLEAN DEFAULT false,
    regression_severity VARCHAR(20) NULL, -- low, medium, high, critical
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evaluation reports
CREATE TABLE IF NOT EXISTS evaluation_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_type VARCHAR(50) NOT NULL, -- benchmark, regression, performance, comparison
    report_name VARCHAR(300) NOT NULL,
    report_data JSONB NOT NULL,
    summary TEXT NULL,
    recommendations TEXT[] DEFAULT '{}',
    generated_by UUID NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    metadata JSONB DEFAULT '{}'
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_benchmarks_name ON benchmarks(name);
CREATE INDEX IF NOT EXISTS idx_benchmarks_type ON benchmarks(benchmark_type);
CREATE INDEX IF NOT EXISTS idx_benchmarks_category ON benchmarks(category);
CREATE INDEX IF NOT EXISTS idx_benchmarks_status ON benchmarks(status);

CREATE INDEX IF NOT EXISTS idx_benchmark_executions_benchmark ON benchmark_executions(benchmark_id);
CREATE INDEX IF NOT EXISTS idx_benchmark_executions_model ON benchmark_executions(model_id);
CREATE INDEX IF NOT EXISTS idx_benchmark_executions_status ON benchmark_executions(status);
CREATE INDEX IF NOT EXISTS idx_benchmark_executions_type ON benchmark_executions(execution_type);
CREATE INDEX IF NOT EXISTS idx_benchmark_executions_created ON benchmark_executions(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_test_case_results_execution ON test_case_results(execution_id);
CREATE INDEX IF NOT EXISTS idx_test_case_results_status ON test_case_results(status);
CREATE INDEX IF NOT EXISTS idx_test_case_results_case ON test_case_results(test_case_id);

CREATE INDEX IF NOT EXISTS idx_evaluation_metrics_name ON evaluation_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_evaluation_metrics_type ON evaluation_metrics(metric_type);

CREATE INDEX IF NOT EXISTS idx_metric_measurements_metric ON metric_measurements(metric_id);
CREATE INDEX IF NOT EXISTS idx_metric_measurements_execution ON metric_measurements(execution_id);
CREATE INDEX IF NOT EXISTS idx_metric_measurements_measured ON metric_measurements(measured_at DESC);

CREATE INDEX IF NOT EXISTS idx_performance_baselines_name ON performance_baselines(baseline_name);
CREATE INDEX IF NOT EXISTS idx_performance_baselines_type ON performance_baselines(baseline_type);
CREATE INDEX IF NOT EXISTS idx_performance_baselines_target ON performance_baselines(target_id);
CREATE INDEX IF NOT EXISTS idx_performance_baselines_active ON performance_baselines(is_active);

CREATE INDEX IF NOT EXISTS idx_regression_tests_name ON regression_tests(test_name);
CREATE INDEX IF NOT EXISTS idx_regression_tests_type ON regression_tests(test_type);
CREATE INDEX IF NOT EXISTS idx_regression_tests_severity ON regression_tests(severity);
CREATE INDEX IF NOT EXISTS idx_regression_tests_active ON regression_tests(is_active);
CREATE INDEX IF NOT EXISTS idx_regression_tests_schedule ON regression_tests(schedule);

CREATE INDEX IF NOT EXISTS idx_regression_test_results_test ON regression_test_results(regression_test_id);
CREATE INDEX IF NOT EXISTS idx_regression_test_results_execution ON regression_test_results(execution_id);
CREATE INDEX IF NOT EXISTS idx_regression_test_results_regression ON regression_test_results(is_regression);

CREATE INDEX IF NOT EXISTS idx_evaluation_reports_type ON evaluation_reports(report_type);
CREATE INDEX IF NOT EXISTS idx_evaluation_reports_generated ON evaluation_reports(generated_at DESC);

-- Triggers for updated_at
CREATE TRIGGER update_benchmarks_updated_at BEFORE UPDATE ON benchmarks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_evaluation_metrics_updated_at BEFORE UPDATE ON evaluation_metrics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_performance_baselines_updated_at BEFORE UPDATE ON performance_baselines
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_regression_tests_updated_at BEFORE UPDATE ON regression_tests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to calculate benchmark score
CREATE OR REPLACE FUNCTION calculate_benchmark_score(p_execution_id UUID)
RETURNS FLOAT AS $$
DECLARE
    total_score FLOAT;
    total_max_score FLOAT;
BEGIN
    SELECT 
        COALESCE(SUM(score), 0.0),
        COALESCE(SUM(max_score), 0.0)
    INTO total_score, total_max_score
    FROM test_case_results
    WHERE execution_id = p_execution_id;
    
    IF total_max_score > 0 THEN
        RETURN (total_score / total_max_score) * 100.0;
    ELSE
        RETURN 0.0;
    END IF;
END;
$$ LANGUAGE plpgsql;