import asyncio, traceback
try:
    from src.core.planner.planner import plan, PlannerInput
    from src.core.executor import Executor
    from src.core.client import WindowsClient
    from src.core.state import StateProvider
except Exception as e:
    print(str(e))
    traceback.print_exc()





async def run():
    try:
        # --- init core components ---
        windows_client = WindowsClient()
        registry = await windows_client.load_registry()

        state_provider = StateProvider()
        executor = Executor(
            controller_client=windows_client,
            state_provider=state_provider,
            file_registry=registry["file_registry"]
        )

        # --- example user input ---
        user_input = "open copied path"
        planner_input = PlannerInput(
            user_input=user_input,
            memory={},                 
            system_state={},           
            available_actions={
                "open_app",
                "open_folder",
                "launch_app",
                "notify"
            }
        )
        print("Planner_input", planner_input)

        # --- planning ---
        task_graph = plan(planner_input)
        if not task_graph:
            print("Planner failed to generate a task graph")
            return
        
        # print("Task Graph: ", task_graph)

        # --- execution ---
        result = await executor.execute(user_input, task_graph)
        await windows_client.close()
        # --- report ---
        print("Execution result:")
        print(result)

    except Exception as e:
        print(str(e))




if __name__ == "__main__":
    asyncio.run(run())
