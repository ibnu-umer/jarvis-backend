import subprocess, httpx
from src.core.logger import logger


class WindowsClient:
    def __init__(self):
        self.base_url = f"http://{self._get_windows_ip()}:6001"

    def _get_windows_ip(self):
        # WSL2 host IP is usually the default gateway
        try:
            route = subprocess.check_output("ip route | grep default", shell=True).decode()
            ip = route.split()[2]  # the gateway IP
            logger.info(f"Detected Windows host IP: {ip}")
            return ip
        except Exception as e:
            logger.error("Unable to detect Windows host IP from WSL", exc_info=e)
            raise RuntimeError("Unable to detect Windows host IP from WSL") from e
        

    async def trigger(self, action, params=None, timeout=5):
        # print("in trigger >>>>>>>>>>>", action, params)
        params = params or {}
        url = f"{self.base_url}/action/{action}"
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(url, json=params)
                resp.raise_for_status()
                logger.info(f"Triggered action '{action}' with params: {params}")
                return resp.json()
        except httpx.TimeoutException:
            logger.warning(f"Request timed out after {timeout}s for action '{action}'")
            return {"error": f"Request timed out after {timeout}s. Windows listener may be offline."}
        except httpx.ConnectError:
            logger.error(f"Cannot connect to Windows listener at {self.base_url}")
            return {"error": "Cannot connect to Windows listener. Is it running?"}
        except httpx.HTTPStatusError as e:
            logger.error(f"Request failed for action '{action}': {str(e)}")
            return {"error": f"Request failed: {str(e)}"}
        

    async def load_registry(self, timeout=5):
        url = f"{self.base_url}/registry"
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.get(url)
                resp.raise_for_status()
                logger.info("Loaded action registry")
                return resp.json()

        except httpx.RequestError as e:
            logger.error(f"Failed to load registry from {self.base_url}: {str(e)}")
            return {}
        

    async def close(self):
        pass
