from src.core.client import WindowsClient
from src.core.intend_parser import IntendParser




def main():
    windows_client = WindowsClient()
    registry = windows_client.load_registry()
    module_registry = registry.get("module_registry")
    file_registry = registry.get("file_registry")
    intent_parser = IntendParser(registry)

    while True:
        user = input(">>>")
        intent_parser.parser(user)

    




if __name__ == "__main__":
    main()
