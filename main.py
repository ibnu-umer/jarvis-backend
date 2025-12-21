import asyncio, traceback
try:
    from src.core.planner.planner import Planner, PlannerInput
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
        planner = Planner(registry)

        state_provider = StateProvider()
        executor = Executor(
            controller_client=windows_client,
            state_provider=state_provider,
            file_registry=registry["file_registry"]
        )

        # --- example user input ---
        while True:
            try:
                user_input = input(">>>>")
                planner_input = PlannerInput(
                    user_input=user_input,
                    memory={},                 
                    system_state={},           
                )
                # print("Planner_input", planner_input)

                # --- planning ---
                plan = planner.plan(planner_input)

                # --- execution ---
                result = await executor.execute(user_input, plan)
                await windows_client.close()
                
                # --- report ---
                print("Execution result:")
                print(result)
            except Exception as e:
                print(str(e))

    except Exception as e:
        print(str(e))




if __name__ == "__main__":
    asyncio.run(run())
