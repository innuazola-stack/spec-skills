# Spec Intake Implementation Plan

## Date

2026-05-26

## Target Dev Root

`skills/spec-intake`

## Target Skill Source Path

`skills/spec-intake/skill`

## Goal

Create a Codex skill that guides idea intake into contract-backed PRDs and HLD.

## Files To Create Or Update

`SKILL.md`, `agents/openai.yaml`, four reference files, validator scripts, lifecycle docs, and blocked fixture package.

## Ownership And Sequence

1. Runtime trigger and workflow.
2. Intake/output/task/gate references.
3. Validator scripts.
4. Fixture package.
5. Validation commands.

## Contracts To Preserve

Contract-first facts, sibling PRDs, honest unknowns, execution-ready gate, and blocked HLD invariants.

## Risks During Implementation

Over-broad trigger wording, bloated `SKILL.md`, validator pretending to judge semantic quality, and untested fixture assumptions.
