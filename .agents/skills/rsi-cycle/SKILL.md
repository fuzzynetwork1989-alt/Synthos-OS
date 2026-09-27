# RSI Cycle Management Skill

## Description
Manages Recursive Self-Improvement (RSI) cycles for the Synthos-OS project, including starting improvement cycles, monitoring progress, and handling safety validations.

## When to Use
- When you need to start an RSI improvement cycle
- When monitoring RSI system status or progress
- When reviewing RSI change proposals
- When handling RSI safety validations
- When managing RSI emergency procedures

## Usage

### Start Improvement Cycle
```bash
# Start a new RSI improvement cycle
curl -X POST http://localhost:8001/rsi/cycle/start \
  -H "Content-Type: application/json" \
  -d '{
    "trigger_reason": "Performance optimization",
    "auto_approve": false
  }'
```

### Monitor RSI Status
```bash
# Get overall RSI system status
curl http://localhost:8001/rsi/status

# Get specific cycle status
curl http://localhost:8001/rsi/cycle/cycle_1

# Get all cycles
curl http://localhost:8001/rsi/cycles
```

### Safety Monitoring
```bash
# Get Goal Drift Index status
curl http://localhost:8001/safety/gdi

# Get constitutional constraints summary
curl http://localhost:8001/safety/constraints
```

### Emergency Procedures
```bash
# Emergency stop
curl -X POST http://localhost:8001/rsi/emergency-stop

# Rollback to version
curl -X POST http://localhost:8001/system/rollback/0.1.0
```

## Important Notes
- RSI cycles are resource-budgeted and limited
- High-risk changes require human approval
- All changes go through 10-layer safety validation
- Emergency stop is always available
- System maintains full audit trail

## Integration Points
- Model Gateway: Provides LLM capabilities for mutation generation
- Memory Engine: Stores improvement history and patterns
- Evaluation Engine: Runs comprehensive test suites
- Policy Engine: Enforces governance policies

## Safety Considerations
- RSI cannot modify its own constitutional constraints
- Goal Drift Index monitors alignment in real-time
- Resource budgets prevent runaway improvement
- Human oversight maintained for high-risk changes