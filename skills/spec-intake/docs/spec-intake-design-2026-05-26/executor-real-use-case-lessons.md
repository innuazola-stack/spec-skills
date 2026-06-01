# Executor Real Use Case Lessons

Date: 2026-05-27

## Summary

The executor real run exposed a repeatable workflow gap. Stage 1 initially captured the product and basic adapter idea, but it did not reliably extract the full execution topology needed for an execution-ready Agent PRD and an information-dense Human PRD. Stage 2 then rendered structurally valid PRDs that still under-described the actual adapter execution and monitoring loop.

## Interaction Pattern

1. The user provided an executor idea with task description input and an existing adapter.
2. Stage 1 asked closed-choice questions for invocation, output, and completion authority.
3. Stage 2 rendered PRDs that passed structural validation but were too abstract around adapter execution.
4. User review identified missing adapter execution and monitoring requirements.
5. The requirement table was revised first, adding explicit execution/monitoring requirements.
6. User review then required concrete adapter methods, idle-state progress judgment, and mechanical delivery checks.
7. Local adapter documentation was read and registered as source evidence before rerendering PRDs.

## Root Cause

The workflow treated "implementation approach" as a single broad readiness category. For execution-like ideas, that is not hard enough. The workflow must separately capture:

- external component sources and public interface boundaries
- execution loop and runtime states
- mechanical observation versus subjective judgment
- evidence chain
- mechanical checks before semantic completion or human approval

## Generalized Fix

The fix is methodological, not executor-specific:

- Stage 1 now treats execution topology as required support for executor, agent, adapter, CLI, automation, scheduler, and tool-orchestration ideas.
- Stage 1 must register available component documentation or implementation as source evidence before making method-level claims.
- Stage 2 Agent PRD must render non-empty implementation-model refs into concrete execution topology.
- Stage 2 Human PRD must summarize material execution topology at human-review depth instead of hiding it behind generic implementation wording.
- The validator now blocks execution-like `proceed_without_questions` packages that lack control flow, modules, or technical decisions, and blocks execution-ready Agent PRDs that omit non-empty implementation-model refs.

## Non-Goals

This lesson does not hard-code `ClaudeTmuxAdapter`, `opencalw`, or executor behavior into the workflow. Those remain examples of a broader execution-like pattern.
