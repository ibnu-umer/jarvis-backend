# Execution Engine Explained — Concrete Example

## Goal
**User:**  
“Prepare my work environment”

This is a single goal that expands into multiple coordinated actions.


## Step 1 — Planner Thinks

The planner decides *what should happen*, not how to execute it.

It considers:
- Historical memory (VS Code usually used)
- Current state (workspace not ready)
- Past success rate (high confidence)

The planner outputs a **task graph**, serialized as DSL:

```yaml
task_graph:
  name: prepare_work_environment
  entry: check_workspace

tasks:
  check_workspace:
    type: decision
    condition: workspace_ready
    on_true: done
    on_false: open_folder

  open_folder:
    type: action
    controller: open_folder
    args:
      path: "~/projects/jarvis"
    on_success: launch_vscode
    on_failure: abort

  launch_vscode:
    type: action
    controller: launch_app
    args:
      app: vscode
    retries: 1
    on_success: done

  done:
    type: action
    controller: notify
    args:
      message: "Workspace ready"
```


The planner stops here.
No execution happens at this stage.

## Step 2 — Execution Engine Obeys

The execution engine receives the graph and executes it exactly as declared.
### Execution Flow
1. check_workspace 
* Condition evaluated → false
* Follows on_false → open_folder

2. open_folder
* Preconditions validated
* Controller action executed
* Postconditions verified
* Transition → launch_vscode

3. launch_vscode
* First attempt fails
* Retry triggered (declared in graph)
* Second attempt succeeds
* Transition → done

4. done
* Notification sent
* Graph execution completes

The engine:
* Did not invent retries
* Did not skip steps
* Did not optimize or infer intent

It executed the plan faithfully.

## Step 3 — Controller Acts

The controller receives atomic commands like:
```json
{ "action": "open_folder", "path": "~/projects/jarvis" }
```

or

```json
{ "action": "launch_app", "app": "vscode" }
```

The controller:
* Executes the action
* Returns success or failure
* Does not reason or plan

## Post-Execution — Learning

Execution results are stored:
```json
{
  "graph": "prepare_work_environment",
  "success": true,
  "retries": { "launch_vscode": 1 },
  "duration": 9.8
}
```

Future planning is biased using this data:
* Successful graphs are preferred
* Retry behavior can be adjusted
* Confidence increases

Learning happens outside execution.

## Key Principle
Planner thinks. <br>
Execution engine obeys.<br>
Controller acts.<br>

Violating this separation collapses the system into unpredictability.

