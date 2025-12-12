from rapidfuzz import process
from pathlib import Path
import json
from configs.config import TEMPLATES_PATH



class Planner:
    def __init__(self, registry, client):
        self.modules = registry.get("modules", {})
        self.file_registry = registry.get("file_registry", {})
        self.TEMPLATES = self._load_templates()
        self.client = client


    # ---------------------- PUBLIC API ----------------------

    def run_plan(self, user_input: str, task: str):
        actions = self.TEMPLATES.get(task)
        if not actions:
            raise ValueError(f"No template found for: {task}")

        results = {}

        for action in actions:
            action_name = action["action"]

            if self._should_handle_running(action, results):
                self._execute_running_action(action, results)
                continue
            print(">>>>>>>", action.get("params", {}))
            params = self._resolve_params(action.get("params", {}), results, user_input)
            output = self._execute_action(action, params)

            if "store_as" in action:
                results[action["store_as"]] = output

        return results


    # ---------------------- PARAMETER RESOLUTION ----------------------

    def _resolve_params(self, raw_params, results, user_input):
        params = {}

        for key, raw_val in raw_params.items():
            if isinstance(raw_val, str):
                if raw_val.startswith("#"):
                    params[key] = raw_val[1:]

                elif raw_val.startswith("@"):
                    var_name = raw_val[1:]
                    params[key] = user_input if var_name == "user_input" else results.get(var_name)

                else:
                    params[key] = raw_val
            else:
                params[key] = raw_val

        return params


    # ----------------- RUNNING INSTANCE HANDLING -----------------

    def _should_handle_running(self, action, results):
        is_running = action.get("is_running")
        if not is_running:
            return False

        if isinstance(is_running, str) and is_running.startswith("@"):
            key = is_running[1:]
            return results.get(key) is not None

        return bool(is_running)


    def _execute_running_action(self, action, results):
        running_action = action.get("running_action")
        if not running_action:
            return

        params = self._resolve_params(running_action.get("params", {}), results, None)
        self.client.trigger(running_action["action"], params)


    # ---------------------- EXECUTION LOGIC ----------------------

    def _execute_action(self, action, params):
        if action.get("func"):  # internal python method
            fn = getattr(self, action["action"])
            return fn(**params)

        # client-side Windows action
        res = self.client.trigger(action["action"], params)
        # print(res)

        fetch = action.get("fetch")
        if fetch:
            return res["result"]["data"].get(fetch)

        return None

  
    # ---------------------- INTERNAL FUNCTIONS ----------------------

    def _load_templates(self):
        with open(TEMPLATES_PATH, "r") as file:
            return json.load(file)
        

    def fuzzy_select(self, query, choices):
        match, score, idx = process.extractOne(query, choices)
        return match


    def build_path(self, parent_name: str, folder: str) -> str:
        base = self.file_registry.get(parent_name)
        if not base:
            raise ValueError(f"No base path found for: {parent_name}")

        if not folder:
            raise ValueError("Folder name required")

        base_str = str(base)

        # WSL-style /mnt/
        if base_str.startswith("/mnt/"):
            return f"{base_str.rstrip('/')}/{folder}"

        # UNC WSL \\wsl$\
        if base_str.lower().startswith("\\\\wsl$"):
            return f"{base_str.rstrip('\\\\')}/{folder}".replace("/", "\\")

        # Windows paths C:\
        if ":" in base_str:
            return str(Path(base_str) / folder)

        raise ValueError(f"Unrecognized path format: {base_str}")
    

    def find_instance(self, instances, query, key=None):
        for inst in instances:
            value = inst.get(key) if key else None
            if value and query in value:
                return inst
        return None
