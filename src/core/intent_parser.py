from dataclasses import dataclass, field
from typing import Any, Dict, Tuple
from pathlib import Path
import joblib
import re

from src.core.logger import logger





@dataclass
class Intent:
    action: str
    params: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0


class IntentParser:
    CONF_THRESHOLD = 0.3
    EXECUTABLE_SUFFIXES = {".exe", ".com", ".bat", ".cmd", ".msi"}

    def __init__(self, registry: dict):
        self.modules = registry.get("modules", {})
        self.file_registry = registry.get("file_registry", {})

        self.intent_model = joblib.load("src/models/intent_predictor_model.pkl")
        self.vectorizer = joblib.load("src/models/vectorizer.pkl")
        self.label_encoder = joblib.load("src/models/label_encoder.pkl")



    def temp_parse(self, user_input: str) -> Intent:
        text = user_input.lower()

        if "setup" in text and "project" in text:
            return Intent(action="start_project")

        if "open" in text and "project" in text:
            return Intent(action="open_project")

        if "prepare" in text and "work" in text:
            return Intent(action="prepare_work_environment")
        
        if "open copied path" in text:
            return Intent(action="open_copied_path")

        return Intent(action="fallback")


    def parse(self, user_input: str) -> Intent:
        text = user_input.lower()
        intent, confidence = self.predict_intent(text)

        logger.debug(f"Predicted intent={intent}, confidence={confidence}")

        if confidence < self.CONF_THRESHOLD and intent not in user_input:
            return Intent("fallback", confidence=confidence)

        if intent == "open":
            return self._handle_open(text, confidence)

        if intent in ("get_time", "get_date", "get_day"):
            return Intent(
                action="datetime",
                params={"result": intent.split("_")[-1]},
                confidence=confidence,
            )

        if intent in ("volume", "brightness"):
            value, mode = self._extract_slider_params(text)
            return Intent(
                action=intent,
                params={"value": value, "mode": mode},
                confidence=confidence,
            )

        return Intent(action=intent, confidence=confidence)


    # ---------------- Intent Handlers ----------------

    def _handle_open(self, text: str, confidence: float) -> Intent:
        file_key = self._match_registry_key(text)
        if not file_key:
            raise ValueError("No matching file or app found")

        path = self.file_registry[file_key]

        if path.startswith(("http://", "https://")):
            return Intent("open_app", {"app_name": file_key}, confidence)

        wsl_path = Path(self._to_wsl_path(path))

        if wsl_path.is_dir():
            return Intent("open_folder", {"folder_name": file_key}, confidence)

        if wsl_path.is_file():
            if wsl_path.suffix.lower() in self.EXECUTABLE_SUFFIXES:
                return Intent("open_app", {"app_name": file_key}, confidence)
            return Intent("open_file", {"file_name": file_key}, confidence)

        raise ValueError("Unrecognized path type")

    
    # ---------------- Param Extraction ----------------

    def _extract_slider_params(self, text: str) -> Tuple[int | None, str | None]:
        value = self._extract_number(text)

        if any(k in text for k in ("mute", "silent")):
            return 0, "set"

        if any(k in text for k in ("max", "full")):
            return 100, "set"

        if any(k in text for k in ("half", "medium")):
            return 50, "set"

        if any(k in text for k in ("decrease", "lower", "down")):
            return value, "dec"

        if any(k in text for k in ("increase", "raise", "up")):
            return value, "inc"

        if any(k in text for k in ("set", "change")):
            return value, "set"

        return None, None

    
    # ---------------- Helpers ----------------

    def _match_registry_key(self, text: str) -> str | None:
        for key in self.file_registry:
            if key in text:
                return key
        return None
    

    def _extract_number(self, text: str) -> int | None:
        match = re.search(r"\b(?:by|to)\s+(\d+)\b", text)
        return int(match.group(1)) if match else None


    def _to_wsl_path(self, windows_path: str) -> str:
        drive = windows_path[0].lower()
        tail = windows_path[2:].replace("\\", "/")
        return f"/mnt/{drive}/{tail}"

   
    # ---------------- ML Model ----------------

    def predict_intent(self, text: str) -> Tuple[str, float]:
        vect = self.vectorizer.transform([text])
        pred = self.intent_model.decision_function(vect)
        idx = pred.argmax()

        intent = self.label_encoder.inverse_transform([idx])[0]
        confidence = float(abs(pred[0][idx]))

        return intent, confidence




    # --------------- TASK LEVEL PARSING -------------------
