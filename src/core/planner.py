import json, os
from rapidfuzz import process
from pathlib import Path
from configs.config import TEMPLATES_PATH
from src.core.logger import logger



class Planner:
    def __init__(self, registry, client):
        self.modules = registry.get("modules", {})
        self.file_registry = registry.get("file_registry", {})
        self.TEMPLATES = self._load_templates()
        self.client = client


    # ---------------------- PUBLIC API ----------------------

    async def run_plan(self, user_input: str, task: str, values: dict = {}):
        actions = self.TEMPLATES.get(task)
        if not actions:
            raise ValueError(f"No template found for: {task}")

        results = {}
        results.update(values)

        for action in actions:
            action_name = action["action"]

            if self._should_handle_running(action, results):
                self._execute_running_action(action, results)
                continue

            params = self._resolve_params(action.get("params", {}), results, user_input)
            status, output, message = await self._execute_action(action, params)
           
            if not status and action.get("fallback_action", None):
                fallback_action = action.get("fallback_action")
                params = self._resolve_params(fallback_action["params"], results, user_input)
                status, output, message = await self._execute_action(fallback_action, params)

            if not status:
                logger.info("Plan running stopped")
                logger.info(f"{action_name} failed: {message}")
                break

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
                    if "::" in var_name:
                        var_name, key_arg = var_name.split("::")
                        params[key] = results[var_name].get(key_arg)
                    else:
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

    async def _execute_action(self, action, params):
        if action.get("func", None):  # internal python method
            fn = getattr(self, action["action"])
            return True, fn(**params)

        # client-side Windows action
        res = await self.client.trigger(action["action"], params)
        
        try:
            fetch = action.get("fetch", None)
            data = res["result"]["data"].get(fetch) if fetch else res["result"]["data"]
            return res["result"]["success"], data, res["result"]["message"]
        except Exception as e:
            return False, res, str(e)

  
    # ---------------------- INTERNAL FUNCTIONS ----------------------

    def _load_templates(self):
        with open(TEMPLATES_PATH, "r") as file:
            return json.load(file)
        

    def fuzzy_select(self, query, choices):
        match, score, idx = process.extractOne(query, choices)
        return match


    def build_path(self, parent_name: str = None, folder: str = None, path: str = None) -> str:
        if path:
            path = path.strip()

            # Convert Windows path → WSL accessible
            if ":" in path and "\\" in path:
                # Windows → /mnt/c style
                drive = path[0].lower()
                rest = path[2:].replace("\\", "/")
                wsl_path = f"/mnt/{drive}/{rest}"

                # optional check (works in WSL for both files/folders)
                exists = os.path.exists(wsl_path)

                return wsl_path if exists else path  # fallback to original

            # Already WSL-style path
            if path.startswith("/") and os.path.exists(path):
                return path

            return path


        if parent_name and not folder:
            base = self.file_registry.get(parent_name)
            if not base:
                raise ValueError(f"No base path found for: {parent_name}")
            return str(base)


        if parent_name and folder:
            base = self.file_registry.get(parent_name)
            if not base:
                raise ValueError(f"No base path found for: {parent_name}")

            base_str = str(base)

            # WSL Unix: /mnt/c/projects
            if base_str.startswith("/mnt/"):
                return f"{base_str.rstrip('/')}/{folder}"

            # UNC (Windows path exposed to WSL): \\wsl$
            if base_str.lower().startswith("\\\\wsl$"):
                return f"{base_str.rstrip('\\')}\\{folder}"

            # Windows-style path: C:\projects
            if ":" in base_str:
                win = str(Path(base_str) / folder)
                # Convert to WSL so WSL-side can verify load-it
                drive = win[0].lower()
                rest = win[2:].replace("\\", "/")
                return f"/mnt/{drive}/{rest}"

            raise ValueError(f"Unrecognized path format: {base_str}")

        raise ValueError("Invalid path arguments")
    

    def find_instance(self, instances, query, key=None):
        for inst in instances:
            value = inst.get(key) if key else None
            if value and query in value:
                return inst
        return None


    def get_folder_name(self, instance: dict):
        title = instance.get("title")
        name_part = title.split("-")[1]
        return name_part.replace("[WSL: Ubuntu]", "") if "[WSL: Ubuntu]" in name_part else name_part

