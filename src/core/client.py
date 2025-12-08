import requests
import subprocess



class WindowsClient:
    def __init__(self):
        self.base_url = f"http://{self._get_windows_ip()}:6001"


    def _get_windows_ip(self):
        # WSL2 host IP is usually the default gateway
        try:
            route = subprocess.check_output("ip route | grep default", shell=True).decode()
            return route.split()[2]  # the gateway IP
        except Exception:
            raise RuntimeError("Unable to detect Windows host IP from WSL")


    def trigger(self, action, params=None, timeout=5):
        params = params or {}
        url = f"{self.base_url}/action/{action}"
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
        

    def load_registry(self, timeout=5):
        url = f"{self.base_url}/registry"
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                print("[WSL] Loaded action registry")
                return resp.json().get("modules", {})
            else:
                print("[WSL] Failed to load registry:", resp.text)
                return resp.text
        except Exception as e:
            print("[WSL] Registry load error:", str(e))
            return str(e)


