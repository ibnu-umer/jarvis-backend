# Planner for Agentic Jarvis

The **Advanced Planner** is the central decision-making module of the agentic Jarvis system. Its role is to **translate user intents into complex, actionable sequences**, dynamically orchestrating actions, resolving parameters, and ensuring dependencies and preconditions are met.

Unlike a basic if-else system, this planner operates autonomously, reasoning about context, capabilities, and execution results to achieve user goals efficiently and intelligently.


## Core Capabilities

1. **Dynamic Action Selection**
   - Determines which actions from the capability registry are necessary based on the parsed intent.
   - Can select multiple actions for multi-step goals.

2. **Intelligent Parameter Resolution**
   - Automatically fills required and optional parameters using context, defaults, or LLM reasoning.

3. **Conditional Execution & Branching**
   - Evaluates preconditions such as folder existence, permissions, or resource availability.
   - Supports branching logic if preconditions fail or prior actions do not succeed.

4. **Execution Feedback Integration**
   - Monitors the outcome of each action.
   - Dynamically adjusts subsequent steps based on success, failure, or partial completion.

5. **Sequencing and Dependency Management**
   - Orders actions logically, ensuring prerequisite tasks are completed before dependent actions.

6. **Autonomous Planning and Recovery**
   - Generates fallback strategies when actions fail.
   - Can suggest alternative steps or escalate to user intervention.

7. **Extensibility and Scalability**
   - Easily integrates new actions and capabilities without changing core logic.
   - Compatible with LLM-based reasoning for enhanced decision-making and parameter inference.


## Responsibilities

- **Interpret Parsed Intent**: Receives structured intents from the Intent Parser and identifies required outcomes.
- **Map Capabilities**: Matches intent to available functions in the capability registry.
- **Generate Action Plan**: Creates a dynamic, ordered sequence of actions with appropriate parameters.
- **Validate Preconditions**: Checks environment, resources, and context to ensure actions can safely execute.
- **Monitor Execution**: Receives results from the Executor and updates the plan dynamically.
- **Adaptive Planning**: Alters action sequences or parameters in response to failures or unexpected conditions.
- **Fallback & Notification**: Provides alternative actions or notifications for user intervention when necessary.
- **Support Complex Workflows**: Can handle multi-step and chained tasks autonomously.


## Example Workflow

1. **User Input**: "Organize my Downloads folder and archive all PDFs."
2. **Intent Parser**: Converts input into structured intent:
```json
{ "intent": "organize_folder", "params": { "folder": "Downloads", "file_types": ["pdf"], "archive": true } }
```
3. **Advanced Planner**: Dynamically generates plan:
   - Move PDFs from Downloads to Archive
   - Archive PDFs in Archive folder
   - Clean up temporary files
4. **Executor**: Runs each step and returns results.
5. **Planner Feedback Loop**:
   - Adjusts subsequent actions if any step fails.
   - Suggests alternative steps or notifies the user.


## Implementation Notes

- The planner is **intelligence-driven**, capable of integrating LLM reasoning for advanced decision-making.
- It is **modular**, separating planning from execution, making it safe to extend and maintain.
- It can handle **dynamic multi-step workflows**, precondition checking, execution feedback, and intelligent fallback strategies.
