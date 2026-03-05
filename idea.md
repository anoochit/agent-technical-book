# 🧠 Multi-Agent Technical Book Publishing System

This system is a production-grade implementation for automating the lifecycle of a technical book—from initial strategy and research to writing, technical validation, and marketing—using the **Google Agent Developer Kit (ADK)**.

---

## 🏗 High-Level Architecture

The system follows a layered cognitive approach, separating high-level planning from specialized content creation and rigorous quality control.

```text
       User Request (e.g., "Write a book about AI Agents")
                ↓
      [ Orchestrator Agent (Root) ]
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
*   **Tools:** DuckDuckGo Search, Web Fetching, File System, Command Execution.

### 2. Strategist Agent (`strategist_agent.yaml`)
Defines the target audience, technical depth, and core value proposition. It ensures the book has a unique and opinionated positioning.

### 3. Research Agent (`research_agent.yaml`)
A technical research specialist that grounds the book in reality.
*   **Protocol:** Uses `ddg_search` and `fetch_web_content` to find official docs and saves grounded reports in the `research/` directory.

### 4. Outline Agent (`outline_agent.yaml`)
Designs the cohesive structure, chapter sequencing, and learning progression.
*   **Output:** Generates the `toc.md` (Table of Contents).

### 5. Author Agent (`author_agent.yaml`)
Converts outlines into detailed technical content.
*   **Constraint:** strictly follows the outline, focusing on clarity and examples while avoiding "fluff."
*   **Output:** Saves chapters as `chapter_1.md`, `chapter_2.md`, etc.

### 6. Example Generator Agent (`example_agent.yaml`)
Specialized in generating production-grade code snippets in Python/TypeScript, including unit tests and inline documentation.

### 7. Technical Validator Agent (`technical_validator_agent.yaml`)
The "sanity check" for code. It verifies correctness, identifies deprecated patterns, and assesses security risks.

### 8. Reviewer Agent (`reviewer_agent.yaml`)
Acts as a Senior Publishing Editor. It enforces the Google Developer Documentation Style Guide, ensures logical flow, and saves refined versions in the `reviewed/` directory.

### 9. Consistency Agent (`consistency_agent.yaml`)
Scans the entire manuscript to ensure uniform terminology, tone, and formatting across all chapters.

### 10. Marketing Agent (`marketing_agent.yaml`)
Generates a multi-channel campaign, including 5-day launch strategies, social media assets, and high-conversion landing page copy in the `marketing/` directory.

### 11. Analytics Agent (`analytics_agent.yaml`)
Predicts performance, maps conversion funnels, and provides data-backed recommendations to optimize the publishing strategy.

---

## 🛠 Tools & Infrastructure

The agents interact with the environment via specialized Python tools:

*   **`file_tools.py`**: A sandboxed file system utility managing the `workspace/` directory. It supports file reading, writing, directory creation, and shell command execution.
*   **`ddg_tools.py`**: Enables real-time web grounding via DuckDuckGo and BeautifulSoup for content extraction.

---

## 🔄 Execution Workflow

1.  **Phase 1: Strategy & Research**: The Orchestrator triggers the Strategist and Research agents to define the book's niche and gather facts.
2.  **Phase 2: Structure**: The Outline agent generates the TOC based on the research.
3.  **Phase 3: Content Cycle**: For each chapter:
    *   **Author** drafts text.
    *   **Example Gen** adds code.
    *   **Validator** checks code.
    *   **Reviewer** edits for style.
4.  **Phase 4: Coherence**: The Consistency agent runs across the full set of files.
5.  **Phase 5: Go-to-Market**: Marketing and Analytics agents prepare the launch assets and performance predictions.

---

## 🚀 Production Status

This system is currently implemented as a set of **ADK Agent Configurations**. All agents are configured with specific instructions, sub-agent dependencies, and tool access to ensure cognitive specialization and reduced hallucination.
