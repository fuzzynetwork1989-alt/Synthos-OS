# ADR-003 - Use PostgreSQL for Production Database

## Status
Accepted

## Context
Synthos-OS requires a database that:
- Supports complex relational queries and transactions
- Provides ACID compliance for data integrity
- Supports full-text search and extensions
- Has strong JSON support for flexible schemas
- Supports horizontal scaling when needed
- Has mature tooling and operational experience
- Supports local development and production deployments

## Decision
Use PostgreSQL as the primary database for production deployments, with SQLite for local development.

## Rationale
- ACID compliance ensures data integrity for transactions
- Excellent JSON support with `pgjson` for flexible schemas
- Full-text search with `pg_trgm` and `pgvector` extensions
- Mature ecosystem with excellent tooling and monitoring
- Strong replication and partitioning support for scaling
- SQLite provides lightweight local development without infrastructure
- Extensive experience in production environments
- Open-source with strong community support

## Consequences
- **Positive:** Strong data integrity with ACID compliance
- **Positive:** Flexible schemas with JSON support
- **Positive:** Built-in full-text search reduces need for separate search engine
- **Positive:** `pgvector` enables vector search for retrieval
- **Positive:** Mature tooling and operational practices
- **Negative:** PostgreSQL requires more resources than SQLite (mitigated by local SQLite for development)
- **Negative:** More complex setup than NoSQL alternatives (mitigated by Docker Compose)
- **Negative:** Vertical scaling limits (mitigated by partitioning and read replicas)

## Alternatives Considered
- **MongoDB:** Better schema flexibility but weaker ACID guarantees
- **MySQL:** Good alternative but weaker JSON support and extensions
- **SQLite-only:** Simplest but lacks production features and scaling
- **DynamoDB:** Scales well but expensive and less control
