import asyncio, traceback, time
try:
    # from src.core.planner import Planner
    # from src.core.executor import Executor
    # from src.core.client import WindowsClient
    # from src.core.state import StateProvider
    from src.api.listener import WSLBackend
    from src.run_pipeline import initialize_components
    from src.core.logger import logger
except Exception as e:
    print(str(e))
    traceback.print_exc()



REGISTRY = None

async def run():
    try:
        while True:
            planner, executor = await initialize_components()

            if planner:
                break

            time.sleep(5)
            logger.info("Retrying initialization")

        listener = WSLBackend(planner, executor)
        listener.start()
        await asyncio.Event().wait()

    except Exception as e:
        logger.error(f"Init failed: {e}")
        await asyncio.sleep(5)



if __name__ == "__main__":
    try:
        asyncio.run(run())
    except Exception as e:
        print(e)
