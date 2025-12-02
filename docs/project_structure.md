# Project Structure (Hybrid Architecture)

## Overview
This structure separates backend processing (WSL) and system execution/UI (Windows) for clean, scalable development.


## WSL Side (Backend / AI / Logic)
```
jarvis-backend/
│
├── src/
│   ├── api/                   # REST endpoints (FastAPI / Flask)
│   │   ├── system_routes.py   # /system/* endpoints
│   │   └── ai_routes.py       # /ai/* endpoints
│   │
│   ├── core/
│   │   ├── dispatcher.py      # Dispatch actions to Windows
│   │   ├── registry.py        # Modules and actions registry
│   │   └── basemodule.py      # Base class for modules
│   │
│   ├── modules/               # Action modules
│   │   ├── screentime.py
│   │   ├── system_metrics.py
│   │   └── ...
│   │
│   ├── ai/                    # NLP / ML / model loading
│   │   ├── engine.py
│   │   └── intent_parser.py
│   │
│   ├── scheduler/
│   │   └── scheduler.py       # Background jobs
│   │
│   ├── storage/
│   │   └── database.py        # SQLite / Postgres
│   │
│   └── main.py                # Backend entrypoint
│
├── tests/
│
└── requirements.txt
```


## Windows Side (Controller / UI / System Actions)
```
jarvis-controller/
│
├── src/
│   ├── tray/
│   │   └── app.py             # System tray / startup app
│   │
│   ├── ui/
│   │   ├── confirm.py         # Custom confirmation dialog
│   │   └── notify.py          # Toast notifications
│   │
│   ├── system/
│   │   ├── actions.py         # PowerShell + OS control wrapper
│   │   └── brightness.py
│   │
│   ├── network/
│   │   └── listener.py        # API listener for backend calls
│   │
│   └── bootstrap.py           # Autostart / reconnect to WSL
│
├── assets/                    # Icons, dialog graphics
│
├── scripts/
│   └── install_startup.ps1
│
└── requirements.txt
```


## Communication flow
```
[WSL Backend] --- HTTP/WebSocket ---> [Windows Controller] --- executes --- OS
```


## Key Principles
- WSL never executes hardware/system commands directly
- Windows never includes backend logic or AI
- Must communicate through a clean API boundary
- Both parts remain independently replaceable


## Simple Flow Example
**Example Command: "Shutdown the system"**
```ascii
╔══════════════════╗      ╔══════════════════════╗      ╔════════════════════════════╗      ╔═══════════════╗
║      User        ║ ───> ║ Jarvis Backend (WSL) ║ ───> ║ Intent: "shutdown" parsed  ║ ───> ║ REST Request  ║
╚══════════════════╝      ╚══════════════════════╝      ╚════════════════════════════╝      ╚═══════════════╝
                                                                                                    │
                                                                                                    ▼
                                                                                            POST /system/shutdown
                                                                                                    │
                                                                                                    ▼
╔═══════════════════════╗     ╔════════════════════════╗     ╔══════════════════════╗     ╔════════════════════╗
║   User Clicks "YES"   ║ ─── ║  Show Confirm Dialog   ║ ─── ║   Receive request    ║ ─── ║ Windows Controller ║
╚═══════════════════════╝     ╚════════════════════════╝     ╚══════════════════════╝     ╚════════════════════╝
                                                                                                    │
                                                                                                    ▼
                                                                                Execute: powershell.exe shutdown /s /t 0
                                                                                                    │
                                                                                                    ▼
                                                                                        💀 System Shuts Down 💀
```

### Flow Breakdown
- User speaks or types command
- WSL Backend interprets intent using NLP model
- Backend calls the Windows controller through a REST request
- Windows controller shows a custom confirmation dialog
- On approval → executes actual OS command
- Backend logs completion and updates system status