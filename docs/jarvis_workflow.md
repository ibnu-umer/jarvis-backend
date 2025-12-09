# Complete Workflow of Agentic Jarvis

## Overview

Agentic Jarvis is designed as a modular, intelligent assistant capable of understanding user intents, planning actions dynamically, executing them safely, and adapting based on feedback. This document describes the **complete workflow** from user input to action execution and feedback.

---

## Core Components

### 1. Intent Parser
- **Purpose:** Understand user intent and extract structured parameters.
- **Responsibilities:**
  - Interpret high-level goals from user input.
  - Extract required and optional parameters.
  - Suggest possible actions based on intent.
- **Tools:** LLM-based NLP for understanding intent.
- **Example Output:**
```json
{
  "intent": "organize_folder",
  "params": {"folder": "Downloads", "file_types": ["pdf"], "archive": true}
}
```

### 2. Planner (Advanced Planner)
- **Purpose:** Decide how to achieve the user intent reliably and efficiently.
- **Responsibilities:**
  - Map intent to available actions from the Capability Registry.
  - Determine action sequence based on dependencies.
  - Fill in missing parameters intelligently.
  - Check preconditions (e.g., folder existence, permissions).
  - Adapt plan based on previous execution results.
  - Handle optional, conditional, and fallback actions.
- **Example Decisions:**
  - Move PDFs from Downloads → Archive
  - Archive PDFs in Archive folder
  - Delete temporary files in Downloads
  - Notify user if any step fails

### 3. Executor
- **Purpose:** Execute actions as instructed by the Planner.
- **Responsibilities:**
  - Call functions with the provided parameters.
  - Capture execution results (success/failure, logs).
  - Return structured results to Planner for feedback.
- **Example Execution Result:**
```json
{
  "action": "move_files",
  "result": {"success": true, "details": "Moved 10 files"}
}
```

### 4. Feedback Loop
- **Purpose:** Ensure plan adapts to real-world results.
- **Responsibilities:**
  - Receive results from Executor.
  - Adjust remaining steps or parameters based on success/failure.
  - Trigger fallback actions if required.
  - Optionally notify user or request intervention.

---

## Complete Workflow Diagram

```
User Input (e.g., "Organize my Downloads folder and archive all PDFs")
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Intent Parser          │
                  │ - Understand goal      │
                  │ - Extract intent       │
                  │ - Suggest actions      │
                  │ - Fill params          │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │  Planner               │
                  │  - Map actions         │
                  │  - Sequence steps      │
                  │  - Check preconditions │
                  │  - Adjust plan based   │
                  │    on feedback         │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │  Executor              │
                  │  - Execute actions     │
                  │  - Return results      │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │  Feedback Loop         │
                  │  - Adapt plan          │
                  │  - Suggest fallback    │
                  │  - Notify user         │
                  └────────────────────────┘
```


## Example End-to-End Execution

**User Input:** "Organize my Downloads folder and archive all PDFs"

1. **Intent Parser:**
```json
{
  "intent": "organize_folder",
  "params": {"folder": "Downloads", "file_types": ["pdf"], "archive": true}
}
```

2. **Planner Output (Dynamic Plan):**
- Move PDFs from Downloads → Archive
- Archive PDFs in Archive folder
- Delete temporary files in Downloads
- Notify user if move fails

3. **Executor Actions:**
- `move_files(source='Downloads', destination='Archive', file_types=['pdf'])`
- `archive_files(folder='Archive', file_types=['pdf'])`
- `delete_files(folder='Downloads', file_types=['tmp', 'log'])`

4. **Feedback Loop:**
- Detect move failure → notify user and suggest alternative folder
- Adjust subsequent steps if needed


## Key Takeaways

- **Intent Parser**: Determines *what* the user wants.
- **Planner**: Determines *how* to achieve it safely, efficiently, and adaptively.
- **Executor**: Performs the actions.
- **Feedback Loop**: Ensures the system adapts dynamically to real-world results.
- This architecture enables **scalable, intelligent, and agentic behavior** in Jarvis.

