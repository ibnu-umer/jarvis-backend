from core.client import WindowsClient
from src.api.listener import WSLBackend



def main():
    wsl_api = WSLBackend()
    wsl_api.start()
    
    windows_client = WindowsClient()
    registry = windows_client.load_registry()
    print(registry)

    response = windows_client.trigger(
        "get_screenusage_today",
        # params={
        #     "interface_name": "WiFi"
        # }
    )
    

    

    
    print(response)


if __name__ == "__main__":
    main()