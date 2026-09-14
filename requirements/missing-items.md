# Missing Items Register

This register is maintained by Devin Autopilot Mode.

| ID | Severity | Layer | Category | Missing Item | Why It Matters | Required Action | Verification | Status |
|---|---:|---|---|---|---|---|---|---|
| GAP-001 | Critical | 12 | Permissions | No tool-permission matrix | Agents could access tools without clear authority | Implement capability-based tool authorization | Denial tests pass | Open |
| GAP-002 | High | 16 | Evaluation | No prompt-injection test corpus | Retrieval and tool layers may follow malicious content | Create adversarial evaluation cases | Security suite passes | Open |
| GAP-003 | High | 20 | Recovery | Restore drill undocumented | Data recovery cannot be trusted during an incident | Document and test restoration | Recovery drill report | Open |
| GAP-004 | Medium | 3 | Memory | Memory deletion workflow incomplete | Users need control over retained information | Add deletion API and UI | E2E deletion test | Open |
| GAP-005 | High | 15 | Observability | No monitoring infrastructure deployed | Cannot detect issues or measure performance | Deploy Prometheus, Grafana, and structured logging | Metrics visible in dashboards | Open |
| GAP-006 | High | 14 | Safety | No emergency stop mechanism | Cannot halt harmful autonomous actions | Implement emergency stop controls and workflows | Emergency stop tested and verified | Open |
| GAP-007 | Medium | 17 | Persistence | No encryption at rest for sensitive data | Database compromise could expose private information | Implement transparent data encryption (TDE) | Encryption verified in production | Open |
| GAP-008 | Medium | 18 | Synchronization | No conflict resolution strategy | Multi-device sync could cause data loss | Implement conflict detection and resolution | Conflict resolution tested | Open |
| GAP-009 | Low | 21 | Learning | No feedback collection mechanism | Cannot learn from user interactions for improvement | Add feedback capture and analysis | Feedback pipeline operational | Open |

Severity definitions:

```
Critical: Security breach, data loss, unauthorized action, broken core path, or release blocker.
High: Significant reliability, privacy, testing, deployment, or product gap.
Medium: Important maintainability, observability, usability, or scalability gap.
Low: Refinement, optimization, research, or future enhancement.
```
