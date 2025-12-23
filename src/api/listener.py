from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import threading

from configs.config import WSL_HOST, WSL_PORT
from src.core.logger import logger
from src.run_pipeline import run_pipeline




class CommandRequest(BaseModel):
    user_input: str


class CommandResponse(BaseModel):
    plan: dict
    result: dict
    status: str


class WSLBackend:
    def __init__(self, planner, executor, host=WSL_HOST, port=WSL_PORT):
        self.host = host
        self.port = port
        self.planner, self.executor = planner, executor

        self.app = FastAPI(title="WSLBackend")
        self.state = {
            "status": "healthy",
            "last_checked": None
        }

        self._setup_routes()
        self.server_thread = None

    def _setup_routes(self):
        @self.app.get("/health")
        def health():
            self.state["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return self.state

        @self.app.post("/command", response_model=CommandResponse)
        async def handle_command(req: CommandRequest):
            print(req)
            try:
                plan, result = await run_pipeline(
                    req.user_input,
                    self.planner,
                    self.executor
                )
                return {
                    "plan": plan,
                    "result": result,
                    "status": "ok"
                }
            except Exception as e:
                logger.exception("Command execution failed")
                return {
                    "plan": {},
                    "result": {"error": str(e)},
                    "status": "error"
                }

    def _run(self):
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="error"
        )

    def start(self):
        if not self.server_thread:
            self.server_thread = threading.Thread(
                target=self._run,
                daemon=True
            )
            self.server_thread.start()
            logger.info(f"WSL backend running at http://{self.host}:{self.port}")

    def stop(self):
        logger.info("FastAPI shutdown not implemented (use SIGTERM)")
