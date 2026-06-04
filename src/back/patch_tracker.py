import json
import os
import autotrack_rmg

INPUT_PATH = "../../data/oot-tracker/track-oot-template.json"
OUTPUT_PATH = "../../data/oot-tracker/track-oot-generated.json"

GATEWAYS = {
    "Deku": {
        "inbound": "kokiri_deku_gateway -> deku_kokiri_gateway",
        "outbound": "deku_kokiri_gateway -> kokiri_deku_gateway"
    },
    "DC": {
        "inbound": "mountain_dodongo_gateway -> dodongo_mountain_gateway",
        "outbound": "dodongo_mountain_gateway -> mountain_dodongo_gateway"
    },
    "Jabu": {
        "inbound": "fountain_jabu_gateway -> jabu_fountain_gateway",
        "outbound": "jabu_fountain_gateway -> fountain_jabu_gateway"
    },
    "Forest": {
        "inbound": "meadow_forest_temple_gateway -> forest_temple_meadow_gateway",
        "outbound": "forest_temple_meadow_gateway -> meadow_forest_temple_gateway"
    },
    "Fire": {
        "inbound": "crater_fire_temple_gateway -> fire_temple_crater_gateway",
        "outbound": "fire_temple_crater_gateway -> crater_fire_temple_gateway"
    },
    "Water": {
        "inbound": "lake_water_temple_gateway -> water_temple_lake_gateway",
        "outbound": "water_temple_lake_gateway -> lake_water_temple_gateway"
    },
    "Spirit": {
        "inbound": "colossus_spirit_temple_gateway -> spirit_temple_colossus_gateway",
        "outbound": "spirit_temple_colossus_gateway -> colossus_spirit_temple_gateway"
    },
    "Shadow": {
        "inbound": "graveyard_shadow_temple_gateway -> shadow_temple_graveyard_gateway",
        "outbound": "shadow_temple_graveyard_gateway -> graveyard_shadow_temple_gateway"
    },
    "BotW": {
        "inbound": "kakariko_well_gateway -> well_kakariko_gateway",
        "outbound": "well_kakariko_gateway -> kakariko_well_gateway"
    },
    "Ice": {
        "inbound": "fountain_ice_cavern_gateway -> ice_cavern_fountain_gateway",
        "outbound": "ice_cavern_fountain_gateway -> fountain_ice_cavern_gateway"
    },
    "GTG": {
        "inbound": "fortress_training_grounds_gateway -> training_grounds_fortress_gateway",
        "outbound": "training_grounds_fortress_gateway -> fortress_training_grounds_gateway"
    }
}

def modify_tracker_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_input = os.path.abspath(os.path.join(script_dir, INPUT_PATH))
    absolute_output = os.path.abspath(os.path.join(script_dir, OUTPUT_PATH))

    print("Connecting to RMG...")
    if not autotrack_rmg.find_game_block():
        print("Error: Could not find the game data in RMG. Make sure RMG is running and you are loaded into a save.")
        return
    
    live_data = autotrack_rmg.get_dungeon_data()
    if not live_data or "locations" not in live_data:
        print("Error: Could not extract dungeon data from memory.")
        return
        
    print("\nLive Dungeon Mapping Found:")
    for loc, dest in live_data["locations"].items():
        print(f"  {loc} -> {dest}")

    dynamic_bindings = {}
    for entrance, destination in live_data["locations"].items():
        if entrance in GATEWAYS and destination in GATEWAYS:
            overworld_door = GATEWAYS[entrance]["inbound"]
            dungeon_interior = GATEWAYS[destination]["outbound"]
            dynamic_bindings[overworld_door] = dungeon_interior
            dynamic_bindings[dungeon_interior] = overworld_door

    if not os.path.exists(absolute_input):
        print(f"\nError: Could not find '{absolute_input}'.")
        return

    print(f"\nLoading '{absolute_input}'...")
    with open(absolute_input, 'r', encoding='utf-8') as file:
        try:
            tracker_data = json.load(file)
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON. Please check the contents.")
            return

    if "data" in tracker_data:
        tracker_data["data"]["exitBindings"] = dynamic_bindings
        print(f"Successfully generated and injected {len(dynamic_bindings)} exit bindings.")
    else:
        print("Error: Could not find the 'data' object in the JSON structure.")
        return

    os.makedirs(os.path.dirname(absolute_output), exist_ok=True)

    print(f"Saving modified data to '{absolute_output}'...")
    with open(absolute_output, 'w', encoding='utf-8') as file:
        json.dump(tracker_data, file, indent=4)
        
    print("Done! You can now import the generated file into your tracker.")

if __name__ == "__main__":
    modify_tracker_json()