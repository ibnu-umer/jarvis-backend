### WSL SIDE (Backend — the brain)

**Create:**
- FastAPI/Flask backend service
- Action dispatcher + registry
- Scheduling engine
- AI processing / NLP / commands interpretation
- Data storage logic (SQLite/Postgres)
- API endpoints for system actions (ex: /system/shutdown, /system/sleep)
- Runs as: Python server inside WSL

**Never do here:**
- GUI, notifications, message boxes
- Direct WinAPI calls
- Power management commands

---

### WINDOWS SIDE (Controller — the hands & face)

**Create:**
- Windows tray application (python + pystray or C# if you’re not scared)
- Custom confirmation dialog UI
- PowerShell command executor
- System action handler (shutdown, sleep, brightness, volume, etc.)
- Listener that receives REST commands from WSL and executes them
- Runs as: Auto-start Windows app

**Never do here:**
- Heavy computation
- AI logic
- Schedulers or backend processing