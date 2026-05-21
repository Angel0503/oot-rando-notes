# OoT Rando Notes Tracker

A comprehensive web-based tracking tool designed specifically for **The Legend of Zelda: Ocarina of Time Randomizer** (OoT Rando). This application helps players manage hints, track paths, organize notes, and monitor dungeon entrances during randomizer gameplay.

## Overview

This tracker is built to assist players during Ocarina of Time randomizer runs by providing a centralized interface to:
- Record barren (empty) locations
- Track paths from source to destination with items obtained
- Manage extensive notes and hints
- Dynamically map dungeon entrances in entrance randomizer mode
- Automatically sync dungeon data from the RMG (Randomizer Memory Game) auto-tracker

## Features

### 1. **Barren Locations Tracking**
- Two text areas to record areas confirmed as barren (containing no important items)
- Helps identify dead ends and optimize exploration strategy

### 2. **Path Tracking System**
- 8 individual path tracking entries with:
  - **Source Field**: Starting location of the path
  - **Destination Field**: End location of the path
  - **Item Dropdowns**: Dynamically add items obtained along the path
  - **Resolution Checkbox**: Mark a path as resolved once completed
- **Smart Dropdown System**:
  - All available items and songs from the game appear in dropdowns
  - Each item can only be selected once (prevents duplicate entries)
  - New dropdown rows automatically generate when you select an item (except for completed paths)
  - Delete button allows removal of the last item in each path
- Items automatically become unavailable in other dropdowns once selected

### 3. **Notes Section**
- 7 dedicated note entries with:
  - **Hint/Item Field**: Record the hint or item reference
  - **Location Field**: Note where the item/hint relates to
- Useful for tracking complex hint clues and their potential locations

### 4. **Dungeon Entrance Management**
- Dropdown menus for all 11 dungeon entrances (excluding Ganon's Castle):
  - Deku Tree (Deku)
  - Dodongo's Cavern (DC)
  - Jabu Jabu's Belly (Jabu)
  - Forest Temple (Forest)
  - Fire Temple (Fire)
  - Water Temple (Water)
  - Shadow Temple (Shadow)
  - Spirit Temple (Spirit)
  - Bottom of the Well (BotW)
  - Ice Cavern (Ice)
  - Gerudo Training Grounds (GTG)
- Each entrance can map to any other dungeon location
- Mutually exclusive selection (each destination can only be assigned once)

### 5. **Auto-Tracker Integration (Optional)**
- **WebSocket Connection**: Automatically connects to the RMG auto-tracker server on `ws://127.0.0.1:8080`
- **Real-time Dungeon Sync**: When the auto-tracker is running, dungeon entrances are automatically updated in real-time as the game data changes
- **Graceful Fallback**: If the auto-tracker is not available, the tracker still functions normally with manual entrance entry
- Status indicators in browser console show connection status

## Setup & Installation

### Prerequisites
- A modern web browser (Chrome, Firefox, Edge, Safari)
- For auto-tracker integration: Python 3.7+, RMG (Randomizer Memory Game) installed

### Quick Start (Manual Mode)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd oot-rando-notes
   ```

2. **Open the application**:
   - Navigate to `src/web/index.html`
   - Open it in your web browser
   - The tracker interface is now ready to use

3. **Start tracking**:
   - Use the barren areas section to note empty locations
   - Create paths by entering source → destination and selecting items
   - Add notes about hints and item locations
   - Fill in dungeon entrances as you discover them

### Setup with Auto-Tracker (Optional)

To automatically sync dungeon entrances from the RMG emulator:

1. **Install Python dependencies**:
   ```bash
   pip install pymem websockets
   ```

2. **Start the RMG emulator**:
   - Launch RMG.exe and start your randomizer game
   - Get to a point where you can access the game (in-game state)

3. **Run the auto-tracker server**:
   ```bash
   python src/back/autotrack_rmg.py
   ```

4. **Open the web tracker**:
   - Open `src/web/index.html` in your browser
   - The application will automatically connect to the WebSocket server
   - Watch for the green connection message in the browser console: "🟢 Connected to RMG Auto-Tracker Server!"
   - Dungeon entrances will now update automatically as you explore in-game

5. **Stop the server**:
   - Press `Ctrl+C` in the terminal running the Python script

**Note**: The auto-tracker server requires the game to be running and accessible in memory. It scans the RMG process to extract dungeon entrance data.

## How to Use

### Using Auto-Tracker Integration
1. Ensure the Python server is running (`autotrack_rmg.py`)
2. Start the tracker in your browser
3. Launch or continue your OoT Rando game
4. Observe the dungeon dropdown fields populate automatically as the auto-tracker reads game memory

## Browser Storage

All data entered in the tracker is stored in your browser's local storage. This means:
- ✅ Data persists across browser sessions
- ✅ Data remains private (stored locally, not sent anywhere)
- ✅ No account or login required
- ⚠️ Clearing browser cache/cookies will erase all data
- ⚠️ Data is device/browser specific (not synced across devices)

## Features & Behavior

### Item Selection Logic
- **Auto-Complete**: When you select an item, a new dropdown automatically appears (unless the path is marked as resolved)
- **Mutual Exclusion**: Once an item is selected anywhere in the tracker, it becomes unavailable for selection in other dropdowns
- **Smart Disabling**: Selected items appear grayed out in other dropdowns
- **Deletion**: Use the ✖ button to remove the last item in a path, or clear the only item

### Dungeon Selection Logic
- **Mutual Exclusion**: Each dungeon destination can only be mapped to one source
- **Prevention of Duplicates**: When a dungeon is selected in one dropdown, it appears grayed out (disabled) in other dropdowns
- **Reset Option**: Select "---" to clear a dungeon mapping

### Path Resolution
- When you check a path's checkbox:
  - The path group fades out (opacity ~40%)
  - Empty item dropdowns are automatically removed
  - The path is marked as "resolved"
- Uncheck to make it active again and re-edit

### Data Persistence
- No save button needed—everything auto-saves to local storage
- A warning appears if you try to leave the page with unsaved changes
- Close the tab/browser and your data will be restored when you return

## Troubleshooting

### Auto-Tracker Not Connecting
- **Error**: "🔴 Disconnected from Auto-Tracker Server" in console
- **Solution**:
  1. Ensure `autotrack_rmg.py` is running
  2. Verify RMG.exe is running with an active game session
  3. Check that port 8080 is not blocked by your firewall
  4. Restart the Python server and refresh the browser page
  5. The tracker will continue to work without auto-tracker (manual mode)

### Data Not Persisting
- **Issue**: Data disappears after closing the browser
- **Solution**: 
  1. Check that cookies/storage are enabled in your browser settings
  2. Your browser's privacy mode may prevent storage—use normal mode
  3. Clear some browser cache if storage quota is exceeded

### Items Not Appearing in Dropdowns
- **Issue**: "Bow", "Hookshot", etc. don't show in selections
- **Solution**: This should not happen. Try:
  1. Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)
  2. Clear browser cache for the site
  3. Check browser console for JavaScript errors (F12)

### Python Script Errors
- **Error**: "Could not find the game data"
- **Solution**: 
  1. Ensure RMG.exe is running
  2. Make sure you are in-game (not at menu screen)
  3. Ensure the game has loaded far enough for memory scanning to work

## Technologies Used

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Backend** (optional): Python 3.7+, asyncio, websockets, pymem
- **Communication**: WebSocket protocol for real-time auto-tracker updates

## Browser Compatibility

- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari (11+)

## Future Development

The following features are planned for future versions:

### Auto-completion of Notes
Implement intelligent suggestion system to automatically fill in notes based on patterns detected in gameplay. This will help players recognize item hints more quickly and cross-reference locations efficiently.

### Visual Connection Status Indicator
Add a persistent, visible indicator on the page showing real-time connection status to the auto-tracker server. This will include:
- A status badge displaying "Connected" or "Disconnected"
- Color-coded visual feedback (green for connected, red for disconnected)
- Optional connection status notifications or alerts

### Complete Map Visualization
Develop an interactive dungeon entrance map that displays the complete dungeon layout in a visual format. This will include:
- Visual representation of all 11 dungeons
- Graphical display of entrance mappings
- Better overview of the entire entrance randomizer configuration
- Potential visual conflict detection

### Item Requirement Tracking
Create a system to track which items are required for specific dungeon checks and locations. This feature will:
- Identify which items are needed to access particular locations
- Display item requirements for each dungeon
- Help players see which items they still need to find for unexplored areas
- Provide a checklist of required items per location

## Contributing

Feel free to fork this project and submit pull requests for improvements and bug fixes.

## License

This project is provided as-is for personal use with The Legend of Zelda: Ocarina of Time Randomizer community.

## Support & Feedback

For issues, suggestions, or feedback regarding this tracker, please open an issue in the repository or reach out to the development team.

---

**Happy randomizing!** 🎮
