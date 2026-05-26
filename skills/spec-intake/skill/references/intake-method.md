# Intake Method

Use this reference when the user gives a raw idea, one-line concept, rough notes, or an incomplete PRD request.

## Classify Source Material

Every extracted statement must become one of:

| Class | Meaning | Contract handling |
| --- | --- | --- |
| Explicit fact | The user or supplied material states it directly. | Create/update object with `SRC.source_type=user_input` or `user_document`. |
| Confirmed fact | The user confirms it during clarification. | Create `SRC.source_type=user_confirmation`; add trace relation `confirmed_by`. |
| Bounded inference | Combines known facts without adding an unsupported product claim. | Keep draft; add `TRACE.relation=inferred_from`; add `ASM` or `Q` if it affects scope, acceptance, execution, risk, or stop behavior. |
| Assumption | Plausible but unconfirmed. | Create `ASM`; block ready output if material. |
| Open question | Needs human/source decision. | Create `Q`; block affected target when it changes scope, validation, execution, risk, or priority. |

Never write internal `confidence`, `candidate_score`, or `question_priority` into the contract.

## Parse The Idea

Extract:

- roles and users
- problem or failure scenario
- intended outcome
- solution behavior
- input data
- output deliverables
- constraints, risks, permissions, or forbidden actions
- success signals

Map them to candidate objects:

| Signal | Primary objects |
| --- | --- |
| Product name, summary, value | `CORE`, `META` |
| User or role | `USER`, `SCOPE` |
| Problem or pain | `CORE`, `REQ`, `RISK` |
| MVP behavior | `SCOPE`, `REQ`, `EXE`, `FLOW` |
| Input | `IN`, `DATA`, `DCT`, `STOP` |
| Output | `OUT`, `DONE`, `AC` |
| Success standard | `AC`, `MET`, `VER`, `DONE` |
| Boundary | `OOS`, `BAR`, `STOP`, `PHASE` |
| Unknown | `Q`, `ASM` |

## Ask Questions

Ask at most three questions per round. Prefer questions that unblock the highest-value target:

1. user, problem, and value
2. MVP scope and non-scope
3. acceptance and success criteria
4. input, permissions, output, stop conditions
5. execution and verification details

Use open, concrete, non-leading wording:

- "Who is the first user, and what do they do today when this problem happens?"
- "What is the smallest first version that would still be useful?"
- "What result would make you say this is good enough?"
- "Which inputs can the agent rely on, and what missing input should stop execution?"
- "Which actions require explicit human confirmation?"

## Output Decision

Ask first when:

- user/problem/value are too unclear to model `CORE`
- MVP scope cannot be separated from future scope
- sensitive data, permissions, automation, or external writes lack stop rules
- the user requests execution-ready Agent PRD but `IN`, `EXE`, `VER`, `OUT`, `STOP`, or `DONE` cannot be traced

If the user asks for a draft anyway, produce a draft or blocked envelope with `Q`, `ASM`, `STOP`, `GATE`, and `next_actions`; do not mark affected targets ready.
