from rapidfuzz import process
from pathlib import Path








TEMPLATES = {
    "start_project": [
        {"action": "list_folder_contents", "params": {"folder_name": "projects"}, "store_as": "project_folders", "fetch": "folders"},  # list all projects
        {"action": "fuzzy_select", "params": {"query": "@user_input", "choices": "@project_folders"}, "store_as": "project_name", "func": True},  # select one folder which is the best similar
        {"action": "build_path", "params": {"parent_name": "projects", "folder": "@project_name"}, "store_as": "project_path", "func": True},  

        {"action": "list_instances", "params": {"app_name": "explorer"}, "fetch": "instances", "store_as": "instances"},
        {"action": "find_instance", "params": {"instances": "@instances", "query": "@project_name", "key": "title"}, "store_as": "explorer_instance", "func": True},
        {"action": "open_app", "params": {"app_name": "explorer", "folder_path": "@project_path"}, "is_running": "@explorer_instance", "running_action": {"action": "focus_app", "params": {"app_name": "explorer", "title": "@project_name"}}},  # open explorer with the path

        {"action": "list_instances", "params": {"app_name": "vscode"}, "fetch": "instances", "store_as": "instances"},
        {"action": "find_instance", "params": {"instances": "@instances", "query": "@project_name", "key": "title"}, "store_as": "vscode_instance", "func": True},
        {"action": "open_app", "params": {"app_name": "vscode", "folder_path": "@project_path"}, "is_running": "@vscode_instance", "running_action": {"action": "focus_app", "params": {"app_name": "vscode", "title": "@project_name"}}} # open vscode with the path
    ]
}






class Planner:
    def __init__(self, registry, client):
        self.modules = registry.get("modules", {})
        self.file_registry = registry.get("file_registry", {})
        self.client = client


    def get_plan(self, user_input):
        return {
            "action"
        }
    
    
    def run_plan(self, user_input: str, task: str):
        actions = TEMPLATES.get(task)
        results = {}
        

        for action in actions:
            params = {}
            print("*********************", action.get("action"))
            is_running = action.get("is_running", False)

            if isinstance(is_running, str) and is_running.startswith("@"):
                is_running = is_running[1:]  # remove @
                is_running = results.get(is_running)
       
            if is_running:
                running_action = action.get("running_action", None)
                func = running_action.get("func", None) if running_action else None
                if not func:
                    params = running_action["params"]
                    if params:
                        for key, value in params.items():
                            if isinstance(value, str) and value.startswith("@"):
                                params[key] = results[value[1:]]
                    res = self.client.trigger(running_action["action"], running_action["params"])
                    print(res)
                continue
            
            # -------------------------
            # PARAMETER RESOLUTION
            # -------------------------
            for key, raw_val in action.get("params", {}).items():

                # 1) Direct literal protected with #
                if isinstance(raw_val, str) and raw_val.startswith("#"):
                    params[key] = raw_val[1:]  # strip #

                # 2) Variable substitution: @something
                elif isinstance(raw_val, str) and raw_val.startswith("@"):
                    var_name = raw_val[1:]  # remove @
                    params[key] = (
                        user_input if var_name == "user_input" 
                        else results.get(var_name)
                    )
                    # print(params)

                # 3) Plain literal
                else:
                    params[key] = raw_val

            # -------------------------
            # EXECUTION
            # -------------------------
            if action.get("func"):
                # backend function
                fn = getattr(self, action["action"])
                output = fn(**params)
            else:
                # windows-side action
                res = self.client.trigger(action["action"], params)

                # extract fetched payload
                fetch_key = action.get("fetch")
                if fetch_key:
                    output = res["result"]["data"].get(fetch_key)
                else:
                    output = None

            # -------------------------
            # STORE
            # -------------------------
            if "store_as" in action:
                # print(output)
                results[action["store_as"]] = output
            

        return results


    

    
    def fuzzy_select(self, query, choices):
        match, score, index = process.extractOne(query, choices)
        return match


    def build_path(self, parent_name: str, folder: str) -> str:
        base = self.file_registry.get(parent_name)
        if not base:
            raise ValueError(f"No base path found for: {parent_name}")
        if not folder:
            raise ValueError("Folder name required")

        base_str = str(base)

        # --- CASE 1: Parent is WSL path (/mnt/c/...) ---
        if base_str.startswith("/mnt/"):
            # join using POSIX rules
            if not base_str.endswith("/"):
                base_str += "/"
            return base_str + folder

        # --- CASE 2: Parent is UNC WSL path (\\wsl$\\Ubuntu\home...) ---
        if base_str.lower().startswith("\\\\wsl$"):
            # keep UNC format, join with backslashes only
            if not base_str.endswith("\\") and not base_str.endswith("/"):
                base_str += "\\"
            return base_str + folder

        # --- CASE 3: Parent is Windows path (C:\...) ---
        if ":" in base_str:
            return str(Path(base_str) / folder)

        raise ValueError(f"Unrecognized path format: {base_str}")

        
    def find_instance(self, instances, query, key=None):
        # print("&&&&&&&&&&&&&&&&&&", instances)
        for instance in instances:
            if key:
                value = instance.get(key)
                print(value)
                if value and query in value:
                    return instance
        return None


