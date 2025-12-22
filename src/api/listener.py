from flask import Flask, jsonify, request
from datetime import datetime
import threading, logging
from src.core.logger import logger
from configs.config import WSL_HOST, WSL_PORT




class WSLBackend:
    def __init__(self, host=WSL_HOST, port=WSL_PORT):
        self.host = host
        self.port = port
        self.app = Flask("WSLBackend")
        self.state = {
            "status": "healthy",
            "last_checked": None
        }
        self.server_thread = None
        self._setup_routes()


    def _setup_routes(self):
        @self.app.route("/health", methods=["GET"])
        def health():
            self.state["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify({
                "status": self.state["status"],
                "last_checked": self.state["last_checked"]

            }), 200
        
        
        @self.app.route("/command", methods=["POST"])
        def handle_command():
            data = request.get_json(force=True, silent=True)

            if not data or "text" not in data:
                return {"error": "missing command text"}, 400

            command_text = data["text"]
            print(command_text)

            return {
                "status": "accepted",
            }, 200


        @self.app.route("/intent", methods=["POST"])
        def handle_intent():
            data = request.json or {}
            intent = data.get("intent")
            payload = data.get("payload", {})
            logger.info(f"[WSLBackend] Intent received: {intent}, payload: {payload}")
            # TODO: Implement real intent handling logic
            return jsonify({"status": "received", "intent": intent})
        

    def _run(self):
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        self.app.run(host=self.host, port=self.port, threaded=True)


    def start(self):
        if not self.server_thread:
            self.server_thread = threading.Thread(target=self._run, daemon=True)
            self.server_thread.start()
            logger.info(f"WSL backend running at http://{self.host}:{self.port}")


    def stop(self):
        logger.info("WSL backend stop requested (implement /shutdown route if needed)")
        if self.server_thread:
            self.server_thread.join(timeout=2)
            self.server_thread = None