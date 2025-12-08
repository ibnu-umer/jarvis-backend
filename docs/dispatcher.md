# Command Dispatcher

The **Command Dispatcher** is the backend component responsible for receiving a standardized command request (e.g., module + action + params) and routing it to the correct module handler.

It acts as the central router for all operations, connecting user intentions to actual execution logic.

## What should it do?
- Receive a structured command object
- Validate required parameters
- Look up the correct module from the module registry
- Execute the requested action
- Return a standardized response object

## Why is it needed?
Currently, the listener only accepts input and prints it. Without a dispatcher, the backend cannot determine what to do with a command or how to invoke an action. The dispatcher becomes the spine that every request flows through.

## Use Cases
| Command Example | Dispatcher Action |
|-----------------|------------------|
| `app.open chrome` | module: app → action: open(params) |
| `file.read C:/abc.txt` | module: file → action: read(path) |
| `system.shutdown` | module: system → action: shutdown() |

## Example Workflow
```
User Input → Intent Parser → Command Object → Dispatcher → Module → Windows Agent → Response
```
