# Synthos-OS Validation Skill

## Description
Validates Synthos-OS components against project requirements, safety rules, and architectural standards. Ensures all changes comply with the 21-layer architecture and AGENTS.md requirements.

## When to Use
- Before making code changes to validate compliance
- When reviewing pull requests for project rule adherence
- When implementing new features to ensure architectural alignment
- When testing new components for safety and quality compliance
- When validating CI/CD pipeline configurations

## Validation Layers

### 1. Architecture Layer Validation
- Validates against 21 required architecture layers
- Ensures proper component integration
- Checks layer interdependencies
- Validates data flow between layers

### 2. Safety Rule Validation
- Checks AGENTS.md safety and quality rules
- Validates no fake production behavior
- Ensures no placeholder business logic
- Validates proper error handling
- Checks for secrets exposure risks

### 3. Model Rule Validation
- Validates model gateway integration
- Checks model registry requirements
- Ensures structured JSON/typed schemas
- Validates untrusted output handling
- Checks model card requirements

### 4. Definition of Done Validation
- Checks acceptance criteria
- Validates test coverage
- Ensures linting/formatting/type checks
- Validates security implications
- Checks observability implementation
- Validates documentation updates
- Ensures database migration testing
- Checks rollback documentation
- Validates missing items register updates

## Usage Examples

### Validate Code Changes
```bash
# Check if changes comply with project rules
python scripts/validate_changes.py --file services/rsi-engine/synthos_rsi_engine/core/coordinator.py
```

### Validate Architecture Layer
```bash
# Validate specific architecture layer implementation
python scripts/validate_layer.py --layer memory --component memory-engine
```

### Validate Safety Compliance
```bash
# Check safety rule compliance
python scripts/validate_safety.py --directory services/rsi-engine
```

### Validate CI/CD Configuration
```bash
# Validate CI/CD pipeline configuration
python scripts/validate_cicd.py --workflow .github/workflows/ci.yml
```

## Validation Criteria

### Must Pass
- All safety rules from AGENTS.md
- Architecture layer requirements
- Definition of done criteria
- No security vulnerabilities
- No secrets exposure
- Proper error handling

### Should Pass
- Code quality standards
- Test coverage thresholds
- Documentation completeness
- Performance benchmarks

### May Fail
- Performance optimizations (with justification)
- Temporary workarounds (with TODO and timeline)
- Experimental features (with proper labeling)

## Integration with AGENTS.md
This skill implements the required agent behavior from AGENTS.md:
- Reads AGENTS.md before code modifications
- Reads directory-level AGENTS.md
- Reads relevant requirements and architecture docs
- Inspects existing contracts and tests
- Identifies missing requirements and gaps
- Records gaps in missing-items.md
- Builds focused, testable vertical slices

## Common Validation Failures

### Critical Failures
- Safety rule violations
- Secrets exposure
- Unrestricted shell commands
- Missing authentication/authorization
- Database schema changes without migration

### High Severity Failures
- Missing test coverage
- Incomplete error handling
- Missing observability
- Incomplete documentation
- Architecture layer violations

### Medium Severity Failures
- Code quality issues
- Performance regressions
- Missing type hints
- Incomplete integration

## Output Format
Validation results are returned in structured JSON format:
```json
{
  "status": "pass/fail/warning",
  "score": 0-100,
  "critical_issues": [],
  "high_issues": [],
  "medium_issues": [],
  "low_issues": [],
  "recommendations": [],
  "architecture_layers_validated": [],
  "safety_rules_compliant": true/false
}
```

## Continuous Integration
This skill is integrated into CI/CD pipelines:
- Runs on every pull request
- Blocks merges on critical failures
- Provides detailed feedback for fixes
- Updates missing-items.md automatically