import pymem
import array

def unswap_memory(data):
    if len(data) % 4 != 0: return data
    arr = array.array('I', data)
    arr.byteswap()
    return arr.tobytes()

def find_true_rupee_address():
    print("=========================================")
    print("       THE RUPEE HUNTER SANDBOX          ")
    print("=========================================\n")
    
    try:
        pm = pymem.Pymem("RMG.exe")
    except Exception:
        print("[-] RMG.exe not found. Is it running?")
        return

    # STEP 1: INITIAL SCAN
    start_rupees = int(input("1. How many Rupees do you have RIGHT NOW? "))
    target_bytes = start_rupees.to_bytes(2, byteorder='big')

    print("\n[*] Sweeping entire RMG memory for that exact number...")
    address = 0
    possible_locations = []

    while address < 0x7FFFFFFFFFFF:
        try:
            mbi = pymem.memory.virtual_query(pm.process_handle, address)
            # Cast a wider net: check all memory blocks 1MB or larger
            if mbi.State == 0x1000 and mbi.RegionSize >= 0x100000:
                raw = pm.read_bytes(mbi.BaseAddress, mbi.RegionSize)
                clean = unswap_memory(raw)

                offset = clean.find(target_bytes)
                while offset != -1:
                    possible_locations.append((mbi.BaseAddress, mbi.RegionSize, offset))
                    offset = clean.find(target_bytes, offset + 1)
        except Exception:
            pass
        address += mbi.RegionSize

    total_locations = len(possible_locations)
    print(f"[+] Found {total_locations} places in memory currently holding the number '{start_rupees}'.")
    
    if total_locations == 0:
        print("[-] Could not find your rupees. Try restarting the script.")
        return

    # STEP 2: THE CHANGE
    input("\n2. Go into the game and spend or collect some Rupees! \n   Press ENTER here ONLY when your count has changed...")
    
   # STEP 3: NARROWING IT DOWN (OPTIMIZED)
    new_rupees = int(input("\n3. What is your NEW Rupee count? "))
    new_target_bytes = new_rupees.to_bytes(2, byteorder='big')

    print("\n[*] Eliminating false positives (Lightning Fast Mode)...")
    final_locations = []

    # 3a. Group our matches by their memory block
    grouped_blocks = {}
    for base, size, offset in possible_locations:
        if base not in grouped_blocks:
            grouped_blocks[base] = {'size': size, 'offsets': []}
        grouped_blocks[base]['offsets'].append(offset)

    # 3b. Read each massive block exactly ONCE, then check all offsets inside it
    for base, data in grouped_blocks.items():
        try:
            # We download the block once...
            raw = pm.read_bytes(base, data['size'])
            clean = unswap_memory(raw)
            
            # ...and instantly check all matching offsets within it!
            for offset in data['offsets']:
                if clean[offset : offset+2] == new_target_bytes:
                    final_locations.append((base, offset, clean))
        except Exception:
            continue

    print() # Pushes the terminal to the next line so we don't overwrite our progress bar

    # STEP 4: THE REVEAL
    if len(final_locations) == 1:
        base, offset, clean = final_locations[0]
        print(f"\n[+] BINGO! The true Live Rupee address is at Block: {hex(base)} | Offset: {hex(offset)}")
        
        # Look 52 bytes backwards (0x34) to see what the header actually is!
        header_offset = offset - 0x34
        if header_offset >= 0:
            header_bytes = clean[header_offset : header_offset+6]
            print(f"\n[*] Looking 52 bytes backwards to find the Save Context Header...")
            print(f"    -> Raw Hex: {header_bytes.hex(' ')}")
            try:
                print(f"    -> Decoded Text: '{header_bytes.decode('ascii', errors='ignore')}'")
            except Exception:
                pass
    else:
        print(f"\n[-] Narrowed it down to {len(final_locations)} locations. We might need a 3rd scan.")

if __name__ == "__main__":
    find_true_rupee_address()