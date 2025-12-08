from core.responses import success, failure
from core.client import WindowsClient
from core.logger import logger




class Dispatcher:
    def __init__(self):
        self.windows_client = WindowsClient()
        self.registry = {} 
        self.load_registry()


    def load_registry(self):
        self.registry = self.windows_client.load_registry()
        if self.registry:
            logger.info(f"Dispatcher loaded registry with modules: {list(self.registry.keys())}")
        else:
            logger.warning("Dispatcher failed to load registry or registry is empty")


    def validate_command(self, command: dict):
        """
        Validate that the command exists in the registry
        """
        module = command.get("module")
        action = command.get("action")
        params = command.get("params", {})

        if module not in self.registry:
            return False, f"Module '{module}' not found"

        module_actions = self.registry[module]
        if action not in module_actions:
            return False, f"Action '{action}' not found in module '{module}'"

        return True, None
    

    def execute(self, command: dict):
        """
        Validate and send the command to Windows
        """
        is_valid, err_msg = self.validate_command(command)
        if not is_valid:
            logger.warning(f"Invalid command: {command} - {err_msg}")
            return failure(err_msg)

        module = command["module"]
        action = command["action"]
        params = command.get("params", {})

        # Build endpoint path for WindowsClient
        action_endpoint = f"{module}/{action}"

        try:
            result = self.windows_client.trigger(action_endpoint, params)
            logger.info(f"Dispatched '{module}.{action}' with params {params}")
            return success(result, f"{module}.{action} executed")
        except Exception as e:
            logger.error(f"Dispatcher execution error: {str(e)}")
            return failure(f"Execution error: {str(e)}")
