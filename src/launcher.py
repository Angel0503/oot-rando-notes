import threading
import time

from back import app_setup, patch_tracker
from back.autotrack_rmg import find_game_block, start_poller
from back.main_menu import MainMenu

RETRY_SECONDS = 10


def connect_to_rmg():
    """Keeps looking for RMG in the background; the menu works meanwhile."""
    print("Scanning for RMG Memory Block...")
    while not find_game_block():
        time.sleep(RETRY_SECONDS)

    print("Ready! Monitoring game memory...")
    start_poller()


def main():
    print("======================================")
    print("  Ocarina of Time RMG Auto-Tracker    ")
    print("======================================\n")

    # Packaged exe: create the data folder + template next to the exe (no-op from source)
    app_setup.prepare(patch_tracker)

    threading.Thread(target=connect_to_rmg, daemon=True).start()

    # Tk must run in the main thread. Closing the menu quits the program.
    MainMenu().run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass