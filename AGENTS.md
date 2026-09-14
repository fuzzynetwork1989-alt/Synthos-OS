# Synthos-OS — Devin Operating Rules

## Mission

Build a hybrid, local-first and cloud-capable AI operating system with persistent
memory, multimodal perception, reasoning, planning, workflow orchestration,
tool routing, governance, safety, evaluation, and deployment capabilities.

The system includes a foundational AI OS, the future HEICN architecture,
the future HSAIN architecture, and a long-term Self-Organizing Intelligence path.

## Project Identity

- **Project Name:** Synthos-OS
- **Repository Name:** Synthos-OS
- **System Type:** Next-Generation Cognitive, Agentic, and Self-Organizing AI Operating System
- **Primary Goal:** Build a hybrid local/cloud AI operating platform with persistent memory,
  model routing, reasoning, planning, multimodal interaction, tools, governance,
  evaluation, deployment, and a future path toward HEICN, HSAIN, and Self-Organizing Intelligence.

## Required Agent Behavior

Before modifying code:

1. Read this `AGENTS.md`.
2. Read the closest directory-level `AGENTS.md`.
3. Read relevant files in `requirements/`, `docs/architecture/`, and `docs/workflows/`.
4. Inspect existing contracts, tests, environment configuration, and migration history.
5. Identify missing requirements, missing tests, security gaps, documentation gaps,
   observability gaps, API-contract gaps, migration gaps, and release gaps.
6. Record significant gaps in `requirements/missing-items.md`.
7. Build one focused, complete, testable vertical slice per branch and pull request.

## Mandatory Autopilot Loop

For every feature:

Discover -> Specify -> Plan -> Implement -> Test -> Secure -> Observe ->
Document -> Review -> Pull Request -> Verify -> Release Gate

Do not skip stages.

## Architecture Requirements

The implementation must support the following major layers:

1. Perception and input
2. Identity
3. Memory
4. Retrieval
5. Context assembly
6. World modeling
7. Reasoning
8. Planning
9. Tool routing
10. Task execution
11. Orchestration
12. Permissions
13. Governance
14. Safety
15. Observability
16. Evaluation
17. Persistence
18. Synchronization
19. User interface and product elements
20. Deployment, recovery, and rollback
21. Ongoing learning

Every feature must identify which layer or layers it affects.

## Safety and Quality Rules

- Do not use fake production behavior, placeholder business logic, untracked TODOs,
  empty error handling, or mocked data paths in production code.
- Do not claim sentience, consciousness, guaranteed safety, legal compliance,
  performance superiority, or "first of its kind" status without supporting evidence.
- Do not allow models to issue unrestricted shell commands, browser automation,
  account changes, financial actions, external writes, or physical-device controls.
- Do not permit model-generated actions to bypass typed validation, permissions,
  policy checks, tool schemas, sandboxing, or approval workflows.
- Do not expose secrets, private prompts, credentials, personal data, raw documents,
  access tokens, or private model artifacts in code, logs, tests, screenshots, or pull requests.
- Do not deploy to production, rotate credentials, change DNS, create paid resources,
  or modify real external accounts without explicit human approval.
- Do not add paid dependencies without documenting them and obtaining approval.
- Prefer free, local, and open-source components where practical.

## Model Rules

- All model providers must be accessed through the model-gateway service.
- Support Ollama, LM Studio, Hugging Face, and optional remote providers through adapters.
- Keep model identity, version, prompt version, adapter version, evaluation data,
  license, base model, and hardware requirements in the model registry.
- Treat model output as untrusted until validated.
- Use structured JSON or typed schemas for plans, tool calls, policies, and task state.
- Do not store unverified model output as factual long-term memory.
- All fine-tuned models and adapters require a model card and evaluation report.

## Definition of Done

A task is complete only when:

- Acceptance criteria are met.
- Tests have been created or updated.
- Relevant linting, formatting, type checks, unit tests, integration tests,
  and end-to-end tests have passed.
- Security implications were reviewed.
- Observability was added where needed.
- Documentation and environment references were updated.
- Database migrations were tested if schema changed.
- Rollback or recovery implications were documented.
- New gaps were fixed or added to `requirements/missing-items.md`.
- The pull request includes validation evidence.
