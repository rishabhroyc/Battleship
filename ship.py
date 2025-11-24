
from typing import List, Tuple


class Ship:
    def __init__(
        self,
        name: str,
        size: int,
        symbol: str,
        coordinates=None,
        hits=None,
    ):
        # Basic data about the ship
        self.name = name          # e.g. "Carrier"
        self.size = size          # length of the ship in cells
        self.symbol = symbol      # 1-letter code, e.g. "C"

        # List of (x, y) positions where the ship is placed
        # If not given, start as "not placed"
        self.coordinates = coordinates if coordinates is not None else []

        # Set of (x, y) positions where this ship has been hit
        self.hits = hits if hits is not None else set()

    def __repr__(self) -> str:
        """
        Helpful string form for debugging.
        """
        return (
            f"Ship(name={self.name!r}, size={self.size!r}, "
            f"symbol={self.symbol!r}, coordinates={self.coordinates!r}, "
            f"hits={self.hits!r})"
        )

    # ---------------- placement helpers ----------------

    def place(self, coords: List[Tuple[int, int]]) -> None:
        """
        Set the coordinates of this ship on the board.
        Board.place_ship(...) calls this after all checks.
        """
        self.coordinates = coords

    def is_at(self, x: int, y: int) -> bool:
        """
        Check if ship occupies cell (x, y).
        """
        return (x, y) in self.coordinates

    # ---------------- combat logic ----------------

    def hit(self, x: int, y: int) -> bool:
        """
        Try to hit this ship at (x, y).

        Returns True if this cell belongs to the ship,
        and records the hit. Otherwise returns False.
        """
        if self.is_at(x, y):
            self.hits.add((x, y))
            return True
        return False

    def is_sunk(self) -> bool:
        
        #Check if the ship has taken 'size' number of hits.
        return len(self.hits) >= self.size

   

    def save_data(self) -> dict:
        """
        Convert this ship into a dict that can be saved as JSON.
        """
        return {
            "name": self.name,
            "size": self.size,
            "symbol": self.symbol,
            # coordinates and hits become normal lists
            "coordinates": list(self.coordinates)
            if self.coordinates is not None
            else [],
            "hits": list(self.hits) if self.hits is not None else [],
        }

    @staticmethod
    def load_data(data: dict) -> "Ship":
    
        #Create a Ship instance from data loaded from JSON.
        
        ship = Ship(data["name"], data["size"], data["symbol"])

        # Convert [x, y] back to (x, y)
        ship.coordinates = [tuple(c) for c in data.get("coordinates", [])]
        ship.hits = set(tuple(h) for h in data.get("hits", []))

        return ship
