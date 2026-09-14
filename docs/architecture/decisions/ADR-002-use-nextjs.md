# ADR-002 - Use Next.js for Operator Console

## Status
Accepted

## Context
Synthos-OS requires a frontend framework that:
- Supports React and TypeScript
- Provides server-side rendering for performance
- Has good developer experience and tooling
- Supports desktop and mobile deployment
- Integrates well with backend APIs
- Has strong ecosystem and community support

## Decision
Use Next.js with TypeScript for the operator console and user-facing interfaces.

## Rationale
- Server-side rendering improves initial load performance and SEO
- TypeScript provides type safety across the application
- File-based routing simplifies navigation structure
- API routes allow backend integration within the same framework
- Strong ecosystem with UI component libraries
- Supports desktop (Electron/Tauri) and mobile (React Native) deployment
- Built-in optimization and image handling
- Excellent developer experience with hot reload

## Consequences
- **Positive:** Fast development with file-based routing
- **Positive:** TypeScript prevents many runtime errors
- **Positive:** Built-in optimization and performance
- **Positive:** Can deploy as web, desktop, or mobile from same codebase
- **Negative:** Next.js specific learning curve (mitigated by strong documentation)
- **Negative:** Server-side rendering adds complexity (mitigated by API routes for data fetching)
- **Negative:** Bundle size can grow large (mitigated by code splitting)

## Alternatives Considered
- **React:** More control but requires more setup (routing, SSR, optimization)
- **Vue.js:** Simpler learning curve but smaller ecosystem
- **Svelte:** Better performance but smaller ecosystem and tooling
- **Angular:** More opinions and structure but steeper learning curve
