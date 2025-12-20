class StateProvider:
    def evaluate(self, condition: str) -> bool:
        if condition == "player_ready":
            return self._is_vlc_running()

        if condition == "clipboard_has_path":
            return self._clipboard_has_valid_path()

        raise ValueError(f"Unknown condition: {condition}")

    def _is_vlc_running(self) -> bool:
        # os / psutil check
        return False

    def _clipboard_has_valid_path(self) -> bool:
        return True