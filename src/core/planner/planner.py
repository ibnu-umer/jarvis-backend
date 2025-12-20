from src.core.planner.intent_parser import IntentParser
from src.core.planner import templates
from dataclasses import dataclass
from typing import Dict, Any




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

        if intent is None:
            raise RuntimeError("Planner cannot handle this intent")

        if intent == "prepare_work_environment":
            graph = templates.prepare_work_environment()
        elif intent == "start_project":
            graph = templates.start_project()
        elif intent == "open_copied_path":
            graph = templates.open_copied_path()
        else:
            raise RuntimeError("Unhandled intent")

        # validate_graph(graph, planner_input.available_actions)
        return graph
   





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


