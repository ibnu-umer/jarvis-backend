try:
    from src.core.planner import PlannerInput, Planner
    from src.core.intent_parser import Intent
    from src.core.client import WindowsClient
    from src.core.planner import Planner
    from src.core.executor import Executor, ExecutionResult
    from src.core.client import WindowsClient
    from src.core.state import StateProvider
except Exception as e:
    print(e)





async def initialize_components():
    windows_client = WindowsClient()
    registry = await windows_client.load_registry()

    if registry:
        planner = Planner(registry)
        state_provider = StateProvider()

        executor = Executor(
            controller_client=windows_client,
            state_provider=state_provider,
            file_registry=registry["file_registry"]
        )
        return planner, executor
    
    return None, None





async def run_pipeline(user_input: str, planner, executor):
    planner_input = PlannerInput(
        user_input=user_input,
        memory={},
        system_state={}
    )
    
    plan = planner.plan(planner_input)
    result = await executor.execute(user_input, plan)

    return serialize_plan(plan), serialize_result(result)




def serialize_plan(plan):
        if isinstance(plan, Intent):
            return {
                "type": "intent",
                "action": plan.action,
                "params": plan.params,
                "confidence": plan.confidence,
            }

        if isinstance(plan, dict):
            return {
                "type": "task_graph",
                "graph": plan,
            }

        raise TypeError(f"Unknown plan type: {type(plan)}")
    

def serialize_result(result):
    if isinstance(result, dict):
        return {
            "type": "action_result",
            **result,
        }

    if isinstance(result, ExecutionResult):
        return {
            "type": "graph_result",
            "graph_id": result.graph_id,
            "status": result.status,
            "executed_nodes": result.executed_nodes,
            "failed_node": result.failed_node,
            "error": result.error,
            "context": result.context,
        }

    raise TypeError(f"Unknown result type: {type(result)}")


