from src.core.planner.intents import match_intent
from src.core.planner import templates
from src.core.planner.dsl_validator import validate_graph
from src.core.planner.schemas import PlannerInput


def plan(planner_input):
    intent = match_intent(planner_input.user_input)

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



if __name__ == "__main__":
    planner_input = PlannerInput(
        user_input="prepare my work environment",
        memory={},                 
        system_state={},           
            available_actions={
            "open_folder",
            "launch_app",
            "notify"
        }
    )

    graph = plan(planner_input)
    print(graph)
