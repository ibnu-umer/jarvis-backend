# Hybrid Architecture Plan for Jarvis System

## Overview
The system will be split into two main components:
- **WSL (Linux environment):** Brain / Backend Logic / AI Processing
- **Windows (Native environment):** System Controller / UI / Hardware & OS Operations

This design allows the assistant to utilize WSL's performance advantages while retaining full control of system-level Windows actions.


## Why Choose Hybrid Architecture?
- **Best of Both Worlds:** WSL handles AI and backend processing efficiently, while Windows handles native system actions and UI.
- **Avoid Limitations:** Running everything in WSL makes GUI dialogs, notifications, and system controls difficult; running only in Windows reduces performance and flexibility.
- **Scalable & Maintainable:** Clearly separates processing logic from system interaction, making the architecture easier to extend, test, and debug.
- **Future Proof:** Allows easy expansion for remote control, plugins, and cross-device communication without major rework.


## Responsibilities
### WSL (Backend / Core Processing)
- Runs the main backend service
- Handles AI features, NLP, scheduling logic, data processing, and monitoring
- Exposes a **REST / WebSocket / gRPC API** on localhost for Windows to interact with
- Can run background tasks efficiently without Windows performance limitations

### Windows (Frontend + System Control)
- A lightweight Windows application that communicates with the backend
- Executes system operations:
  - Shutdown, Restart, Sleep, Lock, Logout
  - Volume and Brightness control
  - Notifications and message boxes
  - Task Scheduler & process automation
- Provides UI dialogs (custom confirmation box)


## Communication Layer
Use localhost communication:

```
WSL backend <----> Windows controller
```

Options:
- Local REST API (FastAPI / Flask)
- WebSockets for real-time streaming
- gRPC for structured binary communication

Recommended: **REST API first**, add WebSockets later if needed.


## Launch Strategy
- Windows tray app auto-starts with system
- Tray app connects to backend
- If backend isn't running, it starts via WSL command
- Commands from backend trigger UI or system actions

Example call:
```
POST http://localhost:5000/system/shutdown
```
Windows app receives & executes:
```
powershell.exe -command "shutdown /s /t 0"
```


## Advantages of Hybrid Approach
| Feature | WSL | Windows |
|--------|------|----------|
| AI & Heavy Compute | ✔ Faster | ✖ Slower |
| System access | ✖ Painful | ✔ Native |
| GUI & Alerts | ✖ Limited | ✔ Full control |
| Clean architecture | ✔ Scalable | ✖ Monolithic |


## Future Expandability
This architecture easily allows:
- Mobile remote control 
- Web dashboard
- Smart automation rules engine
- Plugins / skills system
- Cross-device communication


## Short Summary
WSL runs the **brain**, Windows runs the **hands & face**. Combining both creates a performant and scalable architecture without hacks, path issues, or permission chaos.


