from src.core.planner.intent_parser import IntentParser
from src.core.planner import templates
from dataclasses import dataclass
from typing import Dict, Any
from src.core.logger import logger
from src.core.planner.templates import TEMPLATE_REGISTRY
import importlib



@dataclass
class PlannerInput:
    user_input: str
    memory: Dict[str, Any]
    system_state: Dict[str, Any]


@dataclass
class PlannerOutput:
    task_graph: Dict[str, Any]




class Planner:
    def __init__(self, registry):
        self.intent_parser = IntentParser(registry)






    def plan(self, planner_input):
        intent_obj = self.intent_parser.temp_parse(planner_input.user_input)
        intent = intent_obj.action
        logger.info(f"intent: {intent_obj}")

        # handle templates
        func_info = TEMPLATE_REGISTRY.get(intent) if intent in TEMPLATE_REGISTRY else None
        if func_info:
            module = importlib.import_module(func_info["module"])
            graph = getattr(module, func_info["function"])()
            return graph

        if intent == "fallback":
            intent_obj = self.intent_parser.parse(planner_input.user_input)
        
        return intent_obj




    def validate_graph(graph: dict, available_actions: set):
        tg = graph["task_graph"]
        nodes = tg["nodes"]

        if tg["entry"] not in nodes:
            raise ValueError("Invalid entry node")

        
        for node_id, node in nodes.items():

            # check the action node with the avialable actions
            if node["type"] == "action":
                if node["controller"] not in available_actions:
                    raise ValueError(f"Unknown controller: {node['controller']}")


