import tkinter as tk

from back import autotrack_rmg

BG = "#1e1e24"
ROW_BG = "#2b2b36"
TEXT = "#e0e0e0"
ACCENT = "#fca311"
DIM = "#666666"
GREEN = "#2ecc71"
RED = "#e74c3c"
C_YELLOW = "#f1c40f"   # C buttons
A_BLUE = "#4aa3ff"     # A button
FONT = ("Segoe UI", 11, "bold")
SONG_NAME_FONT = ("Segoe UI", 9, "bold")
SONG_NOTE_FONT = ("Segoe UI", 12, "bold")

# Ocarina notes: A, U = C-up, D = C-down, L = C-left, R = C-right
NOTE_SYMBOLS = {
    "A": ("A", A_BLUE),
    "U": ("↑", C_YELLOW),
    "D": ("↓", C_YELLOW),
    "L": ("←", C_YELLOW),
    "R": ("→", C_YELLOW),
}

SONGS = [
    ("Zelda's Lullaby",    "LURLUR"),
    ("Epona's Song",       "ULRULR"),
    ("Saria's Song",       "DRLDRL"),
    ("Sun's Song",         "RDURDU"),
    ("Song of Time",       "RADRAD"),
    ("Song of Storms",     "ADUADU"),
    ("Minuet of Forest",   "AULRLR"),
    ("Bolero of Fire",     "DADARDRD"),
    ("Serenade of Water",  "ADRRL"),
    ("Nocturne of Shadow", "LRRALRD"),
    ("Requiem of Spirit",  "ADARDA"),
    ("Prelude of Light",   "URURLU"),
]


class DungeonOverlay:
    """Small always-on-top window: dungeon entrances (auto + manual) + song reference."""

    def __init__(self, master=None):
        # Opened from the main menu -> Toplevel; run standalone -> own Tk window
        self.root = tk.Toplevel(master) if master else tk.Tk()
        self._after_id = None
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.title("Dungeons")
        self.root.configure(bg=BG, padx=10, pady=6)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        # ---- Dungeons (auto-filled from RMG, click a destination to set it by hand) ----
        self.values = {name: "" for name in autotrack_rmg.ENTRANCE_ORDER}
        self.dest_vars = {}
        self.dest_buttons = {}
        self.dest_menus = {}
        self._auto_last = {}
        for row, name in enumerate(autotrack_rmg.ENTRANCE_ORDER):
            tk.Label(self.root, text=name.upper(), font=FONT, fg=TEXT, bg=BG,
                     width=6, anchor="w").grid(row=row, column=0, sticky="w", pady=1)
            tk.Label(self.root, text="→", font=FONT, fg=DIM, bg=BG).grid(row=row, column=1, padx=4)

            var = tk.StringVar(value="---")
            button = tk.Menubutton(self.root, textvariable=var, font=FONT, fg=DIM, bg=BG,
                                   activebackground=ROW_BG, activeforeground=TEXT,
                                   width=6, anchor="w", relief="flat", bd=0,
                                   highlightthickness=0, cursor="hand2")
            menu = tk.Menu(button, tearoff=0, bg=ROW_BG, fg=TEXT, activebackground=ACCENT,
                           activeforeground=BG, font=("Segoe UI", 10),
                           postcommand=lambda n=name: self._build_menu(n))
            button.config(menu=menu)
            button.grid(row=row, column=2, sticky="w")

            self.dest_vars[name] = var
            self.dest_buttons[name] = button
            self.dest_menus[name] = menu

        next_row = len(autotrack_rmg.ENTRANCE_ORDER)
        self.status = tk.Label(self.root, text="● No data", font=("Segoe UI", 9, "bold"),
                               fg=RED, bg=BG, anchor="w")
        self.status.grid(row=next_row, column=0, columnspan=3, sticky="w", pady=(6, 0))

        # ---- Songs (click the header to collapse / expand) ----
        self.songs_visible = True
        self.songs_header = tk.Label(self.root, text="▼ SONGS", font=FONT, fg=ACCENT,
                                     bg=BG, anchor="w", cursor="hand2")
        self.songs_header.grid(row=next_row + 1, column=0, columnspan=3, sticky="we", pady=(8, 2))
        self.songs_header.bind("<Button-1>", lambda e: self._toggle_songs())

        self.songs_frame = tk.Frame(self.root, bg=BG)
        self.songs_frame.grid(row=next_row + 2, column=0, columnspan=3, sticky="w")
        for song_name, notes in SONGS:
            tk.Label(self.songs_frame, text=song_name.upper(), font=SONG_NAME_FONT,
                     fg=TEXT, bg=BG, anchor="w").pack(anchor="w")
            notes_row = tk.Frame(self.songs_frame, bg=BG)
            notes_row.pack(anchor="w", pady=(0, 4))
            for code in notes:
                symbol, color = NOTE_SYMBOLS[code]
                tk.Label(notes_row, text=symbol, font=SONG_NOTE_FONT, fg=color,
                         bg=BG, width=2).pack(side="left")

        self._place_window()
        self._refresh()

    def _build_menu(self, name):
        """Rebuild the dropdown: destinations already used elsewhere are greyed out."""
        menu = self.dest_menus[name]
        menu.delete(0, "end")
        menu.add_command(label="---", command=lambda: self._set_dest(name, ""))
        used = {v for n, v in self.values.items() if n != name and v}
        for dest in autotrack_rmg.ENTRANCE_ORDER:
            menu.add_command(label=dest, state="disabled" if dest in used else "normal",
                             command=lambda d=dest: self._set_dest(name, d))

    def _set_dest(self, name, dest):
        self.values[name] = dest
        self.dest_vars[name].set(dest.upper() if dest else "---")
        self.dest_buttons[name].config(fg=ACCENT if dest else DIM)

    def _toggle_songs(self):
        self.songs_visible = not self.songs_visible
        if self.songs_visible:
            self.songs_frame.grid()
            self.songs_header.config(text="▼ SONGS")
        else:
            self.songs_frame.grid_remove()
            self.songs_header.config(text="▶ SONGS")

    def _place_window(self):
        # Top-right corner of the screen; drag the title bar to move it
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() - self.root.winfo_reqwidth() - 40
        self.root.geometry(f"+{x}+30")

    def _refresh(self):
        data = autotrack_rmg.get_latest()

        if data:
            # Only apply an auto value when it changed, so manual edits stick
            for name in autotrack_rmg.ENTRANCE_ORDER:
                dest = data["locations"].get(name, "???")
                if dest == self._auto_last.get(name):
                    continue
                self._auto_last[name] = dest
                if dest in autotrack_rmg.KNOWN_DESTINATIONS:
                    self._set_dest(name, dest)
            self.status.config(text="● Auto-tracker connected", fg=GREEN)
        else:
            self.status.config(text="● RMG not found - manual mode", fg=RED)

        # Re-assert "always on top" in case another window grabbed it
        self.root.attributes("-topmost", True)
        self._after_id = self.root.after(500, self._refresh)

    def _on_close(self):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self.root.destroy()

    def exists(self):
        try:
            return bool(self.root.winfo_exists())
        except tk.TclError:
            return False

    def focus(self):
        self.root.deiconify()
        self.root.lift()

    def run(self):
        self.root.mainloop()