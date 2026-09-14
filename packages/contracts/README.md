# Synthos-OS Contracts

Shared contracts, types, and interfaces for the Synthos-OS platform.

## Purpose

This package contains:
- Common Pydantic models and schemas
- API error response standards
- Shared request/response types
- Protocol definitions for inter-service communication
- Domain models used across multiple services

## Usage

```python
from synthos_contracts.api import ErrorResponse, APIResponse
from synthos_contracts.types import UserId, TaskId, MemoryId
```
