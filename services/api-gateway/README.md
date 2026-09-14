# Synthos-OS API Gateway

The API Gateway provides the main entry point for the Synthos-OS platform, handling authentication, routing, health checks, and structured logging.

## Features

- Health check endpoints for database, Redis, and Ollama
- Structured JSON logging with request tracking
- Configuration validation and warnings
- CORS support for frontend integration
- Request ID tracking for distributed tracing
- Comprehensive error handling

## Installation

```bash
# Install in development mode
cd services/api-gateway
pip install -e .
```

## Running

```bash
# Direct run
python -m synthos_api_gateway.main

# Or with uvicorn
uvicorn synthos_api_gateway.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | Synthos-OS API Gateway |
| `APP_VERSION` | Application version | 0.1.0 |
| `ENVIRONMENT` | Environment (development/staging/production) | development |
| `DEBUG` | Debug mode | False |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `CORS_ORIGINS` | CORS origins (comma-separated) | http://localhost:3000,http://localhost:5173 |
| `DATABASE_URL` | Database connection string | sqlite:///./synthos.db |
| `REDIS_URL` | Redis connection string | redis://localhost:6379/0 |
| `SECRET_KEY` | JWT secret key | (development default) |
| `LOG_LEVEL` | Logging level | INFO |
| `LOG_FORMAT` | Log format (json/console) | json |

## API Endpoints

### Health Checks

- `GET /api/v1/health` - Comprehensive health check
- `GET /api/v1/health/ready` - Readiness check
- `GET /api/v1/health/live` - Liveness check

### Root

- `GET /` - Service information
- `GET /api/v1` - API information

## Architecture

The API Gateway is part of Layer 2 (Identity) and Layer 12 (Permissions) of the Synthos-OS architecture.

## TODO

- Implement actual database connectivity check
- Implement actual Redis connectivity check
- Implement actual Ollama connectivity check
- Add authentication and authorization middleware
- Add rate limiting
- Add request validation
- Add audit logging
