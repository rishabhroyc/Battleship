import tkinter as tk
from tkinter import messagebox
from board import Board, GRID_SIZE
from ship import Ship
from game_manager import gm

SHIP_TYPES = [("Carrier",5,"C"),("Battleship",4,"B"),("Cruiser",3,"R"),("Submarine",3,"S"),("Destroyer",2,"D")]

# Color theme
BG_COLOR = "#00111A"      # dark ice-blue
BOARD_COLOR = "#33CCFF"   # glacier blue
TEXT_COLOR = "#FFFFFF"    # white

# Font size
TITLE_FONT_SIZE = 28
SAFETY_FONT_SIZE = 24
LABEL_FONT_SIZE = 20
INSTR_FONT_SIZE = 18
BUTTON_FONT_SIZE = 16
GRID_LABEL_FONT_SIZE = 20

SYMBOL_FONT_SIZE = 18

class BattleshipGUI:
    CELL_SIZE = 36
    PADDING = 56   

    def __init__(self, root):
        self.root = root
        self.root.title("Battleship (Arctic Fleet)")
        self.root.configure(bg=BG_COLOR)

        # Using the game manager file for game logic and file IO
        # GUI-local state:
        self.has_attacked = False

        self.placing_player = 0
        self.placement_mode = None
        self.manual_ship_index = 0
        self.manual_stage = 0
        self.manual_start = None

        self.build_main_menu()

    def build_main_menu(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, padx=24, pady=24, bg=BG_COLOR)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Battleship (Arctic Fleet)", font=(None, TITLE_FONT_SIZE, "bold"),
                 fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=12)

        tk.Button(frame, text="Load previous game", width=28,
                  command=self.load_previous,
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).pack(pady=8)

        tk.Button(frame, text="Start New Game", width=28,
                  command=self.start_new_game,
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).pack(pady=8)

        tk.Button(frame, text="Quit", width=28,
                  command=self.root.quit,
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).pack(pady=8)

    def show_safety_screen(self, player):
        self.root.update_idletasks()

        overlay = tk.Toplevel(self.root)
        sw = self.root.winfo_screenwidth(); sh = self.root.winfo_screenheight()
        overlay.geometry(f"{sw}x{sh}+0+0")
        overlay.configure(bg=BG_COLOR)
        overlay.overrideredirect(True)
        overlay.transient(self.root)
        overlay.lift()
        overlay.grab_set()
        overlay.attributes("-topmost", True)

        frame = tk.Frame(overlay, bg=BG_COLOR)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame,
            text=f"Pass the device to Player {player}.\nClick OK when ready.",
            font=(None, SAFETY_FONT_SIZE),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            justify="center"
        ).pack(padx=40, pady=16)

        tk.Button(
            frame,
            text="OK",
            font=(None, BUTTON_FONT_SIZE),
            command=overlay.destroy,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            activebackground="#002233"
        ).pack(pady=10)

        return overlay

    def load_previous(self):
        data = gm.load_state()
        if data is None:
            messagebox.showinfo("Load", "No saved game found.")
            return

        try:
            # gm.load_state already populated gm.boards and gm.current
            messagebox.showinfo("Load", "Game loaded.")
            self.show_turn_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load saved game: {e}")

    def start_new_game(self):
        gm.reset()
        self.placing_player = 0
        self.show_placement_choice()

    def show_placement_choice(self):
        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, padx=16, pady=16, bg=BG_COLOR)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text=f"Player {self.placing_player+1}: Random or Manual placement?",
            font=(None, LABEL_FONT_SIZE),
            fg=TEXT_COLOR,
            bg=BG_COLOR
        ).pack(pady=12)

        row = tk.Frame(frame, bg=BG_COLOR)
        row.pack()

        tk.Button(row, text="Random", width=14,
                  command=lambda: self.do_random_setup(self.placing_player),
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).grid(row=0, column=0, padx=8)

        tk.Button(row, text="Manual", width=14,
                  command=lambda: self.do_manual_setup(self.placing_player),
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).grid(row=0, column=1, padx=8)

    def do_random_setup(self, p):
        gm.random_setup(p)
        messagebox.showinfo("Placement", f"Player {p+1} ships placed.")
        self.next_after_placement()

    def do_manual_setup(self, p):
        self.placement_mode = "manual"
        self.placing_player = p
        self.manual_ship_index = 0
        self.manual_stage = 0
        self.manual_start = None
        self.show_manual_placement()

    def show_manual_placement(self):
        for w in self.root.winfo_children():
            w.destroy()

        board = gm.get_board(self.placing_player)

        frame = tk.Frame(self.root, padx=12, pady=12, bg=BG_COLOR)
        frame.pack(fill="both", expand=True)

        tk.Label(frame,
                 text=f"Player {self.placing_player+1} Manual Placement",
                 font=(None, LABEL_FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR).pack()

        tk.Label(frame, text="Click start cell then end cell.",
                 font=(None, INSTR_FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=6)

        ship_name, ship_size, ship_sym = SHIP_TYPES[self.manual_ship_index]
        tk.Label(
            frame,
            text=f"Placing: {ship_name} (size {ship_size}) symbol {ship_sym}",
            font=(None, INSTR_FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR
        ).pack(pady=6)

        canvas = tk.Canvas(frame,
                           width=GRID_SIZE * self.CELL_SIZE + 2 * self.PADDING,
                           height=GRID_SIZE * self.CELL_SIZE + 2 * self.PADDING,
                           bg=BOARD_COLOR,
                           highlightthickness=0)
        canvas.pack()

        self._manual_canvas = canvas

        canvas.bind("<Button-1>", lambda ev: self.manual_canvas_click(ev, canvas))
        self.draw_board_on_canvas(canvas, board, show_ships=True)

        tk.Button(frame, text="Cancel", command=self.show_placement_choice,
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).pack(pady=8)

    def manual_canvas_click(self, ev, canvas):
        padding = self.PADDING
        x = (ev.x - padding) // self.CELL_SIZE
        y = (ev.y - padding) // self.CELL_SIZE

        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return

        if self.manual_stage == 0:
            self.manual_start = (x, y)
            self.manual_stage = 1
            self.draw_board_on_canvas(canvas, gm.get_board(self.placing_player),
                                      show_ships=True, highlight_start=self.manual_start)
            return

        start = self.manual_start
        end = (x, y)

        ship_name, ship_size, ship_sym = SHIP_TYPES[self.manual_ship_index]

        placed = gm.place_ship_manual(self.placing_player, ship_name, start, end)
        if not placed:
            messagebox.showerror("Invalid", "Invalid placement. Try again.")
            self.manual_stage = 0
            self.manual_start = None
            self.draw_board_on_canvas(canvas, gm.get_board(self.placing_player), show_ships=True)
            return

        self.draw_board_on_canvas(canvas, gm.get_board(self.placing_player), show_ships=True)

        self.manual_ship_index += 1
        self.manual_stage = 0
        self.manual_start = None

        if self.manual_ship_index >= len(SHIP_TYPES):
            self.root.update_idletasks()
            messagebox.showinfo("Done", f"Player {self.placing_player+1} finished placement.")
            self.next_after_placement()
            return

        self.show_manual_placement()

    def next_after_placement(self):
        if self.placing_player == 0:
            self.placing_player = 1
            overlay = self.show_safety_screen(2)
            overlay.wait_window()
            self.show_placement_choice()
        else:
            messagebox.showinfo("Ready", "Both players finished placing ships.")
            gm.current = 0
            self.show_turn_screen()

    def show_turn_screen(self):
        self.has_attacked = False

        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root, padx=12, pady=12, bg=BG_COLOR)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Player {gm.current+1}'s Turn",
                 font=(None, LABEL_FONT_SIZE, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack()

        boards_frame = tk.Frame(frame, bg=BG_COLOR)
        boards_frame.pack(pady=10)

        own_frame = tk.Frame(boards_frame, bg=BG_COLOR)
        own_frame.grid(row=0, column=0, padx=12)
        tk.Label(own_frame, text="Your board", font=(None, INSTR_FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR).pack()
        own_canvas = tk.Canvas(
            own_frame,
            width=GRID_SIZE * self.CELL_SIZE + 2 * self.PADDING,
            height=GRID_SIZE * self.CELL_SIZE + 2 * self.PADDING,
            bg=BOARD_COLOR,
            highlightthickness=0)
        own_canvas.pack()
        self.draw_board_on_canvas(own_canvas, gm.get_board(gm.current), show_ships=True)

        opp_frame = tk.Frame(boards_frame, bg=BG_COLOR)
        opp_frame.grid(row=0, column=1, padx=12)
        tk.Label(opp_frame, text="Opponent view", font=(None, INSTR_FONT_SIZE), fg=TEXT_COLOR, bg=BG_COLOR).pack()
        opp_canvas = tk.Canvas(
            opp_frame,
            width=GRID_SIZE * self.CELL_SIZE + 2 * self.PADDING,
            height=GRID_SIZE * self.CELL_SIZE + 2 * self.PADDING,
            bg=BOARD_COLOR,
            highlightthickness=0)
        opp_canvas.pack()

        if not self.has_attacked:
            opp_canvas.bind("<Button-1>", lambda ev: self.attack_click(ev, opp_canvas))

        self.draw_board_on_canvas(opp_canvas, gm.get_board(1 - gm.current), show_ships=False)

        ctrl = tk.Frame(frame, bg=BG_COLOR)
        ctrl.pack(pady=10)

        tk.Button(ctrl, text="Save and Quit", command=self.save_and_quit,
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).grid(row=0, column=0, padx=8)
        tk.Button(ctrl, text="Pass device (End Turn)", command=self.pass_device,
                  bg=BG_COLOR, fg=TEXT_COLOR, activebackground="#002233",
                  font=(None, BUTTON_FONT_SIZE)).grid(row=0, column=1, padx=8)

    def draw_board_on_canvas(self, canvas, board, show_ships=False, highlight_start=None):
        canvas.delete("all")
        padding = self.PADDING

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                x1 = padding + x * self.CELL_SIZE
                y1 = padding + y * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                canvas.create_rectangle(x1, y1, x2, y2, outline=TEXT_COLOR, width=4)

                pos = (x, y)
                ch = ""

                if pos in getattr(board, 'hits', set()):
                    ch = "X"
                elif pos in getattr(board, 'misses', set()):
                    ch = "O"
                else:
                    ship_here = None
                    for s in getattr(board, 'ships', []):
                        if pos in s.coordinates:
                            ship_here = s
                            break
                    if show_ships and ship_here:
                        ch = ship_here.symbol
                    elif ship_here and ship_here.is_sunk():
                        ch = ship_here.symbol

                if ch:
                    canvas.create_text(
                        x1 + self.CELL_SIZE / 2,
                        y1 + self.CELL_SIZE / 2,
                        text=ch,
                        font=(None, SYMBOL_FONT_SIZE, 'bold'),
                        fill=TEXT_COLOR
                    )

                if highlight_start and pos == highlight_start:
                    canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2,
                                            outline='red', width=3)

        top_offset = max(12, GRID_LABEL_FONT_SIZE // 2 + 6)
        left_offset = max(14, GRID_LABEL_FONT_SIZE // 2 + 8)

        for i in range(GRID_SIZE):
            letter = chr(ord('A') + i)
            canvas.create_text(
                padding + i*self.CELL_SIZE + self.CELL_SIZE/2,
                padding - top_offset,
                text=letter,
                anchor='s',
                fill=TEXT_COLOR,
                font=(None, GRID_LABEL_FONT_SIZE, 'bold')
            )
            canvas.create_text(
                padding - left_offset,
                padding + i*self.CELL_SIZE + self.CELL_SIZE/2,
                text=str(i+1),
                anchor='e',
                fill=TEXT_COLOR,
                font=(None, GRID_LABEL_FONT_SIZE, 'bold')
            )

    def attack_click(self, ev, opp_canvas):
        if self.has_attacked:
            return

        padding = self.PADDING
        x = (ev.x - padding) // self.CELL_SIZE
        y = (ev.y - padding) // self.CELL_SIZE

        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return

        defender = 1 - gm.current
        result = gm.register_attack(defender, x, y)

        if result == "repeat":
            messagebox.showinfo("Info", "Already attacked there.")
            return
        if result == "miss":
            messagebox.showinfo("Result", "Miss.")
        elif result == "hit":
            messagebox.showinfo("Result", "Hit!")
        elif isinstance(result, str) and result.startswith("sunk:"):
            parts = result.split(":")
            if len(parts) >= 3:
                _, name, sym = parts[:3]
                messagebox.showinfo("Result", f"You sunk the enemy {name}!")
            else:
                messagebox.showinfo("Result", "You sunk a ship!")

        self.has_attacked = True

        self.draw_board_on_canvas(opp_canvas, gm.get_board(defender), show_ships=False)

        victor = self.check_victory()
        if victor:
            messagebox.showinfo("Game Over", f"Player {victor} wins!")
            self.build_main_menu()

    def pass_device(self):
        if not self.has_attacked:
            ok = messagebox.askyesno("End Turn", "You have not attacked. End turn anyway?")
            if not ok:
                return

        gm.current = 1 - gm.current
        overlay = self.show_safety_screen(gm.current + 1)
        overlay.wait_window()
        self.show_turn_screen()

    def check_victory(self):
        if gm.all_sunk(0):
            return 2
        if gm.all_sunk(1):
            return 1
        return 0

    def save_and_quit(self):
        gm.save_state()
        messagebox.showinfo("Saved", "Game saved.")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleshipGUI(root)
    root.mainloop()