# Rust Detailed Design Checklist

Use this checklist when the target project uses Rust.

## Crate And Module Boundaries

- Workspace and crate ownership.
- Public module API vs private internals.
- Trait boundaries for replaceable components.
- Feature flags and platform-specific code, if relevant.
- CLI, service, library, adapter, or integration entrypoints.

## Data Flow And Types

- Domain structs/enums and field meanings.
- Serialization/deserialization formats.
- Validation boundaries.
- Borrowed vs owned data expectations.
- Conversion points between external DTOs and internal domain types.

## Control Flow

- Entry trigger.
- Ordered execution steps.
- Branches and failure paths.
- Retry, cancellation, timeout, and idempotency behavior.
- Interaction with external tools, files, APIs, or processes.

## Errors And Diagnostics

- Error enum or error handling style.
- Recoverable vs fatal failures.
- User-facing diagnostics.
- Logging/tracing spans and evidence artifacts.
- Exit codes for CLI tools when applicable.

## State And Persistence

- In-memory state lifecycle.
- File/database/cache ownership.
- Atomicity and consistency expectations.
- Migration or compatibility needs.
- Cleanup behavior on failure.

## Async And Concurrency

- Runtime choice such as Tokio, async-std, or synchronous execution.
- Task boundaries and cancellation.
- Shared state protections.
- Backpressure and bounded queues.
- Determinism requirements for tests and acceptance.

## Testing And Acceptance

- Unit tests for pure logic and type conversions.
- Integration tests for real interfaces.
- Fixture strategy.
- Golden/snapshot outputs when applicable.
- Acceptance command, preconditions, expected artifacts, mechanical checks, and failure criteria.

If any checklist item is material but unsupported by PRD/HLD or target-project evidence, mark it as a blocker or required design decision.
