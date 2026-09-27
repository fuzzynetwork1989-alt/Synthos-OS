# RSI Engine Activation Guide

## Overview

This guide demonstrates how to activate the Recursive Self-Improvement (RSI) engine for Synthos-OS, including the revolutionary Cognitive DNA Evolution System.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ available locally
- Environment configured (.env file created)

## Step 1: Start the RSI Engine Service

### Using Docker Compose

```bash
# Start RSI engine with dependencies
docker-compose up -d rsi-engine postgres redis

# Check service status
docker-compose ps
```

### Using Local Python

```bash
# Navigate to RSI engine directory
cd services/rsi-engine

# Install dependencies
pip install -e .

# Start the service
python -m synthos_rsi_engine.main
```

The RSI engine will start on port 8004.

## Step 2: Verify RSI Engine Status

```bash
# Check health endpoint
curl http://localhost:8004/health

# Expected response:
{
  "status": "healthy",
  "coordinator_status": {
    "current_cycle": null,
    "cycle_count": 0,
    "total_mutations_generated": 0,
    "total_mutations_approved": 0,
    "resource_budgets": {
      "max_cycles": 10,
      "max_mutations_per_cycle": 5,
      "max_compute_per_cycle": 3600
    },
    "gdi_status": "active"
  },
  "state_manager_status": {
    "current_state": "initial",
    "current_version": "0.1.0"
  }
}
```

## Step 3: Start a Manual RSI Cycle

### Manual Cycle Start

```bash
# Start a manual improvement cycle
curl -X POST http://localhost:8004/rsi/cycle/start \
  -H "Content-Type: application/json" \
  -d '{
    "trigger_reason": "Initial system optimization",
    "auto_approve": false
  }'

# Expected response:
{
  "cycle_id": "cycle_1",
  "status": "approved",
  "mutations_generated": 3,
  "mutations_approved": 2,
  "gdi_before": 0.1,
  "gdi_after": 0.08,
  "performance_delta": 0.05
}
```

### Monitor Cycle Progress

```bash
# Get cycle status
curl http://localhost:8004/rsi/cycle/cycle_1

# Get all cycles
curl http://localhost:8004/rsi/cycles
```

## Step 4: Enable Autonomous Mode

The autonomous mode enables the Continuous RSI system to self-trigger improvement cycles based on system conditions.

### Enable Autonomous Mode

```bash
# Enable autonomous mode (basic)
curl -X POST http://localhost:8004/rsi/autonomous/enable

# Enable with safety override (for enhanced autonomy)
curl -X POST http://localhost:8004/rsi/autonomous/enable \
  -H "Content-Type: application/json" \
  -d '{
    "safety_override_key": "secure-override-key"
  }'

# Expected response:
{
  "status": "autonomous_mode_enabled"
}
```

### Check Autonomous Status

```bash
# Get autonomous mode status
curl http://localhost:8004/rsi/autonomous/status

# Expected response:
{
  "autonomous_enabled": true,
  "emergency_stop_triggered": false,
  "monitoring_active": true,
  "trigger_history_count": 0,
  "performance_baseline": {
    "response_time": 100.0,
    "error_rate": 0.01,
    "cpu_usage": 0.3,
    "memory_usage": 0.4,
    "throughput": 1000.0
  },
  "current_metrics": {
    "response_time": 100.0,
    "error_rate": 0.01,
    "cpu_usage": 0.3,
    "memory_usage": 0.4,
    "throughput": 1000.0
  },
  "resource_budgets": {
    "max_cycles": 10,
    "max_mutations_per_cycle": 5,
    "max_compute_per_cycle": 3600
  }
}
```

## Step 5: Manual Trigger in Autonomous Mode

Even in autonomous mode, you can manually trigger improvement cycles.

```bash
# Manual trigger
curl -X POST http://localhost:8004/rsi/autonomous/manual-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Performance optimization needed",
    "context": {
      "cpu_usage": 0.85,
      "memory_usage": 0.9
    }
  }'

# Expected response:
{
  "status": "manual_trigger_initiated"
}
```

## Step 6: Monitor Meta-RSI Metrics

The Meta-RSI system tracks the evolution of improvement strategies.

```bash
# Get Meta-RSI performance metrics
curl http://localhost:8004/rsi/meta/metrics

# Expected response:
{
  "improvement_strategy": "balanced",
  "gene_count": 0,
  "success_rate": 0.0,
  "performance_history": [],
  "evolution_generation": 0,
  "best_strategy": "balanced"
}
```

## Step 7: Safety Monitoring

Monitor safety systems to ensure alignment is maintained.

```bash
# Get Goal Drift Index status
curl http://localhost:8004/safety/gdi

# Expected response:
{
  "current_gdi": 0.05,
  "status": "healthy",
  "signals": [
    {
      "name": "goal_alignment",
      "value": 0.95,
      "threshold": 0.8,
      "status": "healthy"
    }
  ],
  "trend": "stable"
}

# Get constitutional constraints summary
curl http://localhost:8004/safety/constraints
```

## Step 8: Emergency Procedures

Always have emergency procedures available.

```bash
# Emergency stop - halts all RSI activity
curl -X POST http://localhost:8004/rsi/emergency-stop

# Expected response:
{
  "status": "emergency_stop_triggered"
}

# Disable autonomous mode
curl -X POST http://localhost:8004/rsi/autonomous/disable

# Expected response:
{
  "status": "autonomous_mode_disabled"
}
```

## Step 9: System State Management

Monitor and manage system state and versions.

```bash
# Get current system state
curl http://localhost:8001/system/state

# Expected response:
{
  "state": "initial",
  "version": "0.1.0",
  "version_history": [
    {
      "version": "0.1.0",
      "timestamp": "2024-01-01T00:00:00",
      "changes_count": 0
    }
  ]
}

# Rollback to a specific version if needed
curl -X POST http://localhost:8004/system/rollback/0.1.0
```

## Cognitive DNA Evolution System

The revolutionary Cognitive DNA Evolution System enables the RSI engine to:

1. **Learn from Improvement History**: Extract successful improvement patterns as "genes"
2. **Evolve Improvement Strategies**: Use genetic operations to evolve better improvement methodologies
3. **Self-Optimize the Improvement Process**: Meta-RSI continuously improves how the system improves itself
4. **Autonomous Operation**: Self-triggering improvement cycles based on system conditions
5. **Adaptive Resource Management**: Dynamic resource allocation based on strategy performance

### Trigger Conditions for Autonomous Cycles

The Continuous RSI system automatically triggers improvement cycles based on:

- **Performance Degradation**: When system performance drops below baseline
- **Error Rate Threshold**: When error rate exceeds configured threshold (default 5%)
- **Resource Pressure**: When CPU or memory usage exceeds threshold (default 80%)
- **Improvement Opportunities**: When Meta-RSI detects favorable conditions for improvement
- **Time-Based**: Periodic cycles based on configured intervals
- **Manual Requests**: User-initiated improvement cycles

### Resource Budgeting

The system uses adaptive resource budgeting based on improvement strategy:

- **Conservative**: 50% of baseline resources
- **Balanced**: 100% of baseline resources
- **Aggressive**: 150% of baseline resources

### Safety Layers

The RSI engine includes 10-layer safety validation:

1. Constitutional constraint checking
2. Goal drift monitoring
3. Invariant preservation
4. Security validation
5. Performance regression checks
6. Dependency safety
7. Code quality gates
8. Test coverage requirements
9. Deployment safety
10. Rollback capability

## Configuration

Edit the RSI engine configuration in `services/rsi-engine/synthos_rsi_engine/config.py`:

```python
# RSI Configuration
max_improvement_cycles: int = 10
max_mutations_per_cycle: int = 5
auto_approve_low_risk: bool = False
emergency_stop_enabled: bool = True

# Safety Configuration
gdi_threshold: float = 0.5
constitutional_enforcement: bool = True
invariant_preservation: bool = True

# Resource Budgets
max_compute_per_cycle: int = 3600  # 1 hour
max_token_budget: int = 100000
max_files_changed: int = 10
```

## Monitoring and Logs

Check logs for RSI activity:

```bash
# View RSI engine logs
docker-compose logs -f rsi-engine

# Check specific logs
tail -f logs/rsi_audit.log
```

## Troubleshooting

### RSI Engine Won't Start

1. Check dependencies are running: `docker-compose ps`
2. Verify configuration: Check `.env` file
3. Check logs: `docker-compose logs rsi-engine`

### Autonomous Mode Not Triggering

1. Verify autonomous mode is enabled: `curl http://localhost:8001/rsi/autonomous/status`
2. Check trigger conditions are met
3. Review monitoring logs for issues

### Safety Gates Blocking Improvements

1. Check GDI status: `curl http://localhost:8001/safety/gdi`
2. Review constitutional constraints: `curl http://localhost:8001/safety/constraints`
3. Check gate results in cycle history

## Next Steps

After activating the RSI engine:

1. Monitor initial improvement cycles
2. Review Meta-RSI metrics to understand strategy evolution
3. Configure trigger conditions based on your needs
4. Set up monitoring and alerting
5. Document successful improvement patterns

## Safety Notes

- Always have emergency stop capability available
- Monitor Goal Drift Index regularly
- Review changes before applying in production
- Keep human oversight for high-risk changes
- Maintain audit trails for all improvements
- Test improvements in staging first