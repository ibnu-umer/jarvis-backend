from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PlannerInput:
    user_input: str
    memory: Dict[str, Any]
    system_state: Dict[str, Any]
    available_actions: set


@dataclass
class PlannerOutput:
    task_graph: Dict[str, Any]
