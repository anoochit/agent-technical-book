# Agent Technical Book Orchestrator

A multi-agent system designed to collaboratively research, outline, write, and validate a technical book. This project leverages the [Google Agent Developer Kit (ADK)](https://github.com/google/adk-python) to coordinate a team of specialized AI agents.

## Project Overview

Writing a technical book is a complex process involving various stages from initial brainstorming to final review. This system automates and assists in this lifecycle through an orchestrated collection of agents, each with a specific domain of expertise.

## Agent Team

The system is managed by a **Root Orchestrator** which delegates tasks to the following specialized agents:

- **Strategist**: Defines the high-level goals and target audience.
- **Outline Agent**: Structures the table of contents and chapter breakdowns.
- **Research Agent**: Performs web searches and gathers technical information.
- **Author Agent**: Drafts the content for chapters and sections.
- **Example Agent**: Generates practical code examples and snippets.
- **Technical Validator**: Ensures the accuracy of technical claims and code.
- **Reviewer Agent**: Provides feedback on writing style and clarity.
- **Consistency Agent**: Maintains a unified voice and terminology across the book.
- **Marketing Agent**: Develops promotion strategies and social media content.
- **Analytics Agent**: Evaluates the writing process and content metrics.

## Directory Structure

```text
├───orchestrator/       # Agent configurations and custom tools
│   ├───tools/          # Python tools for search and file I/O
│   └───*.yaml          # ADK agent configuration files
├───workspace/          # Output directory for the book content
│   ├───chapter*.md     # Individual chapter drafts
│   ├───marketing/      # Generated marketing materials
│   └───research/       # Research notes and source data
├───main.py             # Entry point for the agent system
└───pyproject.toml      # Project dependencies and metadata
```

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended for package management)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd agent-technical-book
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Set up your API keys (e.g., for Gemini):
   ```bash
   export GOOGLE_API_KEY='your-api-key'
   ```

### Usage

#### Run the Web UI

Start the interactive agent dashboard:

```bash
adk web
```

#### Run the API Server

Start a RESTful interface for external integration:

```bash
adk api_server
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
