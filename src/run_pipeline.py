try:
    from src.core.planner import PlannerInput, Planner
    from src.core.client import WindowsClient
    from src.core.planner import Planner
    from src.core.executor import Executor
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

    return {
        "plan": plan,
        "result": result
    }
