import json
import os

# Define the input and output filenames
# Make sure this matches the exact name of your downloaded JSON file
input_filename = "track-oot-state.RandoS9-Main.27.05.2026 11_40_08.json"
output_filename = "modified-track-oot-state.json"

# The vanilla exit bindings you provided
vanilla_exit_bindings = {
    "kokiri_deku_gateway -> deku_kokiri_gateway": "deku_kokiri_gateway -> kokiri_deku_gateway",
    "dodongo_mountain_gateway -> mountain_dodongo_gateway": "mountain_dodongo_gateway -> dodongo_mountain_gateway",
    "deku_kokiri_gateway -> kokiri_deku_gateway": "kokiri_deku_gateway -> deku_kokiri_gateway",
    "mountain_dodongo_gateway -> dodongo_mountain_gateway": "dodongo_mountain_gateway -> mountain_dodongo_gateway",
    "fountain_jabu_gateway -> jabu_fountain_gateway": "jabu_fountain_gateway -> fountain_jabu_gateway",
    "jabu_fountain_gateway -> fountain_jabu_gateway": "fountain_jabu_gateway -> jabu_fountain_gateway",
    "meadow_forest_temple_gateway -> forest_temple_meadow_gateway": "forest_temple_meadow_gateway -> meadow_forest_temple_gateway",
    "forest_temple_meadow_gateway -> meadow_forest_temple_gateway": "meadow_forest_temple_gateway -> forest_temple_meadow_gateway",
    "kakariko_well_gateway -> well_kakariko_gateway": "well_kakariko_gateway -> kakariko_well_gateway",
    "well_kakariko_gateway -> kakariko_well_gateway": "kakariko_well_gateway -> well_kakariko_gateway",
    "crater_fire_temple_gateway -> fire_temple_crater_gateway": "fire_temple_crater_gateway -> crater_fire_temple_gateway",
    "fire_temple_crater_gateway -> crater_fire_temple_gateway": "crater_fire_temple_gateway -> fire_temple_crater_gateway",
    "lake_water_temple_gateway -> water_temple_lake_gateway": "water_temple_lake_gateway -> lake_water_temple_gateway",
    "water_temple_lake_gateway -> lake_water_temple_gateway": "lake_water_temple_gateway -> water_temple_lake_gateway",
    "colossus_spirit_temple_gateway -> spirit_temple_colossus_gateway": "spirit_temple_colossus_gateway -> colossus_spirit_temple_gateway",
    "spirit_temple_colossus_gateway -> colossus_spirit_temple_gateway": "colossus_spirit_temple_gateway -> spirit_temple_colossus_gateway",
    "graveyard_shadow_temple_gateway -> shadow_temple_graveyard_gateway": "shadow_temple_graveyard_gateway -> graveyard_shadow_temple_gateway",
    "shadow_temple_graveyard_gateway -> graveyard_shadow_temple_gateway": "graveyard_shadow_temple_gateway -> shadow_temple_graveyard_gateway",
    "fortress_training_grounds_gateway -> training_grounds_fortress_gateway": "training_grounds_fortress_gateway -> fortress_training_grounds_gateway",
    "training_grounds_fortress_gateway -> fortress_training_grounds_gateway": "fortress_training_grounds_gateway -> training_grounds_fortress_gateway",
    "fountain_ice_cavern_gateway -> ice_cavern_fountain_gateway": "ice_cavern_fountain_gateway -> fountain_ice_cavern_gateway",
    "ice_cavern_fountain_gateway -> fountain_ice_cavern_gateway": "fountain_ice_cavern_gateway -> ice_cavern_fountain_gateway"
}

def modify_tracker_json():
    # Check if the file exists before trying to open it
    if not os.path.exists(input_filename):
        print(f"Error: Could not find '{input_filename}'. Please ensure it is in the same folder as this script.")
        return

    print(f"Loading '{input_filename}'...")
    
    # Read the original JSON file
    with open(input_filename, 'r', encoding='utf-8') as file:
        try:
            tracker_data = json.load(file)
        except json.JSONDecodeError:
            print("Error: The file is not a valid JSON. Please check the contents.")
            return

    # Update the exitBindings inside the 'data' object
    if "data" in tracker_data:
        tracker_data["data"]["exitBindings"] = vanilla_exit_bindings
        print("Successfully updated 'exitBindings'.")
    else:
        print("Error: Could not find the 'data' object in the JSON structure.")
        return

    # Write the modified dictionary to a new JSON file
    print(f"Saving modified data to '{output_filename}'...")
    with open(output_filename, 'w', encoding='utf-8') as file:
        # indent=4 keeps the JSON readable and formatted nicely
        json.dump(tracker_data, file, indent=4)
        
    print("Done! You can now import the modified file into your tracker.")

if __name__ == "__main__":
    modify_tracker_json()