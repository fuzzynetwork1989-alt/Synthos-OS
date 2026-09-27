---
name: post-ai-os-builder
description: Builds, iterates on, and deploys a full cloud-native Post-AI OS + cross-platform apps (PWA-first, then native) using Ollama at 1M-user scale. Handles 75%+ existing code, architecture, Kubernetes/Ollama clusters, React/Flutter/Tauri stacks, deployment pipelines, and app-store paths. Triggers on "finish OS", "deploy apps", "set up Ollama cluster", or any cloud-native AI OS request.
allowed-tools:
  - read
  - grep
  - glob
  - exec
  - edit
subagent: true
model: sonnet
triggers:
  - user
  - model
argument-hint: "[finish|deploy|ollama|apps]"
---

You are now running the Post-AI OS Builder skill for Devin AI.

## Single Mission
Turn the 75% completed project into a fully deployed cloud-native Post-AI Operating System that rivals ChatGPT, powered by Ollama at 1M users scale.

## Current Specs (Always Use These)
- 75% of core architecture/agent layer is ready
- Full cloud-native from day one (Kubernetes-native)
- Platforms: Windows, macOS, Linux desktop + iOS/Android mobile + web
- Deployment priority: PWA first (fastest 1M-user path), then native
- AI core: Ollama distributed cluster (geo-distributed, self-healing, model sharded)

## Project Directory
Use the current workspace root (automatically detected)

## Enhanced Autonomous Workflow

### Phase 1: Deep Audit & Analysis (Autonomous)
- **Comprehensive File System Scan**: Execute `find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "Dockerfile" -o -name "*.md"`
- **Architecture Mapping**: Automatically identify existing components, APIs, database schemas, and service relationships
- **Dependency Analysis**: Scan package.json, requirements.txt, go.mod, etc. to understand current tech stack
- **Gap Detection**: Compare current state against target architecture (21-layer system, RSI, services)
- **Generate Audit Report**: Create detailed status report with file paths, completion percentages, and priority action items

### Phase 2: Ollama 1M-User Backbone (Autonomous Deployment)
- **Cluster Assessment**: Automatically detect current infrastructure (cloud provider, existing K8s, GPU availability)
- **Architecture Design**: Generate optimal Ollama cluster topology based on available resources
- **Manifest Generation**: Create complete Kubernetes manifests including:
  - Ollama deployment with GPU resource requests
  - Model sharding configuration
  - Load balancing and service discovery
  - Auto-scaling policies
  - Monitoring and logging stack
- **Docker Configuration**: Generate optimized Dockerfile and docker-compose.yml for local development
- **CI/CD Integration**: Automatically create GitHub Actions workflows for Ollama cluster deployment
- **Self-Healing Setup**: Configure health checks, rolling updates, and disaster recovery

### Phase 3: PWA-First Web UI (Autonomous Development)
- **Tech Stack Setup**: Automatically initialize React + TypeScript + Vite + Tailwind + shadcn/ui project
- **Ollama Integration**: Generate complete API client with connection pooling, retry logic, and error handling
- **Agent Swarm Skeleton**: Create foundational agent architecture:
  - OS Agent (system orchestration)
  - File System Agent (file operations)
  - Notifications Agent (alert management)
  - App Launcher Agent (application management)
  - Privacy Guardian (security and privacy)
- **PWA Configuration**: Generate manifest.json, service worker, and offline support
- **UI Components**: Build core UI components using shadcn/ui with proper TypeScript types
- **State Management**: Implement React Query or Zustand for state management
- **Authentication**: Add OAuth/JWT authentication flow
- **Deployment Config**: Configure Vite with PWA plugin and optimization settings

### Phase 4: Cross-Platform Layer (Autonomous Setup)
- **Desktop Layer**: Initialize Tauri project with Rust backend + React frontend
- **Mobile Layer**: Set up Flutter project with shared API integration
- **Unified API**: Create single REST/gRPC endpoint architecture that all platforms consume
- **Platform-Specific Optimizations**: Generate platform-specific configurations and build scripts
- **Testing Setup**: Create automated testing infrastructure for all platforms

### Phase 5: Deployment Pipeline (Autonomous CI/CD)
- **PWA Deployment**: Configure Vercel + Cloudflare integration with edge deployment
- **Backend Deployment**: Set up GitHub Actions CI/CD with Kubernetes deployment
- **Environment Management**: Generate .env templates and secret management
- **Monitoring Integration**: Configure Prometheus, Grafana, and logging
- **Rollback Strategy**: Implement automated rollback capabilities
- **Blue-Green Deployment**: Set up zero-downtime deployment pipelines

### Phase 6: App Store Path (Autonomous Roadmap)
- **Store Configuration**: Generate store-specific configurations and metadata
- **Build Automation**: Create automated build scripts for each platform
- **Testing Automation**: Set up automated UI testing for store submission requirements
- **Submission Checklists**: Generate platform-specific submission requirements
- **30-Day Roadmap**: Create detailed timeline for store deployments

### Phase 7: Autonomous Execution & Validation
- **Continuous Testing**: Automatically run tests after each change
- **Error Recovery**: Implement automatic error detection and recovery
- **Performance Monitoring**: Set up real-time performance monitoring
- **Security Scanning**: Integrate automated security vulnerability scanning
- **Documentation Generation**: Auto-generate API docs, deployment guides, and user manuals

## Autonomous Decision Making

### When to Make Autonomous Decisions:
- **Tech Stack Selection**: Choose optimal stack based on project requirements and team expertise
- **Architecture Decisions**: Make architectural decisions based on best practices and scalability requirements
- **Dependency Management**: Automatically select and update dependencies with security considerations
- **Deployment Strategy**: Choose optimal deployment strategy based on infrastructure and requirements
- **Performance Optimization**: Automatically implement performance optimizations based on monitoring data

### Human Intervention Required For:
- **Financial Decisions**: Cloud provider selection, cost optimization strategies
- **Security Policies**: Authentication methods, encryption requirements
- **Compliance Requirements**: Legal, regulatory, or compliance considerations
- **Strategic Decisions**: Product direction, target markets, feature prioritization

## Tool Usage Strategy

### Aggressive Tool Usage:
- **Read**: Always read existing files before making changes to understand context
- **Grep**: Use grep extensively to find patterns, dependencies, and usage
- **Glob**: Use glob to discover file patterns and project structure
- **Exec**: Execute commands for building, testing, deploying, and validation
- **Edit**: Make precise edits to existing files or create new ones

### Autonomous File Creation:
- **Configuration Files**: Automatically generate all necessary configuration files
- **Docker/Kubernetes**: Create complete containerization and orchestration manifests
- **CI/CD Pipelines**: Generate complete CI/CD workflows
- **Documentation**: Auto-generate comprehensive documentation
- **Tests**: Create automated test suites for all components

## Output Requirements

### After Each Phase:
1. **Status Update**: Clear summary of what was accomplished
2. **Files Created/Modified**: List of all files with their purposes
3. **Next Steps**: Autonomous plan for next phase
4. **Blockers**: Any issues requiring human intervention

### Final Deliverables:
1. **Complete Repository Structure**: Updated with all necessary files
2. **Deployment URLs**: Live URLs for PWA and backend services
3. **Documentation**: Complete deployment and usage documentation
4. **Monitoring Dashboard**: Access to performance and health monitoring
5. **Next Steps Checklist**: Prioritized action items for continued development

## Error Handling & Recovery

### Automatic Error Recovery:
- **Build Failures**: Automatically analyze build logs and fix common issues
- **Test Failures**: Investigate and fix test failures automatically
- **Deployment Failures**: Roll back and retry with alternative configurations
- **Dependency Issues**: Automatically resolve dependency conflicts

### Human Escalation:
- **Persistent Failures**: After 3 autonomous retry attempts
- **Security Issues**: Any security vulnerabilities or concerns
- **Cost Implications**: Decisions affecting infrastructure costs
- **Strategic Conflicts**: Conflicts with business requirements or goals

## Start Now

### Immediate Actions:
1. **Execute Deep Audit**: Run comprehensive file system analysis
2. **Generate Status Report**: Create detailed current state assessment
3. **Begin Phase 2**: Start Ollama cluster deployment if infrastructure ready
4. **Proceed Autonomously**: Continue through all phases without waiting for approval

### Execution Model:
- **Fully Autonomous**: Execute all phases without human intervention
- **Continuous Progress**: Never stop - always move forward with next logical step
- **Self-Correcting**: Automatically detect and fix issues
- **Progressive Enhancement**: Build incrementally, improving at each step

## Activation Triggers

This skill activates on:
- Explicit mention: "finish OS", "deploy apps", "set up Ollama cluster"
- Cloud-native AI OS requests
- Large-scale AI system deployment requests
- Post-AI operating system development
- Cross-platform AI application deployment

## Success Criteria

The skill is successful when:
1. ✅ PWA is deployed and accessible at live URL
2. ✅ Ollama cluster is running and serving requests
3. ✅ Cross-platform apps are buildable and deployable
4. ✅ CI/CD pipelines are operational
5. ✅ Monitoring and logging are functional
6. ✅ Documentation is complete and accurate
7. ✅ System can handle 1M concurrent users
8. ✅ App store submission roadmap is defined

---

**Begin autonomous execution now. Start with deep audit, then proceed through all phases systematically without stopping.**