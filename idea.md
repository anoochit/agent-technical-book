# 🧠 Multi-Agent Technical Book Publishing System

This system is a production-grade implementation for automating the lifecycle of a technical book—from initial strategy and research to writing, technical validation, and marketing—using the **Google Agent Developer Kit (ADK)**.

---

## 🏗 High-Level Architecture

The system follows a layered cognitive approach, separating high-level planning from specialized content creation and rigorous quality control, coordinated by a central state management system.

```text
       User Request (e.g., "Write a book about AI Agents")
                ↓
      [ Orchestrator Agent (Root) ] ↔ [ book_state.json ]
                ↓
    ┌───────────┴───────────┬──────────────────┐
 [ Planning ]          [ Creation ]        [ Quality ]
 ├── Strategist         ├── Author          ├── Technical Validator
 ├── Research           ├── Example Gen.    ├── Reviewer (Editor)
 └── Outline            └── Marketing       └── Consistency
                               ↓
                      [ Analytics & Optimization ]
```

---

## 🤖 Agent Role Breakdown

### 1. Orchestrator (`root_agent.yaml`)
The "brain" of the system. It decomposes user requests, maintains shared state, and delegates tasks to specialists.
*   **Model:** `gemini-2.5-flash`
*   **Protocol:** Manages `book_state.json` to track project progress.
*   **Tools:** `ddg_search`, `fetch_web_content`, `create_project_dir`, `execute_command`.

### 2. Strategist Agent (`strategist_agent.yaml`)
Defines target audience, technical depth, and USPs.
*   **Output:** Saves strategic foundation as `strategy.md`.

### 3. Research Agent (`research_agent.yaml`)
Grounds the book in official documentation and credible technical sources.
*   **Output:** Saves grounded reports in the `research/` directory.
*   **Tools:** `ddg_search`, `fetch_web_content`.

### 4. Outline Agent (`outline_agent.yaml`)
Designs the chapter flow and learning progression.
*   **Output:** Generates the master `toc.md` (Table of Contents).

### 5. Author Agent (`author_agent.yaml`)
Converts outlines into detailed technical content.
*   **Output:** Saves chapters in `chapters/` (e.g., `00_preface.md`, `01_introduction.md`).

### 6. Example Generator Agent (`example_agent.yaml`)
Creates high-quality, tested code snippets in Python or TypeScript.
*   **Output:** Saves snippets in the `examples/` directory.

### 7. Technical Validator Agent (`technical_validator_agent.yaml`)
Verifies code correctness, technical accuracy, and security.
*   **Output:** Maintains a detailed `validation_log.md`.

### 8. Reviewer Agent (`reviewer_agent.yaml`)
Enforces the **Google Developer Documentation Style Guide**.
*   **Output:** Saves refined versions in the `reviewed/` directory.

### 9. Consistency Agent (`consistency_agent.yaml`)
Ensures uniform voice and terminology across the manuscript.
*   **Output:** Manages the project-wide `glossary.md`.

### 10. Marketing Agent (`marketing_agent.yaml`)
Designs launch plans and promotional assets (LinkedIn/Twitter threads, blog posts).
*   **Output:** Saves all content in the `marketing/` directory.

### 11. Analytics Agent (`analytics_agent.yaml`)
Predicts performance and optimizes the publishing funnel.
*   **Model:** `gemini-3.1-pro-preview`
*   **Output:** Generates `analytics_report.md`.

---

## 🛠 Tools & Infrastructure

The agents interact with a sandboxed environment via specialized Python tools:

*   **`file_tools.py`**: Manages the `workspace/` sandbox.
    *   `read_file` / `write_file`: Standard I/O.
    *   `create_project_dir`: Folder management.
    *   `execute_command`: Shell execution within the workspace.
*   **`ddg_tools.py`**: Real-time web grounding.
    *   `ddg_search`: Broad technical queries.
    *   `fetch_web_content`: Content extraction using BeautifulSoup.

---

## 🔄 Execution Workflow

1.  **Phase 1: Strategy & Research**: Orchestrator triggers Strategist (`strategy.md`) and Research agents to define the niche.
2.  **Phase 2: Structure**: Outline agent generates the `toc.md` based on research.
3.  **Phase 3: Content Cycle**: 
    *   **Author** drafts text to `chapters/`.
    *   **Example Gen** adds code to `examples/`.
    *   **Validator** logs checks in `validation_log.md`.
    *   **Reviewer** edits for style into `reviewed/`.
4.  **Phase 4: Coherence**: Consistency agent harmonizes terminology via `glossary.md`.
5.  **Phase 5: Go-to-Market**: Marketing and Analytics agents prepare launch assets and ROI predictions.

---

## 🚀 Production Status

This system is fully operational as a set of **ADK Agent Configurations**. It leverages `gemini-2.5-flash` for high-volume tasks and `gemini-3.1-pro-preview` for complex analytical reasoning. All state is persisted in `book_state.json` to enable interrupted/resumable workflows.
