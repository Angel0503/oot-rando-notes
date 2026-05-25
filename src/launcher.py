import threading
import webbrowser
import asyncio
import websockets

from back.autotrack_rmg import find_game_block, tracker_server
from back.web_server import start_http_server
async def main():
    print("======================================")
    print("  Ocarina of Time RMG Auto-Tracker    ")
    print("======================================\n")
    
    threading.Thread(target=start_http_server, daemon=True).start()
    webbrowser.open("http://127.0.0.1:8000")

    if find_game_block():
        print("Ready! Monitoring game memory...")
        async with websockets.serve(tracker_server, "127.0.0.1", 8080):
            await asyncio.Future() 
    else:
        print("\n[!] Could not find the game data.")
        print("[!] Make sure RMG is running and you are loaded into your save file!")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass