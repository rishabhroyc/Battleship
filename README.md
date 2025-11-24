# Battleship
A two-player Battleship game implemented in Python, using a clean modular structure that separates game logic, ship rules, board management, and save/load functionality. The project allows players to place ships (manually or randomly), take turns attacking each other’s boards, and continue previously saved games.
## Project Description

The project recreates the standard Battleship experience on a 10×10 grid. Each player places a fleet of five ships either manually (by selecting start and end coordinates) or automatically through valid random placement.

Players then alternate turns, firing at the opponent’s board. Every shot is evaluated as a hit, miss, or ship sink. Repeated shots are prevented, and the game concludes when all ships of one player are destroyed. The full game state—including ship positions, hits, misses, and the current turn—can be saved and loaded at any time.
## Features

Proper Battleship mechanics: straight-line placement, correct ship lengths, no overlaps, in-bounds validation.

Reliable combat handling: hit, miss, sunk ship, and full-fleet defeat detection.

Manual and random ship placement options.

Turn management and rule enforcement handled through a clean game manager.

Complete JSON-based save/load support for resuming matches.

Clear modular structure with separate files for ships, board logic, game control, and saving.

## Directory Structure
battleship_clean_with_manager


├── ship.py             - Ship logic (size, hits, sunk, serialization)

├── board.py            - Placement rules, attack handling, board state

├── game_manager.py     - Turns, placement control, attacks, saving/loading

├── file_manager.py     - JSON save/load helper

├── main.py             - Interaction entry point (GUI)

└── battleship_state.json  - Created automatically when saving
## Game Instructions
Start the game

Run : python main.py


Choose New Game or Load Previous Game.

Place ships

Choose Manual (select start → end coordinates), or

Random placement for quick setup.

Take turns attacking

Select a cell on the opponent’s grid.

The game reports: Hit, Miss, Ship Sunk, or All Ships Sunk.

Win condition : A player wins when all five of the opponent’s ships are destroyed.

Saving : The complete state is saved automatically and can be loaded later.

