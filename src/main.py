from src.core.sender import Sender
from src.api.listener import WSLBackend



def main():
    wsl_api = WSLBackend()
    wsl_api.start()
    
    sender = Sender()
    response = sender.trigger("lock")
    print(response)


if __name__ == "__main__":
    main()