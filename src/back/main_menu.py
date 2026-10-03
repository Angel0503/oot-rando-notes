import asyncio
import os
import threading
import tkinter as tk
import webbrowser

from back import autotrack_rmg, patch_tracker
from back.dungeon_overlay import DungeonOverlay
from back.web_server import start_http_server

BG = "#1e1e24"
ROW_BG = "#2b2b36"
TEXT = "#e0e0e0"
ACCENT = "#fca311"
GREEN = "#2ecc71"
RED = "#e74c3c"
WEB_URL = "http://127.0.0.1:8000"


class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OoT RMG Auto-Tracker")
        self.root.configure(bg=BG, padx=24, pady=18)
        self.root.resizable(False, False)

        self.overlay = None

        # The local web server runs quietly in the background
        threading.Thread(target=start_http_server, daemon=True).start()

        tk.Label(self.root, text="OOT RANDO TRACKER", font=("Segoe UI", 16, "bold"),
                 fg=ACCENT, bg=BG).pack(pady=(0, 2))
        self.rmg_status = tk.Label(self.root, text="", font=("Segoe UI", 9, "bold"), bg=BG)
        self.rmg_status.pack(pady=(0, 14))

        self._make_button("Open tracker (web)", self.open_web)
        self._make_button("Open dungeon overlay", self.open_overlay)
        self.generate_btn = self._make_button("Generate tracker file", self.generate_file)
        self._make_button("Open output folder", self.open_output_folder)

        self.message = tk.Label(self.root, text="", font=("Segoe UI", 9), fg=TEXT, bg=BG,
                                wraplength=300, justify="left")
        self.message.pack(pady=(10, 0))

        self._refresh_status()

    def _make_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command, width=28,
                           font=("Segoe UI", 11, "bold"), fg=TEXT, bg=ROW_BG,
                           activebackground=ACCENT, activeforeground=BG,
                           relief="flat", bd=0, pady=8, cursor="hand2")
        button.pack(pady=4)
        return button

    def _set_message(self, text, color=TEXT):
        self.message.config(text=text, fg=color)

    def _refresh_status(self):
        if autotrack_rmg.GAME_BASE_ADDRESS != 0:
            self.rmg_status.config(text="● RMG connected", fg=GREEN)
        else:
            self.rmg_status.config(text="● Searching for RMG...", fg=RED)
        self.root.after(1000, self._refresh_status)

    # ---- Actions ----
    def open_web(self):
        webbrowser.open(WEB_URL)

    def open_overlay(self):
        if self.overlay and self.overlay.exists():
            self.overlay.focus()
            return
        self.overlay = DungeonOverlay(self.root)

    def generate_file(self):
        if autotrack_rmg.GAME_BASE_ADDRESS == 0:
            self._set_message("RMG not found yet. Start RMG, load your save, then try again.", RED)
            return
        self.generate_btn.config(state="disabled")
        self._set_message("Generating...", TEXT)
        threading.Thread(target=self._generate_worker, daemon=True).start()

    def _output_path(self):
        # Same output path that patch_tracker computes (absolute paths win in os.path.join)
        patch_dir = os.path.dirname(os.path.abspath(patch_tracker.__file__))
        return os.path.abspath(os.path.join(patch_dir, patch_tracker.OUTPUT_PATH))

    def open_output_folder(self):
        folder = os.path.dirname(self._output_path())
        os.makedirs(folder, exist_ok=True)
        if hasattr(os, "startfile"):
            os.startfile(folder)
        else:
            webbrowser.open(folder)

    def _generate_worker(self):
        output = self._output_path()
        before = os.path.getmtime(output) if os.path.exists(output) else None

        try:
            asyncio.run(patch_tracker.modify_tracker_json())
        except Exception as e:
            print(f"[-] Generation error: {e}")

        after = os.path.getmtime(output) if os.path.exists(output) else None
        ok = after is not None and after != before
        self.root.after(0, lambda: self._generation_done(ok, output))

    def _generation_done(self, ok, output):
        self.generate_btn.config(state="normal")
        if ok:
            self._set_message(f"File generated:\n{output}", GREEN)
        else:
            self._set_message("Generation failed (is your save loaded? is the template found?). "
                              "See the console for details.", RED)

    def run(self):
        self.root.mainloop()