# AI Task Agent

A lightweight AI-powered task management agent built in Python using Google's Gemini API and function calling.

The project explores how an LLM can act as an agent rather than just a chatbot: interpreting natural-language requests, selecting tools, executing actions, using tool results, and continuing through multiple steps until the user's request is resolved.

## Current Features

- Add tasks using natural language
- Retrieve the current task list
- Mark tasks as completed
- Delete tasks
- Multi-step tool execution
- Conversation memory during the active session
- Persistent task storage using JSON
- Natural-language task identification
- Handling of ambiguous task references
- System instructions and behavioral guardrails
- Structured handling of API errors

## Example

Instead of requiring commands or task IDs, the user can interact naturally:

```text
User: Complete "buy milk"

Agent:
1. Retrieves the current task list
2. Identifies the matching task
3. Resolves its internal ID
4. Executes the completion tool
5. Confirms the result
```

Task IDs remain an internal implementation detail and are not exposed to the user.

If multiple tasks could match a request, the agent is instructed to ask for clarification instead of making an arbitrary choice.

## Architecture

The project separates agent reasoning from deterministic application logic:

```text
User
  │
  ▼
main.py
  │
  ▼
agent.py
  │
  ├── System instructions
  ├── Conversation state
  ├── Gemini API
  └── Agent/tool loop
          │
          ▼
   Tool declarations
          │
          ▼
      Python tools
          │
          ▼
      tasks.json
```

### `agent.py`

Handles communication with Gemini, conversation state, tool calls, tool results, and the multi-step agent loop.

### `tools.py`

Contains the deterministic Python functions that read or modify task data.

### `tools_schemas.py`

Defines the tools and their parameter schemas so the model knows which actions are available and how to call them.

### `instructions.py`

Defines the agent's purpose, behavior, tool-use rules, ambiguity handling, and conversational guardrails.

### `main.py`

Provides the current command-line chat interface.

## Agent Loop

The agent supports multi-step interactions.

For example:

```text
User: Delete "buy coffee"
        │
        ▼
Gemini decides it needs the task list
        │
        ▼
get_tasks()
        │
        ▼
Tool result returned to Gemini
        │
        ▼
Gemini identifies the matching internal task ID
        │
        ▼
delete_task(task_id)
        │
        ▼
Tool result returned to Gemini
        │
        ▼
Final natural-language response
```

This allows the model to dynamically choose and chain tools instead of relying on a fixed sequence of hard-coded actions.

## Conversation State

Conversation history is currently stored in memory for the duration of the running session.

This allows follow-up interactions such as:

```text
User: Complete the milk task.

Agent: I found multiple matching tasks:
- Buy milk
- Buy milk for the office

Which one do you mean?

User: The office one.
```

Persistent conversation storage is planned for a future version.

## Project Status

This project is under active development.

The current version focuses on the core agent architecture and tool-calling workflow. Planned improvements include:

- Database-backed task persistence
- Task editing and richer task metadata
- Improved deterministic ambiguity handling
- Persistent conversations
- Automated tests and evaluations
- Web frontend
- Calendar view
- Dates, deadlines, and reminders
- Calendar and reminder integrations
- Authentication and multi-user support
- Deployment as a full-stack application

## Security

API credentials are stored locally in a `.env` file and are excluded from version control.

Never commit API keys or other secrets to the repository.

## Tech Stack

- Python
- Gemini API
- Function calling / tool use
- JSON-based persistence (current development version)

## Why I Built This

The goal of this project is to explore the architecture behind AI agents: how language models can interpret user intent, interact with deterministic tools, maintain conversational context, handle ambiguity, and perform multi-step actions against application state.

The project is being developed incrementally, with the intention of evolving the initial command-line prototype into a more complete task and calendar management application.