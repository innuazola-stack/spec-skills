# HLD Methodology Reference

This reference distills architecture-documentation and technical-writing practices into rules for writing professional Simplified Chinese software product HLD documents. Use these source IDs for methodology citations only. Product facts still require project evidence markers.

## Source Map

| ID | Source | HLD-Relevant Principle |
| --- | --- | --- |
| [M01] | ISO/IEC/IEEE 42010 Architecture Descriptions, https://www.iso-architecture.org/ieee-1471/ads/ | An architecture description identifies the system of interest and can include scope, context, version, status, glossary, references, and other supplementary information. |
| [M02] | ISO/IEC/IEEE 42010 Conceptual Model, https://www.iso-architecture.org/ieee-1471/cm/ | Architecture descriptions should address stakeholders, concerns, viewpoints, views, models, correspondences, decisions, and rationale. |
| [M03] | SEI Views and Beyond factsheet, https://resources.sei.cmu.edu/asset_files/factsheet/2018_010_001_513864.pdf | Architecture documentation should use views and view-specific guidance so different stakeholder concerns can be understood and reviewed. |
| [M04] | arc42 Template Overview, https://arc42.org/overview | A pragmatic architecture document covers goals, constraints, context, solution strategy, building blocks, runtime, deployment, crosscutting concepts, decisions, quality requirements, risks, and glossary. |
| [M05] | C4 Model, https://c4model.info/ | Use hierarchical architecture views for audience-specific communication: system context, container, component, and code views, plus deployment and dynamic views when useful. |
| [M06] | AWS Well-Architected Framework, https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html | Architecture quality should evaluate decisions against reliability, security, efficiency, cost, sustainability, and operational concerns. |
| [M07] | Azure Well-Architected Framework, https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework | Architecture decisions must balance quality pillars, business requirements, risks, and tradeoffs. |
| [M08] | Google Cloud Well-Architected Framework, https://docs.cloud.google.com/architecture/framework | Architecture design should organize guidance around operational excellence, security/privacy/compliance, reliability, cost, performance, and sustainability. |
| [M09] | Martin Fowler, Architecture Decision Record, https://martinfowler.com/bliki/ArchitectureDecisionRecord.html | Important architecture decisions should record context, decision, and significant ramifications in concise records. |
| [M10] | MADR, Markdown Architectural Decision Records, https://adr.github.io/madr/ | Architecture-significant decisions should be captured in a lean, structured form with rationale. |
| [M11] | Diátaxis Documentation Framework, https://diataxis.fr/ | Documentation should stay focused on reader needs and avoid mixing incompatible documentation purposes. |
| [M12] | Google Developer Documentation Style Guide Highlights, https://developers.google.com/style/highlights | Technical documentation should be clear, consistent, accessible, and organized with appropriate lists, headings, and formatting. |
| [M13] | Microsoft Style Guide: Scannable Content, https://learn.microsoft.com/en-us/style-guide/scannable-content/ | Long technical content should lead with important information, use short headings, tables, and consistent structure for scanability. |
| [M14] | GitHub architecture-decision-record repository, https://github.com/architecture-decision-record/architecture-decision-record | ADR collections show practical templates and examples for decision context, consequences, naming, and organization. |

## HLD Quality Principles

| Principle | Writing Rule | Source Basis |
| --- | --- | --- |
| System boundary first | State the system of interest, environment, actors, upstream/downstream systems, and excluded scope before explaining internals. | [M01], [M02], [M04], [M05] |
| Stakeholder concerns drive structure | Include only sections that answer real stakeholder concerns: business value, operability, security, reliability, performance, data, integration, delivery, and risk. | [M02], [M03], [M11] |
| Multiple views, one coherent architecture | Use separate views for context, static structure, runtime behavior, deployment, data, security, and operations; keep naming and relationships consistent across views. | [M02], [M03], [M04], [M05] |
| Decisions need rationale | For architecture-significant decisions, record the chosen option, alternatives considered, rationale, tradeoffs, and consequences. | [M02], [M04], [M09], [M10], [M14] |
| Quality attributes must be testable | Express reliability, security, performance, cost, operability, scalability, and maintainability goals as measurable or reviewable targets whenever evidence allows. | [M04], [M06], [M07], [M08] |
| Tradeoffs are first-class content | Make tradeoffs explicit instead of implying the chosen design is universally optimal. | [M06], [M07], [M08], [M09] |
| Risk and technical debt belong in the HLD | Record known risks, debt, uncertainty, and mitigation ownership so reviewers can make informed decisions. | [M04], [M06], [M07] |
| Reader-oriented documentation | Use a concise, formal, human-readable structure. Prefer tables and diagrams where they reduce cognitive load. | [M11], [M12], [M13] |
| Evidence over assertion | Every material product or architecture claim must trace to project evidence. Methodology sources justify structure, not product truth. | [M01], [M02], [M09], [M12] |

## View Selection Guide

| View | Include When | Preferred Form |
| --- | --- | --- |
| Context view | The HLD needs to explain users, external systems, or system boundary. | Mermaid flowchart or C4-style context diagram plus short prose. |
| Container/module view | The HLD needs to explain major deployable units, services, modules, or data stores. | Mermaid flowchart/table with responsibilities, interfaces, owners, and evidence. |
| Runtime view | The HLD needs to explain critical flows, failure behavior, authentication, async processing, or operational scenarios. | Mermaid sequence diagram/state diagram plus assumptions and failure handling. |
| Deployment view | Infrastructure, environments, regions, networks, scaling, or release topology matter. | Mermaid flowchart/deployment diagram plus environment table. |
| Data view | Data ownership, lifecycle, storage, lineage, privacy, or consistency matters. | Data entity table, data-flow diagram, retention and classification table. |
| Security view | Authentication, authorization, secrets, threat boundaries, compliance, or privacy matter. | Trust-boundary diagram, control matrix, threat/mitigation table. |
| Operations view | Observability, alerting, SLOs, runbooks, rollback, or incident response matter. | SLO table, monitoring matrix, release/rollback sequence. |

## Decision Record Pattern

Use this compact pattern inside the HLD when a separate ADR file is not requested:

| Field | Requirement |
| --- | --- |
| Decision ID | Stable ID such as `ADR-HLD-001`. |
| Decision | One clear sentence naming the chosen approach. |
| Context | Source-backed situation, constraint, or problem. |
| Alternatives | Practical alternatives that were actually relevant. |
| Rationale | Why the chosen approach best satisfies the documented goals. |
| Tradeoffs | Costs, limitations, risks, or future constraints accepted by this choice. |
| Consequences | Expected effect on implementation, operations, security, cost, and evolution. |
| Evidence | Project source markers and methodology markers. |

## Writing Style

- Lead with conclusions; place supporting details after the reader understands the point.
- Use short headings and consistent section names.
- Use tables for comparison, inventories, traceability, decisions, risks, and ownership.
- Use Mermaid diagrams only when relationships or flows are clearer visually than in prose.
- Use LaTeX only for formulas such as capacity estimates, scoring, or availability calculations.
- Keep tone formal and natural. Avoid slogans, ornate language, and generic architecture theory.
- Remove content that does not serve the HLD purpose.
