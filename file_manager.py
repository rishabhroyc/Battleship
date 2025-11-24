
import json
from typing import Any, Dict, Optional
class FileManager:
    """
    Manages writing and reading files used by the game.
    """

    def __init__(
        self,
        result_filename: str = "battleship_save.txt",
        state_filename: str = "battleship_state.json",
    ):
        # Filenames for text and JSON save files
        self.result_filename = result_filename
        self.state_filename = state_filename

    def save_result(self, text: str) -> None:
        """
        Save plain text (like logs or summary) to a text file.
        Overwrites previous contents.
        """
        with open(self.result_filename, "w") as f:
            f.write(text)

    def save_state(self, state: Dict[str, Any]) -> None:
        """
        Save full game state as JSON.
        'state' must contain only JSON-friendly types.
        """
        with open(self.state_filename, "w") as f:
            json.dump(state, f)

    def load_state(self) -> Optional[Dict[str, Any]]:
        """
        Load game state from JSON file.
        Returns the dictionary if file exists,
        else returns None.
        """
        try:
            with open(self.state_filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # No saved game available
            return None
