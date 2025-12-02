from core.registry import FUNCTION_REGISTRY, MODULE_INSTANCES




class Dispathcer:
    def dispatch(self, name, *args, **kwargs):
        info = FUNCTION_REGISTRY.get(name)
        if not info:
            raise ValueError(f"Action '{name}' not found")

        instance = MODULE_INSTANCES.get(info["class"])
        if not instance:
            raise RuntimeError(f"Instance for class {info['class']} not loaded")

        method = getattr(instance, info["function"])
        return method(*args, **kwargs)
