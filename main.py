from core.registry import FUNCTION_REGISTRY
from core.dispatcher import Dispathcer





def main():
    dispatcher = Dispathcer()
    dispatcher.dispatch("volume", value=50)


if __name__ == "__main__":
    main()