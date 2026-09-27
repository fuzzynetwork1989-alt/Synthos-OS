# Synthos-OS

Next-Generation Cognitive, Agentic, and Self-Organizing AI Operating System

## 🧬 Revolutionary Feature: Cognitive DNA Evolution

Synthos-OS features a groundbreaking **Cognitive DNA Evolution System** that enables fully autonomous recursive self-improvement. This unique capability allows the system to:

1. **Learn from Improvement History**: Extract successful improvement patterns as "genes"
2. **Evolve Improvement Strategies**: Use genetic operations (crossover, mutation) to evolve better improvement methodologies
3. **Self-Optimize the Improvement Process**: Meta-RSI continuously improves how the system improves itself
4. **Autonomous Operation**: Self-triggering improvement cycles based on system conditions
5. **Adaptive Resource Management**: Dynamic resource allocation based on strategy performance

This represents a fundamental breakthrough - not just improving capabilities, but improving the improvement process itself through meta-level recursion.

## Overview

Synthos-OS is a hybrid, local-first and cloud-capable AI operating system with persistent memory, multimodal perception, reasoning, planning, workflow orchestration, tool routing, governance, safety, evaluation, and deployment capabilities.

The system includes:
- Foundational AI OS with 21 architectural layers
- **Cognitive DNA Evolution System** for autonomous self-improvement
- Future HEICN (Holistic Evolving Interactive Cognitive Nexus) architecture
- Future HSAIN (Hyper-Synergistic Autonomous Intelligence Nexus) architecture
- Long-term Self-Organizing Intelligence path
- Cross-platform applications (Desktop, Mobile, VR/AR)

## Architecture

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| API Gateway | 8000 | Main API entry point and routing |
| Model Gateway | 8002 | Model provider routing (Ollama, OpenAI, Anthropic) |
| Memory Engine | 8003 | Persistent memory and knowledge storage |
| RSI Engine | 8004 | Recursive self-improvement with Cognitive DNA |
| Cognitive Engine | 8005 | Reasoning and planning engine |
| Tool Execution Engine | 8006 | Tool execution and sandboxing |
| Workflow Engine | 8007 | Workflow orchestration |
| Policy Engine | 8008 | Governance and policy enforcement |
| Evaluation Engine | 8009 | Testing and benchmarking |
| Device Gateway | 8010 | Device communication and management |

### Applications

| Application | Platform | Description |
|-------------|----------|-------------|
| Operator Console | Web | Management and monitoring interface |
| Desktop Shell | Desktop | Native desktop application (Tauri) |
| Mobile Client | iOS/Android | Cross-platform mobile app (Expo) |
| Quest 3 App | VR/AR | Meta Quest 3 spatial computing app |

### Infrastructure

- **Database**: PostgreSQL with vector search capabilities
- **Cache**: Redis for fast data access
- **Model Inference**: Ollama cluster with auto-scaling
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker Compose + Kubernetes

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.10+ (for local development)
- Git
- 8GB RAM minimum (16GB recommended)

### Automated Setup (Recommended)

#### Windows
```powershell
# 1. Run prerequisite checker
.\scripts\install-prerequisites.ps1

# 2. Set up environment
.\scripts\setup-environment.ps1

# 3. Start services
.\scripts\deploy.bat dev

# 4. Run migrations
.\scripts\deploy.bat migrate

# 5. Pull Ollama models
.\scripts\pull-ollama-models.ps1
```

#### Linux/Mac
```bash
# 1. Set up environment
./scripts/deploy.sh dev

# 2. Run migrations
./scripts/deploy.sh migrate

# 3. Pull Ollama models
docker exec -it synthos-ollama bash
ollama pull llama2 mistral neural-chat
exit
```

### Manual Setup

1. **Clone the repository**
```bash
git clone https://github.com/fuzzynetwork1989-alt/Synthos-OS.git
cd Synthos-OS
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Install dependencies**
```bash
pip install -e .
cd apps/mobile-client && npm install && cd ../..
```

4. **Start services**
```bash
docker-compose up -d
```

5. **Run migrations**
```bash
docker-compose exec postgres psql -U synthos -d synthos_os -f /docker-entrypoint-initdb.d/001_create_memory_tables.sql
```

See [Environment Setup Guide](docs/operations/environment-setup.md) for detailed instructions.

## Deployment

### Development
```bash
./scripts/deploy.sh dev
```

### Production
```bash
./scripts/deploy.sh prod
```

### Kubernetes
```bash
kubectl apply -f infra/kubernetes/
kubectl apply -f infra/ollama-cluster/kubernetes/
```

See [Deployment Guide](docs/operations/deployment-guide.md) for detailed deployment instructions.

## Documentation

- [Architecture Overview](docs/architecture/overview.md) - System architecture and design
- [Recursive Self-Improvement](docs/architecture/recursive-self-improvement.md) - RSI system details
- [Autonomous RSI Capabilities](docs/architecture/autonomous-rsi-capabilities.md) - Cognitive DNA system
- [Self-Organizing Intelligence](docs/architecture/self-organizing-intelligence.md) - Future vision
- [Deployment Guide](docs/operations/deployment-guide.md) - Complete deployment instructions
- [API Documentation](docs/api/) - API reference and examples

## Key Features

### 🧠 Cognitive Architecture
- 21-layer cognitive architecture
- Multimodal perception and input processing
- Persistent memory with vector search
- Advanced reasoning and planning
- Tool routing and execution

### 🔄 Autonomous Self-Improvement
- Cognitive DNA evolution system
- Meta-RSI for strategy optimization
- Self-triggering improvement cycles
- Adaptive resource management
- Multi-layer safety constraints

### 🛡️ Safety and Governance
- Constitutional constraints (19 fundamental rules)
- Goal drift monitoring
- Emergency stop capabilities
- Human oversight always maintained
- Comprehensive audit trails

### 🌐 Cross-Platform Support
- Web-based operator console
- Native desktop application
- iOS and Android mobile apps
- Meta Quest 3 VR/AR support
- API-first design for integration

### ⚡ Performance
- Local-first architecture
- Ollama cluster with auto-scaling
- Efficient caching with Redis
- Vector search for memory retrieval
- Optimized model routing

## Development

### Project Structure
```
Synthos-OS/
├── apps/              # Application interfaces
├── services/          # Backend microservices
├── infra/             # Infrastructure configuration
├── docs/              # Documentation
├── migrations/        # Database migrations
├── scripts/           # Deployment and utility scripts
└── tests/             # Test suites
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

TBD

## Acknowledgments

Built with inspiration from:
- SAHOO: Safeguarded Alignment for High-Order Optimization
- Constitutional Self-Modification frameworks
- Geneclaw: Safe, Auditable Self-Evolving Agent Framework
- Self-Healing Harness for Runtime Oversight

## Contact

- GitHub: https://github.com/fuzzynetwork1989-alt/Synthos-OS
- Issues: https://github.com/fuzzynetwork1989-alt/Synthos-OS/issues
