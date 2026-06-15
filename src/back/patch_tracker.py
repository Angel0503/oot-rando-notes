import json
import os
from back import autotrack_rmg # Updated for module importing

# Define the input and output filenames
INPUT_PATH = "../../data/oot-tracker/track-oot-template.json"
OUTPUT_PATH = "../../data/generated/track-oot-generated.json"

GATEWAYS = {
    "Deku": {"inbound": "kokiri_deku_gateway -> deku_kokiri_gateway", "outbound": "deku_kokiri_gateway -> kokiri_deku_gateway"},
    "DC": {"inbound": "dodongo_mountain_gateway -> mountain_dodongo_gateway", "outbound": "mountain_dodongo_gateway -> dodongo_mountain_gateway"},
    "Jabu": {"inbound": "fountain_jabu_gateway -> jabu_fountain_gateway", "outbound": "jabu_fountain_gateway -> fountain_jabu_gateway"},
    "Forest": {"inbound": "forest_temple_meadow_gateway -> meadow_forest_temple_gateway", "outbound": "meadow_forest_temple_gateway -> forest_temple_meadow_gateway"},
    "Fire": {"inbound": "crater_fire_temple_gateway -> fire_temple_crater_gateway", "outbound": "fire_temple_crater_gateway -> crater_fire_temple_gateway"},
    "Water": {"inbound": "lake_water_temple_gateway -> water_temple_lake_gateway", "outbound": "water_temple_lake_gateway -> lake_water_temple_gateway"},
    "Spirit": {"inbound": "colossus_spirit_temple_gateway -> spirit_temple_colossus_gateway", "outbound": "spirit_temple_colossus_gateway -> colossus_spirit_temple_gateway"},
    "Shadow": {"inbound": "shadow_temple_graveyard_gateway -> graveyard_shadow_temple_gateway", "outbound": "graveyard_shadow_temple_gateway -> shadow_temple_graveyard_gateway"},
    "BotW": {"inbound": "kakariko_well_gateway -> well_kakariko_gateway", "outbound": "well_kakariko_gateway -> kakariko_well_gateway"},
    "Ice": {"inbound": "fountain_ice_cavern_gateway -> ice_cavern_fountain_gateway", "outbound": "ice_cavern_fountain_gateway -> fountain_ice_cavern_gateway"},
    "GTG": {"inbound": "training_grounds_fortress_gateway -> fortress_training_grounds_gateway", "outbound": "fortress_training_grounds_gateway -> training_grounds_fortress_gateway"}
}

GATEWAYS = {
    "Deku": {"inbound": "kokiri_deku_gateway -> deku_kokiri_gateway", "outbound": "deku_kokiri_gateway -> kokiri_deku_gateway"},
    "DC": {"inbound": "mountain_dodongo_gateway -> dodongo_mountain_gateway", "outbound": "dodongo_mountain_gateway -> mountain_dodongo_gateway"},
    "Jabu": {"inbound": "fountain_jabu_gateway -> jabu_fountain_gateway", "outbound": "jabu_fountain_gateway -> fountain_jabu_gateway"},
    "Forest": {"inbound": "meadow_forest_temple_gateway -> forest_temple_meadow_gateway", "outbound": "forest_temple_meadow_gateway -> meadow_forest_temple_gateway"},
    "Fire": {"inbound": "crater_fire_temple_gateway -> fire_temple_crater_gateway", "outbound": "fire_temple_crater_gateway -> crater_fire_temple_gateway"},
    "Water": {"inbound": "lake_water_temple_gateway -> water_temple_lake_gateway", "outbound": "water_temple_lake_gateway -> lake_water_temple_gateway"},
    "Spirit": {"inbound": "colossus_spirit_temple_gateway -> spirit_temple_colossus_gateway", "outbound": "spirit_temple_colossus_gateway -> colossus_spirit_temple_gateway"},
    "Shadow": {"inbound": "graveyard_shadow_temple_gateway -> shadow_temple_graveyard_gateway", "outbound": "shadow_temple_graveyard_gateway -> graveyard_shadow_temple_gateway"},
    "BotW": {"inbound": "kakariko_well_gateway -> well_kakariko_gateway", "outbound": "well_kakariko_gateway -> kakariko_well_gateway"},
    "Ice": {"inbound": "fountain_ice_cavern_gateway -> ice_cavern_fountain_gateway", "outbound": "ice_cavern_fountain_gateway -> fountain_ice_cavern_gateway"},
    "GTG": {"inbound": "fortress_training_grounds_gateway -> training_grounds_fortress_gateway", "outbound": "training_grounds_fortress_gateway -> fortress_training_grounds_gateway"}
}

def modify_tracker_json():
    # Safely resolve absolute paths based on where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_input = os.path.abspath(os.path.join(script_dir, INPUT_PATH))
    absolute_output = os.path.abspath(os.path.join(script_dir, OUTPUT_PATH))

    # Fetch the live dungeon data directly (launcher already hooked the memory!)
    live_data = autotrack_rmg.get_dungeon_data()
    
    if not live_data or "locations" not in live_data:
        print("[-] Error: Could not extract dungeon data from memory.")
        return
        
    # Translate the short names into tracker bindings
    dynamic_bindings = {}
    for entrance, destination in live_data["locations"].items():
        if entrance in GATEWAYS and destination in GATEWAYS:
            overworld_door = GATEWAYS[entrance]["inbound"]
            dungeon_interior = GATEWAYS[destination]["outbound"]
            
            dynamic_bindings[overworld_door] = dungeon_interior
            dynamic_bindings[dungeon_interior] = overworld_door

    # Modify the JSON file
    if not os.path.exists(absolute_input):
        print(f"[-] Error: Could not find '{absolute_input}'.")
        return

    with open(absolute_input, 'r', encoding='utf-8') as file:
        try:
            tracker_data = json.load(file)
        except json.JSONDecodeError:
            print("[-] Error: The file is not a valid JSON. Please check the contents.")
            return

    # Update the exitBindings inside the 'data' object
    if "data" in tracker_data:
        tracker_data["data"]["exitBindings"] = dynamic_bindings
        print(f"[+] Successfully generated and injected {len(dynamic_bindings)} exit bindings.")
    else:
        print("[-] Error: Could not find the 'data' object in the JSON structure.")
        return

    # Ensure output directory exists before saving
    os.makedirs(os.path.dirname(absolute_output), exist_ok=True)

    # Save the file
    with open(absolute_output, 'w', encoding='utf-8') as file:
        json.dump(tracker_data, file, indent=4)