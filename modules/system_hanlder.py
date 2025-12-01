from core.helpers import confirm_with_timeout
import subprocess
from core.registry import action
from core.base_module import BaseModule



class SystemHandler(BaseModule):
    NIRCMD = r"C:\Tools\nircmd\nircmd.exe"

    @action(name="shutdown")
    def shutdown(self):
        if confirm_with_timeout("Shutdown in 5 seconds?", "Confirm Shutdown"):
            subprocess.Popen(["shutdown", "/s", "/t", "0"])
            return self.success("Shutting down")
        return self.success("Cancelled")
    

    @action(name="restart")
    def restart(self):
        if confirm_with_timeout("Restart in 5 seconds?", "Confirm Restart"):
            subprocess.Popen(["shutdown", "/r", "/t", "0"])
            return self.success("Restarting")
        return self.success("Cancelled")
    

    @action(name="logout")
    def logout(self):
        if confirm_with_timeout("Logout in 5 seconds?", "Confirm Logout"):
            subprocess.Popen(["shutdown", "/l"])
            return self.success("Logging out")
        return self.success("Cancelled")
    

    @action(name="sleep")
    def sleep(self):
        if confirm_with_timeout("Sleep in 5 seconds?", "Confirm Sleep"):
            subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "Sleep"])
            return self.success("Sleeping")
        return self.success("Cancelled")
    

    @action(name="lock")
    def lock(self):
        subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])
        return self.success("Locked")
    

    @action(name="brightness", params={"value"})
    def brightness(self, value):
        value = max(0, min(100, value))
        subprocess.run(["cmd.exe", "/c", self.NIRCMD, "setbrightness", str(value)])
        return self.success(f"Brightness set to {value}%")
    

    @action(name="volume", params={"value"})
    def volume(self, value): 
        value = int(65535 * (value / 100))
        subprocess.run(["cmd.exe", "/c", self.NIRCMD, "setsysvolume", str(value)]) 
        return self.success(f"Volume set to {value}%")
