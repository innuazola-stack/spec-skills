# Brief Methodology Reference

This reference distills product brief, product design brief, UX/design brief, technical spec, software design document, and technical writing guidance into reusable rules for writing professional Simplified Chinese briefs. Use source IDs for methodology citations only. Product facts still require project evidence markers.

## Source Map

| ID | Source | Brief-Relevant Principle |
| --- | --- | --- |
| [M01] | UXPin, "How to Write a Good Design Brief?", https://www.uxpin.com/studio/blog/design-brief/ | Distinguish design briefs from detailed specs; include target audience, research needs, accessibility, brand, assets, formats, and technical limits. |
| [M02] | Ignitec, "How to write an effective product design brief", https://www.ignitec.com/insights/how-to-write-an-effective-product-design-brief/ | Put end users and problems at the center, keep the brief short, avoid prescribing solutions too early, and define timescales and deliverables. |
| [M03] | Truss Project Toolkit, "Product brief template", https://trussworks.github.io/project-toolkit/docs/product-brief-template.html | Product briefs set direction after discovery and before design/development; they are not PRDs or detailed acceptance specs. |
| [M04] | Asana, "Product Brief Template: How to Write One + Steps", https://asana.com/resources/product-brief-template | Product briefs align team scope, goals, direction, target audience, features, context, metrics, resources, and milestones; effective briefs are concise and scannable. |
| [M05] | Atlassian, "What is a Product Requirements Document (PRD)?", https://www.atlassian.com/agile/product-management/requirements | PRDs and adjacent requirement artifacts should align purpose, user needs, success criteria, assumptions, user stories, design, and out-of-scope items without over-specifying. |
| [M06] | Atlassian, "How to Create a Software Design Document", https://www.atlassian.com/work-management/knowledge-sharing/documentation/software-design-document | Software design documents bridge product intent and implementation through architecture, components, data, interfaces, assumptions, dependencies, and team review. |
| [M07] | Stack Overflow Blog, "A practical guide to writing technical specs", https://stackoverflow.blog/2020/04/06/a-practical-guide-to-writing-technical-specs/ | Technical specs force problem examination before coding, expose scope, support peer feedback, and reduce repeated design explanations. |
| [M08] | Notion, "How to write a tech spec step by step", https://www.notion.com/use-case/project-management/how-to-write-a-tech-spec | Good tech specs translate product intent into buildable decisions, constraints, tradeoffs, assumptions, and execution-linked updates. |
| [M09] | Diataxis documentation framework, https://diataxis.fr/ | Documents should be organized around reader needs and should not mix incompatible purposes. |
| [M10] | Google Developer Documentation Style Guide Highlights, https://developers.google.cn/style/highlights | Technical writing should be clear, accessible, active, consistently structured, and formatted with the right list and code conventions. |
| [M11] | Microsoft Style Guide, "Scannable content", https://learn.microsoft.com/en-us/style-guide/scannable-content/ | Help readers find what they need quickly by leading with important information and using headings, lists, tables, and short paragraphs. |
| [M12] | Gerrit Code Review, "Design Docs", https://gerrit-review.googlesource.com/Documentation/dev-design-docs.html | Design documents should support iterative review, separate unrelated issues, and give governance bodies enough context to accept or reject scope. |
| [M13] | Figma, "How to create a design brief", https://www.figma.com/resource-library/how-to-create-a-design-brief/ | Design briefs clarify scope, goals, background, target audience, requirements, timelines, budget, deliverables, collaboration, and sign-off. |
| [M14] | Lucidchart, "How to Create Software Design Documents", https://www.lucidchart.com/blog/how-to-create-software-design-documents | Software design docs should define functionality, UI, goals, milestones, prioritization, current and proposed solutions, timeline, visuals, feedback, and living updates. |

## Distilled Brief Logic

| Principle | Writing Rule | Source Basis |
| --- | --- | --- |
| Briefs unlock decisions | Start by stating the decision, alignment, approval, or handoff the brief is meant to enable. | [M03], [M04], [M08], [M12] |
| Problem before solution | Explain the user, business, design, or technical problem before listing features, screens, components, or implementation choices. | [M02], [M04], [M05], [M07] |
| Right-sized detail | Keep the brief shorter than a PRD/HLD/spec and move deep details into linked artifacts. | [M03], [M04], [M09], [M11] |
| Audience-specific content | Select sections according to reader needs: product direction, design execution, technical feasibility, or cross-functional governance. | [M06], [M08], [M09], [M13] |
| Evidence over assertion | Separate facts from assumptions and cite sources for claims about users, market, scope, constraints, metrics, dependencies, risks, and dates. | [M05], [M07], [M10] |
| Constraints are design material | Surface budget, timeline, stack, accessibility, legal, data, security, design-system, and integration constraints early. | [M01], [M08], [M13] |
| Avoid premature prescription | In discovery and design briefs, state desired outcomes and constraints without dictating a finished solution unless the solution is already decided. | [M02], [M03], [M08] |
| Make success testable | Include measurable outcomes, acceptance signals, review criteria, launch metrics, or validation plan appropriate to the brief stage. | [M04], [M05], [M07], [M08] |
| Tradeoffs are required for technical briefs | Explain options, rationale, rejected alternatives, operational impact, and accepted risks. | [M06], [M07], [M08], [M14] |
| Scannability is a quality attribute | Use short headings, tables, bullets, and leading conclusions so stakeholders can review quickly. | [M04], [M10], [M11] |
| Collaboration path matters | Name owners, reviewers, decision makers, milestones, sign-off path, and unresolved questions. | [M12], [M13], [M14] |
| Living artifact discipline | Record version/status and update the brief when decisions, constraints, scope, or timelines change. | [M04], [M08], [M12], [M14] |

## Brief Type Selection

| Brief Type | Use When | Avoid |
| --- | --- | --- |
| Product brief | The team needs strategic alignment before PRD, design, build, launch, or executive review. | Low-level implementation detail, exhaustive acceptance criteria, full test plan. |
| Product design brief | Product and design need a shared frame for user problem, constraints, deliverables, review path, and design exploration. | Prescribing exact UI if discovery is still open; hiding feasibility constraints. |
| UX/research brief | The team needs to define research questions, participants, decision use, scope, timeline, and evidence gaps. | Turning research into conclusions before data exists. |
| Technical brief | Engineering needs a concise proposal or decision frame before a full tech spec, HLD, RFC, or implementation plan. | Generic architecture essays; implementation checklists without tradeoff rationale. |
| Hybrid brief | Product, design, and engineering need one shared artifact for a feature, initiative, or kickoff. | Blurring section purposes until nobody knows what is decided. |

## Recommended Content Model

| Module | Purpose | Typical Expression |
| --- | --- | --- |
| Revision/status | Shows whether the brief is draft, ready for review, approved, or superseded. | Table |
| Decision summary | States what decision the brief enables and the recommended direction. | Short prose |
| Background | Explains why this work matters now. | Prose with source markers |
| Problem and audience | Defines affected users, customers, operators, teams, or systems. | Persona/scenario table |
| Goals and non-goals | Clarifies target outcomes and prevents scope creep. | Table |
| Evidence and assumptions | Separates known facts from guesses. | Table |
| Scope and constraints | Defines included, excluded, fixed, flexible, and unknown boundaries. | Table |
| Recommended direction | Explains the proposed product/design/technical path. | Prose plus options table |
| Alternatives and tradeoffs | Makes judgment visible, especially for technical or strategic briefs. | Comparison table |
| Success criteria | Defines metrics, acceptance signals, review criteria, or validation checks. | Table |
| Deliverables and handoff | Names output artifacts, formats, owners, milestones, review path, and next document. | Table |
| Risks and open questions | Makes unresolved issues actionable. | Table |
| References | Lists all cited project and methodology sources. | Table |

## Evaluation Standards

| Dimension | High-Quality Brief Standard |
| --- | --- |
| Decision clarity | A reader can say what decision is being requested, what is recommended, and who decides. |
| Problem grounding | The brief explains the problem from user/business/system evidence before describing the solution. |
| Scope control | In scope, out of scope, constraints, assumptions, and dependencies are explicit. |
| Audience fit | Detail level matches the brief type and readers; deeper PRD/HLD/spec content is linked, not duplicated. |
| Evidence integrity | Material claims have source markers; assumptions and unknowns are labeled honestly. |
| Success definition | Outcomes, metrics, acceptance signals, or validation steps are specific enough to review. |
| Technical feasibility | Relevant stack, architecture, integration, data, security, privacy, accessibility, operations, and delivery constraints are visible. |
| Tradeoff reasoning | Important options, alternatives, costs, and consequences are not hidden. |
| Handoff readiness | Owners, deliverables, milestone expectations, reviewers, and next artifacts are clear. |
| Scannability | The document uses short sections, tables, bullets, and front-loaded conclusions. |

## Writing Style

- Lead with the answer, then provide supporting evidence.
- Prefer concrete nouns, named owners, exact dates when known, and measurable criteria.
- Use "已知事实 / 假设 / 待确认" to separate confidence levels.
- Use "固定约束 / 可协商约束 / 未知约束" when constraints shape design or technical choices.
- Keep product language outcome-oriented, design language user- and constraint-oriented, and technical language decision- and tradeoff-oriented.
- Avoid slogans, vague adjectives, and unfounded certainty.
