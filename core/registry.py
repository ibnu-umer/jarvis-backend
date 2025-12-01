from core.base_module import BaseModule
import importlib, os






FUNCTION_REGISTRY = {}

def action(name=None, params=None):
    def wrapper(func):
        module = func.__module__
        qual = func.__qualname__.split(".")
        cls_name = qual[-2] if len(qual) > 1 else None

        FUNCTION_REGISTRY[name or func.__name__] = {
            "module": module,
            "class": cls_name,
            "function": func.__name__,
            "params": params or [],
        }
        return func
    return wrapper



MODULE_INSTANCES = {}

def load_all_modules():
    modules_path = os.path.join(os.path.dirname(__file__), "..", "modules")
    
    for file in os.listdir(modules_path):
        if file.endswith(".py") and file != "__init__.py":
            importlib.import_module(f"modules.{file[:-3]}")

    for subclass in BaseModule.__subclasses__():
        MODULE_INSTANCES[subclass.__name__] = subclass()

load_all_modules()
