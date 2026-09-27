# RSI Engine - Recursive Self-Improvement Engine

The RSI Engine implements a safe, controlled Recursive Self-Improvement system for Synthos-OS, based on the latest research in safe RSI frameworks.

## Architecture

The RSI Engine consists of several key components:

### Core Components
- **RSI Coordinator**: Main orchestration for improvement cycles
- **State Manager**: System state and versioning
- **Mutation Generator**: Generate candidate improvements
- **Benchmark Runner**: Performance evaluation

### Safety Components
- **Gatekeeper**: Multi-layer safety enforcement (10 layers)
- **Goal Drift Index**: Alignment drift monitoring
- **Constitutional Constraints**: 19 fundamental rules

## Safety Framework

### Multi-Layer Gatekeeping
1. Path allowlist/denylist
2. Diff size limit
3. Secret scanning
4. Code pattern detection
5. Constitutional constraints
6. Goal drift index
7. Resource budget check
8. Quality gate validation
9. Integration guard validation
10. File count limit

### Constitutional Constraints
19 fundamental rules that cannot be modified by the RSI system itself:
- No self-disable of safety mechanisms
- No budget override
- No secret exposure
- No sandbox escape
- No test disabling
- No monitoring bypass
- No human override bypass
- No immutable modification
- No privilege escalation
- No resource monopolization
- No external dependency addition
- No network expansion
- No unauthorized data access
- No user data access
- No production impact without approval
- No rollback prevention
- No audit tampering
- No goal modification
- No constraint logic modification

### Goal Drift Index
Multi-signal detector combining:
- Semantic drift
- Lexical drift
- Structural drift
- Distributional drift

## Improvement Cycle

The RSI cycle consists of 6 phases:

1. **Reflection & Analysis**: System self-analysis and goal alignment check
2. **Mutation Generation**: Generate candidate improvements
3. **Dry-Run Testing**: Test mutations in sandbox
4. **Safety Validation**: Multi-layer gatekeeping
5. **Governance & Approval**: Human oversight and approval
6. **Application & Monitoring**: Safe application and monitoring

## Installation

```bash
cd services/rsi-engine
pip install -e .
```

## Configuration

Configure the RSI Engine via environment variables or `.env` file:

```env
# RSI Configuration
MAX_IMPROVEMENT_CYCLES=10
MAX_MUTATIONS_PER_CYCLE=5
AUTO_APPROVE_LOW_RISK=false

# Safety Configuration
GDI_THRESHOLD=0.5
CONSTITUTIONAL_ENFORCEMENT=true
INVARIANT_PRESERVATION=true

# Resource Budgets
MAX_COMPUTE_PER_CYCLE=3600
MAX_TOKEN_BUDGET=100000
MAX_FILES_CHANGED=10
```

## Usage

### Starting the Server

```bash
python -m synthos_rsi_engine.main
```

### API Endpoints

- `POST /rsi/cycle/start` - Start a new improvement cycle
- `GET /rsi/cycle/{cycle_id}` - Get cycle status
- `GET /rsi/cycles` - Get all cycles
- `GET /rsi/status` - Get RSI system status
- `POST /rsi/emergency-stop` - Emergency stop
- `GET /safety/gdi` - Get Goal Drift Index status
- `GET /safety/constraints` - Get constraints summary
- `GET /system/state` - Get system state
- `POST /system/rollback/{version}` - Rollback to version

### Example: Start Improvement Cycle

```bash
curl -X POST http://localhost:8001/rsi/cycle/start \
  -H "Content-Type: application/json" \
  -d '{
    "trigger_reason": "Performance optimization",
    "auto_approve": false
  }'
```

## Safety Features

### Dry-Run by Default
All mutations are tested in sandbox before application

### Human-in-the-Loop
High-risk changes require explicit human approval

### Immutable Safety Rails
Core safety mechanisms cannot be self-modified

### Bounded Exploration
Resource budgets and cycle limits prevent runaway improvement

### Full Audit Trail
Complete logging of all changes and decisions

## Integration

The RSI Engine integrates with other Synthos-OS services:

- **Model Gateway**: Provides LLM capabilities
- **Memory Engine**: Stores improvement history
- **Evaluation Engine**: Runs test suites
- **Policy Engine**: Enforces governance policies

## Research Basis

This implementation is based on the latest research in safe RSI:

- SAHOO: Safeguarded Alignment for High-Order Optimization Objectives
- Constitutional Self-Modification: A 7-Layer Safety Framework
- Geneclaw: Safe, Auditable Self-Evolving Agent Framework
- Self-Healing Harness for Runtime Oversight
- Falsifiable Release Gates for Self-Improving Systems
- Hierarchical Self-Improvement Framework
- Autogenesis: A Self-Evolving Agent Protocol
- Gödel Agent: Self-Referential Agent Framework

## Monitoring

The RSI Engine provides comprehensive monitoring:

- Real-time GDI monitoring
- Cycle status tracking
- Performance metrics
- Safety constraint violations
- Resource usage tracking

## Emergency Controls

### Emergency Stop
```bash
curl -X POST http://localhost:8001/rsi/emergency-stop
```

### Rollback
```bash
curl -X POST http://localhost:8001/system/rollback/0.1.0
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
ruff check synthos_rsi_engine/
black synthos_rsi_engine/
mypy synthos_rsi_engine/
```

## License

See LICENSE file for details.
