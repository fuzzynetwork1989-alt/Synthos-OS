# ADR-004 - Use Ollama as Primary Local Model Runtime

## Status
Accepted

## Context
Synthos-OS requires a local model runtime that:
- Supports open-weight models for privacy and offline operation
- Provides easy local deployment and management
- Integrates well with Python backend
- Supports model selection and versioning
- Has good performance on consumer hardware
- Supports multiple model formats and quantization
- Provides API compatibility for easy integration

## Decision
Use Ollama as the primary local model runtime for Synthos-OS, with support for LM Studio and Hugging Face as secondary options.

## Rationale
- Simple installation and management of local models
- REST API for easy integration with backend services
- Supports multiple model formats (GGUF, etc.)
- Good performance on consumer hardware
- Active development and growing model library
- Open-source with permissive licensing
- Supports streaming responses for real-time interaction
- Modelfile system for custom model configuration
- Adapter support for fine-tuned models

## Consequences
- **Positive:** Easy local deployment without complex infrastructure
- **Positive:** Good performance on consumer hardware
- **Positive:** Growing ecosystem of supported models
- **Positive:** API compatibility simplifies integration
- **Positive:** Modelfile system for custom configurations
- **Negative:** Limited to models available in Ollama library (mitigated by custom models)
- **Negative:** Hardware requirements for larger models (mitigated by quantization)
- **Negative:** Limited distributed serving (mitigated by local-first design)

## Alternatives Considered
- **LM Studio:** Good GUI but more complex API integration
- **Hugging Face Transformers:** More flexible but requires more engineering
- **LocalLLM:** More configurable but higher complexity
- **vLLM:** Better performance but more complex setup
