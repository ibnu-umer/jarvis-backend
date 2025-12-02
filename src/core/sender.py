import requests
import subprocess
import json



def get_windows_ip():
    # WSL2 host IP is usually the default gateway
    try:
        route = subprocess.check_output("ip route | grep default", shell=True).decode()
        return route.split()[2]  # the gateway IP
    except Exception:
        raise RuntimeError("Unable to detect Windows host IP from WSL")



class Sender:
    def __init__(self):
        self.base_url = f"http://{get_windows_ip()}:6001"


    def trigger(self, action, params=None, timeout=5):
        print("triggering", action)
        params = params or {}
        url = f"{self.base_url}/action/{action}"
        print(url)
        try:
            resp = requests.post(url, json=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.Timeout:
            return {"error": f"Request timed out after {timeout}s. Windows listener may be offline."}
        except requests.ConnectionError:
            return {"error": "Cannot connect to Windows listener. Is it running?"}
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}


