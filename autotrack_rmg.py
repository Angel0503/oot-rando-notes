import pymem
import array
import json
import asyncio
import websockets

ENTRANCE_ORDER = [
    "Deku", "DC", "Jabu", "Forest", "Fire", "Water", 
    "Shadow", "Spirit", "BotW", "Ice", "GTG"
]

# All possible strings the Randomizer could ever print
KNOWN_DESTINATIONS = {
    "Deku", "DC", "Jabu", "Forest", "Fire", "Water", 
    "Shadow", "Spirit", "BotW", "Ice", "GTG"
}

# We will search for any of these to use as our anchor point
ANCHORS = [
    b"Water   \x00", b"Fire    \x00", b"Forest  \x00", 
    b"Shadow  \x00", b"Spirit  \x00", b"Ice     \x00"
]

def unswap_memory(data):
    """Flips RMG's scrambled memory back into normal N64 memory"""
    if len(data) % 4 != 0: return data
    arr = array.array('I', data)
    arr.byteswap()
    return arr.tobytes()

GAME_BASE_ADDRESS = 0
GAME_REGION_SIZE = 0
pm = None

def find_game_block():
    global GAME_BASE_ADDRESS, GAME_REGION_SIZE, pm
    print("Scanning for RMG Memory Block...")
    try:
        pm = pymem.Pymem("RMG.exe")
    except Exception:
        return False

    address = 0
    while address < 0x7FFFFFFFFFFF:
        try:
            mbi = pymem.memory.virtual_query(pm.process_handle, address)
            if mbi.State == 0x1000 and mbi.RegionSize >= 0x400000:
                raw_data = pm.read_bytes(mbi.BaseAddress, mbi.RegionSize)
                clean_mem = unswap_memory(raw_data)
                
                # Check if ANY of our anchors exist in this block
                for anchor in ANCHORS:
                    if anchor in clean_mem:
                        GAME_BASE_ADDRESS = mbi.BaseAddress
                        GAME_REGION_SIZE = mbi.RegionSize
                        print(f"--- Locked onto Game RAM at {hex(GAME_BASE_ADDRESS)} ---")
                        return True
        except Exception:
            pass
        address += mbi.RegionSize
    return False

def get_dungeon_data():
    if GAME_BASE_ADDRESS == 0: return None

    try:
        raw_data = pm.read_bytes(GAME_BASE_ADDRESS, GAME_REGION_SIZE)
        clean_memory = unswap_memory(raw_data)

        # 1. Find an anchor
        anchor_offset = -1
        for anchor in ANCHORS:
            offset = clean_memory.find(anchor)
            if offset != -1:
                anchor_offset = offset
                break

        if anchor_offset == -1: return None

        # 2. THE GRID SNAP ALGORITHM
        best_base = 0
        max_score = -1

        # Test all 12 possible starting positions
        for i in range(12):
            test_base = anchor_offset - (i * 9)
            score = 0
            
            # Read the 12 items at this alignment and score them
            for j in range(12):
                start = test_base + (j * 9)
                chunk = clean_memory[start:start+9]
                clean_text = chunk.split(b'\x00', 1)[0].decode('ascii', errors='ignore').strip()
                
                if clean_text in KNOWN_DESTINATIONS:
                    score += 1
            
            # If this alignment looks the most like a Zelda list, lock it in!
            if score > max_score:
                max_score = score
                best_base = test_base

        # 3. Read and extract the perfected data
        payload = {"type": "entrances", "locations": {}}

        for i, dungeon in enumerate(ENTRANCE_ORDER):
            start = best_base + (i * 9)
            raw_text = clean_memory[start:start+9]
            clean_text = raw_text.split(b'\x00', 1)[0].decode('ascii', errors='ignore').strip()
            
            if not clean_text: 
                clean_text = "???"
                
            payload["locations"][dungeon] = clean_text
            
        return payload
    except Exception:
        return None

async def tracker_server(websocket):
    print("\n[+] HTML TRACKER CONNECTED!")
    last_sent_data = ""
    
    while True:
        try:
            data = get_dungeon_data()
            
            if data:
                json_string = json.dumps(data)
                
                if json_string != last_sent_data:
                    await websocket.send(json_string)
                    last_sent_data = json_string
                    
                    print("\n[+] Broadcasted New Dungeon Layout to HTML:")
                    for loc, dest in data["locations"].items():
                        print(f"    {loc.ljust(8)} -> {dest}")
                        
            await asyncio.sleep(1) 
            
        except websockets.exceptions.ConnectionClosed:
            print("\n[-] HTML Tracker Disconnected.")
            break

async def main():
    print("Starting Auto-Tracker Bridge Server...")
    if find_game_block():
        print("Ready! Waiting for your HTML file to connect on port 8080...")
        async with websockets.serve(tracker_server, "127.0.0.1", 8080):
            await asyncio.Future() 
    else:
        print("Could not find the game data. Make sure you are in-game!")

if __name__ == "__main__":
    asyncio.run(main())