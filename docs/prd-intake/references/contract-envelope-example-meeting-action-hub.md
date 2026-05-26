# Contract Envelope Example: Meeting Action Hub

This fixture is a minimal smoke fixture for the audit envelope shape used by the Meeting Action Hub examples. It validates envelope mechanics, object payload shape, traceability, object indexing, and gate reporting with a compact subset of objects. It does not claim to cover every canonical ID that appears in the full Human PRD and Agent PRD display examples; a full conformance fixture must do that explicitly.

```json
{
  "intake_id": "prd-intake-meeting-action-hub-example",
  "contract_version": "1.8",
  "maturity_level": "L4",
  "render_status": {
    "human_prd": "review_ready",
    "agent_prd": "execution_ready",
    "blocked_reasons": []
  },
  "canonical_contract": {
    "summary": {
      "product": "Meeting Action Hub",
      "current_phase": "PHASE-001"
    },
    "objects": {
      "CORE-001": {
        "type": "CORE",
        "payload": {
          "id": "CORE-001",
          "product_name": "Meeting Action Hub",
          "one_line_summary": "Turn authorized meeting notes into reviewable action items.",
          "target_users": ["USER-001"],
          "personas": ["USER-001"],
          "problem_statement": "Teams lose action ownership after meetings.",
          "value_proposition": "Create a traceable action list without committing tasks automatically.",
          "source_refs": ["SRC-001"],
          "assumption_refs": [],
          "status": "confirmed"
        }
      },
      "REQ-001": {
        "type": "REQ",
        "payload": {
          "id": "REQ-001",
          "title": "Extract action items",
          "description": "Extract owner, task, due date, and evidence excerpt from authorized meeting input.",
          "user_value": "Reviewers can confirm meeting follow-ups quickly.",
          "priority": "must",
          "phase": "PHASE-001",
          "scope_ref": "SCOPE-001",
          "acceptance_criteria": ["AC-001"],
          "source_refs": ["SRC-001"],
          "status": "confirmed"
        }
      },
      "AC-001": {
        "type": "AC",
        "payload": {
          "id": "AC-001",
          "requirement_id": "REQ-001",
          "criterion": "Every exported action item includes an owner, task text, and source excerpt.",
          "verification_method": "inspection",
          "blocking": true
        }
      },
      "STOP-001": {
        "type": "STOP",
        "payload": {
          "id": "STOP-001",
          "condition": "meeting_transcript is missing",
          "reason": "Action extraction would be unsupported.",
          "status": "defined",
          "required_human_action": "Provide authorized transcript or meeting notes.",
          "related_refs": ["IN-001", "REQ-001"],
          "resolution_refs": []
        }
      },
      "SRC-001": {
        "type": "SRC",
        "payload": {
          "id": "SRC-001",
          "source_type": "user_input",
          "label": "Initial meeting action hub idea",
          "target": "canonical_contract",
          "provided_by": "human",
          "accessed_at": "2026-05-25T00:00:00+08:00",
          "scope": "Example fixture source for product facts."
        }
      },
      "USER-001": {
        "type": "USER",
        "payload": {
          "id": "USER-001",
          "name": "Meeting organizer",
          "description": "A person responsible for turning meeting outcomes into follow-up actions.",
          "source_refs": ["SRC-001"]
        }
      },
      "SCOPE-001": {
        "type": "SCOPE",
        "payload": {
          "id": "SCOPE-001",
          "statement": "Extract reviewable action items from authorized meeting notes.",
          "phase": "PHASE-001",
          "source_refs": ["SRC-001"]
        }
      },
      "OOS-001": {
        "type": "OOS",
        "payload": {
          "id": "OOS-001",
          "statement": "Automatically committing tasks without human confirmation.",
          "phase": "PHASE-001",
          "reason": "Human confirmation is required before task commitment.",
          "source_refs": ["SRC-001"]
        }
      },
      "PHASE-001": {
        "type": "PHASE",
        "payload": {
          "id": "PHASE-001",
          "name": "Phase 1 MVP",
          "goal": "Validate action extraction and human confirmation.",
          "deliverables": ["OUT-001"],
          "excluded_items": ["OOS-001"],
          "exit_criteria": ["DONE-001"]
        }
      },
      "IN-001": {
        "type": "IN",
        "payload": {
          "id": "IN-001",
          "name": "meeting_transcript",
          "required": true,
          "constraints": ["Must be authorized meeting text or notes."],
          "entry_blockers": ["STOP-001"],
          "permission_requirements": ["Human must have permission to process the meeting text."]
        }
      },
      "EXE-001": {
        "type": "EXE",
        "payload": {
          "id": "EXE-001",
          "rule": "Do not commit extracted items without human confirmation.",
          "required_behavior": "Generate candidates and keep them reviewable.",
          "forbidden_behavior": "Do not create final tasks automatically.",
          "sequence_refs": ["REQ-001", "STOP-001"],
          "human_confirmation": "Required before export or commitment."
        }
      },
      "DCT-001": {
        "type": "DCT",
        "payload": {
          "id": "DCT-001",
          "schema": {
            "action_items": ["title", "owner", "due_date", "source_excerpt"]
          },
          "required_fields": ["title", "source_excerpt"],
          "constraints": ["Missing owner or due date must remain reviewable."],
          "related_reqs": ["REQ-001"]
        }
      },
      "DATA-001": {
        "type": "DATA",
        "payload": {
          "id": "DATA-001",
          "inputs": ["IN-001"],
          "transformations": ["Extract candidate action items."],
          "stores": ["Reviewable action item list."],
          "outputs": ["OUT-001"],
          "related_reqs": ["REQ-001"]
        }
      },
      "VER-001": {
        "type": "VER",
        "payload": {
          "id": "VER-001",
          "case_type": "positive",
          "related_refs": ["REQ-001", "AC-001", "OUT-001"],
          "input": "Authorized meeting text with an explicit owner and action.",
          "expected_result": "A candidate action item with owner, task text, and source excerpt.",
          "blocking": true,
          "failure_handling": "Do not mark Agent PRD execution-ready until the case is satisfied."
        }
      },
      "OUT-001": {
        "type": "OUT",
        "payload": {
          "id": "OUT-001",
          "deliverable": "Reviewable action item list",
          "acceptance_rule": "Must satisfy AC-001 and VER-001.",
          "related_reqs": ["REQ-001"],
          "residual_scope_note": "External task-system sync remains out of scope for this fixture."
        }
      },
      "DONE-001": {
        "type": "DONE",
        "payload": {
          "id": "DONE-001",
          "criterion": "REQ-001 passes AC-001 and VER-001.",
          "verification_refs": ["VER-001"],
          "blocking": true,
          "consistency_condition": "Human PRD, Agent PRD, and canonical contract agree on REQ-001 and AC-001."
        }
      },
      "Q-003": {
        "type": "Q",
        "payload": {
          "id": "Q-003",
          "question": "What is the retention duration for source excerpts?",
          "impact": "Affects privacy handling and auditability beyond the fixture's minimal execution.",
          "phase": "PHASE-001",
          "owner": "human",
          "blocks_human_prd": false,
          "blocks_agent_prd": false,
          "agent_handling": "defer",
          "status": "open",
          "resolution_refs": []
        }
      },
      "RISK-003": {
        "type": "RISK",
        "payload": {
          "id": "RISK-003",
          "risk": "Source excerpts may contain sensitive meeting context.",
          "impact": "Privacy and retention decisions must remain visible.",
          "mitigation": "Keep only necessary source excerpts and defer concrete retention policy to Q-003.",
          "related_refs": ["Q-003", "DATA-001"]
        }
      },
      "RB-001": {
        "type": "RB",
        "payload": {
          "id": "RB-001",
          "target": "human_prd",
          "section": "标准是什么",
          "content_type": "table",
          "contract_refs": ["REQ-001", "AC-001"],
          "source_refs": ["SRC-001"],
          "allowed_inference": "summary",
          "unsupported_claims": [],
          "status": "ready"
        }
      },
      "RB-101": {
        "type": "RB",
        "payload": {
          "id": "RB-101",
          "target": "agent_prd",
          "section": "Verification Contract",
          "content_type": "table",
          "contract_refs": ["REQ-001", "AC-001", "VER-001"],
          "source_refs": ["SRC-001"],
          "allowed_inference": "summary",
          "unsupported_claims": [],
          "status": "ready"
        }
      },
      "GATE-001": {
        "type": "GATE",
        "payload": {
          "id": "GATE-001",
          "name": "source integrity",
          "blocking_condition": "Rendered facts lack canonical object or source support.",
          "status": "pass",
          "blocking": false,
          "affected_targets": ["human_prd", "agent_prd"],
          "evidence_refs": ["SRC-001", "RB-001", "RB-101"]
        }
      }
    },
    "object_index": {
      "CORE": ["CORE-001"],
      "SRC": ["SRC-001"],
      "USER": ["USER-001"],
      "SCOPE": ["SCOPE-001"],
      "OOS": ["OOS-001"],
      "PHASE": ["PHASE-001"],
      "REQ": ["REQ-001"],
      "AC": ["AC-001"],
      "IN": ["IN-001"],
      "EXE": ["EXE-001"],
      "DCT": ["DCT-001"],
      "DATA": ["DATA-001"],
      "VER": ["VER-001"],
      "OUT": ["OUT-001"],
      "STOP": ["STOP-001"],
      "DONE": ["DONE-001"],
      "Q": ["Q-003"],
      "RISK": ["RISK-003"],
      "RB": ["RB-001", "RB-101"],
      "GATE": ["GATE-001"]
    }
  },
  "human_prd": {
    "format": "markdown",
    "content": "[fixture body omitted]",
    "render_block_refs": ["RB-001"],
    "status": "review_ready"
  },
  "agent_prd": {
    "format": "markdown",
    "content": "[fixture body omitted]",
    "render_block_refs": ["RB-101"],
    "status": "execution_ready"
  },
  "contract_summary": {
    "product": "Meeting Action Hub",
    "requirements": ["REQ-001"],
    "scope": ["SCOPE-001"],
    "out_of_scope": ["OOS-001"],
    "phases": ["PHASE-001"],
    "open_questions": ["Q-003"],
    "assumptions": []
  },
  "traceability_summary": {
    "render_traceability": [
      {
        "render_block_id": "RB-001",
        "target": "human_prd",
        "section": "标准是什么",
        "contract_refs": ["REQ-001", "AC-001"],
        "source_refs": ["SRC-001"],
        "status": "ready"
      },
      {
        "render_block_id": "RB-101",
        "target": "agent_prd",
        "section": "Verification Contract",
        "contract_refs": ["REQ-001", "AC-001", "VER-001"],
        "source_refs": ["SRC-001"],
        "status": "ready"
      }
    ],
    "requirement_traceability": [
      {
        "requirement_id": "REQ-001",
        "source_refs": ["SRC-001"],
        "assumption_refs": [],
        "acceptance_criteria": ["AC-001"],
        "verification_refs": ["VER-001"],
        "output_refs": ["OUT-001"],
        "done_refs": ["DONE-001"]
      }
    ],
    "decision_traceability": [
      {
        "decision_ref": "Q-003",
        "decision_type": "open_question",
        "affected_refs": ["DATA-001", "RISK-003"],
        "status": "open",
        "owner": "human",
        "resolution_refs": []
      }
    ]
  },
  "gate_report": [
    {
      "gate_id": "GATE-001",
      "name": "source integrity",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["SRC-001", "RB-001", "RB-101"],
      "message": "All rendered facts are backed by canonical objects or sources.",
      "required_fix": ""
    }
  ],
  "next_actions": []
}
```
