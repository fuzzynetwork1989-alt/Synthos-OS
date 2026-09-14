# Missing Items Register

This register is maintained by Devin Autopilot Mode.

| ID | Severity | Layer | Category | Missing Item | Why It Matters | Required Action | Verification | Status |
|---|---:|---|---|---|---|---|---|---|
| GAP-001 | Critical | 12 | Permissions | No tool-permission matrix | Agents could access tools without clear authority | Implement capability-based tool authorization | Denial tests pass | Open |
| GAP-002 | High | 16 | Evaluation | No prompt-injection test corpus | Retrieval and tool layers may follow malicious content | Create adversarial evaluation cases | Security suite passes | Open |
| GAP-003 | High | 20 | Recovery | Restore drill undocumented | Data recovery cannot be trusted during an incident | Document and test restoration | Recovery drill report | Open |
| GAP-004 | Medium | 3 | Memory | Memory deletion workflow incomplete | Users need control over retained information | Add deletion API and UI | E2E deletion test | Open |

Severity definitions:

```
Critical: Security breach, data loss, unauthorized action, broken core path, or release blocker.
High: Significant reliability, privacy, testing, deployment, or product gap.
Medium: Important maintainability, observability, usability, or scalability gap.
Low: Refinement, optimization, research, or future enhancement.
```
