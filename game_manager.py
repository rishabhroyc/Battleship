"""
Controls the main Battleship game logic (NOT the GUI):
Holds 2 boards (one for each player)
Places ships (manual or random)
Handles attacks and turn switching
Saves & loads game state using FileManager
"""

from board import Board, GRID_SIZE
from ship import Ship
from file_manager import FileManager
import random
from typing import Tuple, List, Optional
# All types of ships used in the game
SHIP_TYPES = [
    ("Carrier", 5, "C"),
    ("Battleship", 4, "B"),
    ("Cruiser", 3, "R"),
    ("Submarine", 3, "S"),
    ("Destroyer", 2, "D"),
]
class GameManager:
    
    #Keeps track of everything related to gameplay logic.
    

    def __init__(self):
        # Each player has their own Board
        self.boards = [Board(), Board()]

        # Player index whose turn it currently is (0 or 1)
        self.current = 0

        # Handles saving/loading files
        self.fm = FileManager()


    def save_state(self, path: Optional[str] = None):
        """
        Save the entire game state to JSON:
        - current player's turn
        - both boards (ships, hits, misses)
        """
        state = {
            "current": self.current,
            "boards": [b.save_data() for b in self.boards],
        }

        # If no custom file path, save to the default file
        if path is None:
            self.fm.save_state(state)
        else:
            # Save to a custom location (if added)
            self.fm.save_state_to(path, state)


    def load_state(self):
        """
        Load game state from JSON file and rebuild boards.
        Returns None if no save file exists.
        """
        data = self.fm.load_state()
        if data is None:
            return None

        # Restore whose turn it is
        self.current = data.get("current", 0)

        # Rebuild both boards from saved data
        self.boards = [Board.load_data(bd) for bd in data.get("boards", [])]

        return data


    def place_all_ships_random(self, player: int):
        """
        Randomly place all ships for the given player.
        Makes many attempts until valid placement is found.
        """
        board = self.boards[player]

        for name, size, sym in SHIP_TYPES:
            placed = False
            tries = 0

            # Keep trying until ship is placed
            while not placed and tries < 1000:
                tries += 1

                # Random orientation
                orient = random.choice(["H", "V"])

                # Random starting cell
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)

                # Compute end cell based on orientation
                if orient == "H":
                    end = (x + size - 1, y)
                else:
                    end = (x, y + size - 1)

                # Create ship object
                ship = Ship(name, size, sym)

                # Try placing it on board
                placed = board.place_ship(ship, (x, y), end)

            if not placed:
                raise RuntimeError("Failed to randomly place ship after many tries.")


    def place_ship_manual(
        self,
        player: int,
        ship_name: str,
        start: Tuple[int, int],
        end: Tuple[int, int],
    ) -> bool:
        
        # Place one ship manually for a player.

        # Returns True if successfully placed.
        
        # Find the ship definition by name
        for name, size, sym in SHIP_TYPES:
            if name == ship_name:
                ship = Ship(name, size, sym)
                return self.boards[player].place_ship(ship, start, end)

        return False  # Should not happen unless name is wrong


    def attack(self, attacker: int, x: int, y: int) -> str:
        """
        The attacker shoots at (x, y) on the defender's board.
        Returns result string: hit, miss, sunk, sunk_all, repeat.
        """
        defender = 1 - attacker  # Switch player index (if 0 then 1 & if 1 then 0)

        result = self.boards[defender].receive_attack(x, y)

        # If the move was valid (not repeat), turn switches to defender
        if result != "repeat":
            self.current = defender

        return result


    def all_sunk(self, player: int) -> bool:
        """Check if all ships of a player are destroyed."""
        return self.boards[player].all_sunk()


    def get_board(self, player: int) -> Board:
        """Return the board belonging to a player."""
        return self.boards[player]

    def reset(self):
        """Reset the game: new empty boards, set turn to Player 1."""
        self.boards = [Board(), Board()]
        self.current = 0
# Global instance used by the GUI
gm = GameManager()
