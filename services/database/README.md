# Synthos-OS Database Configuration

Database configuration and migration management for Synthos-OS, supporting both SQLite for local development and PostgreSQL for production.

## Features

- Support for SQLite (local development) and PostgreSQL (production)
- Async database sessions with SQLAlchemy 2.0
- Alembic migrations for schema management
- Connection pooling for production databases
- Type-safe configuration with Pydantic

## Installation

```bash
# Install in development mode
cd services/database
pip install -e .
```

## Configuration

Set environment variables in `.env`:

```bash
# Database type (sqlite or postgresql)
DATABASE_TYPE=sqlite

# SQLite settings (when DATABASE_TYPE=sqlite)
SQLITE_PATH=./synthos.db

# PostgreSQL settings (when DATABASE_TYPE=postgresql)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=synthos
POSTGRES_PASSWORD=synthos
POSTGRES_DATABASE=synthos

# Connection pool settings
POOL_SIZE=5
MAX_OVERFLOW=10
POOL_TIMEOUT=30
POOL_RECYCLE=3600
```

## Usage

### Using the Database Session

```python
from synthos_database.session import get_session, Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

async def create_user(name: str):
    async with get_session() as session:
        user = User(name=name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
```

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

### Development vs Production

**Local Development (SQLite):**
- Default configuration
- No external dependencies
- Easy to reset (delete database file)
- SQL echoing enabled for debugging

**Production (PostgreSQL):**
- Set `DATABASE_TYPE=postgresql`
- Requires PostgreSQL server
- Connection pooling for performance
- Proper persistence and scaling

## Database URL Formats

**SQLite:**
- Async: `sqlite+aiosqlite:///./synthos.db`
- Sync (migrations): `sqlite:///./synthos.db`

**PostgreSQL:**
- Async: `postgresql+asyncpg://user:pass@host:port/db`
- Sync (migrations): `postgresql://user:pass@host:port/db`

## Architecture

The database configuration is part of Layer 17 (Persistence) of the Synthos-OS architecture.

## TODO

- Add database backup and restore utilities
- Add migration testing
- Add database seeding for development
- Add connection health checks
- Add migration rollback testing
