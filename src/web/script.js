// ==========================================
// GAME DATA & UI GENERATION
// ==========================================
const gameItems = [
    "Bow", "Hookshot", "Longshot", "Hammer", "Bombs", "Bombchus", "Scale", 
    "Strength 1", "Strength 2", "Strength 3", "KokiriSword", "BiggoronSword", 
    "MirrorShield", "ZoraTunic", "GoronTunic", "IronBoots", "HoverBoots", 
    "Dins", "Farores", "Nayrus", "Magic", "Fire", "Ice", "Light", "Slingshot", 
    "Boomerang", "Lens", "Bottle", "ZoraLetter"
];
const gameSongs = [
    "ZeldasLullaby", "EponasSong", "SunsSong", "SariasSong", "SongofTime", 
    "SongofStorms", "MinuetofForest", "BoleroofFire", "SerenadeofWater", 
    "NocturneofShadow", "RequiemofSpirit", "PreludeofLight"
];
const allItemsAndSongs = [...gameItems, ...gameSongs];

// --- Mutually Exclusive Logic for Items ---
function updateItemDropdowns() {
    const allItemSelects = document.querySelectorAll('.item-select');
    const selectedValues = Array.from(allItemSelects)
        .map(s => s.value)
        .filter(val => val !== "");

    allItemSelects.forEach(select => {
        const currentVal = select.value;
        Array.from(select.options).forEach(option => {
            if (option.value === "") return;

            if (selectedValues.includes(option.value) && option.value !== currentVal) {
                option.disabled = true;
                option.style.color = "#555";
            } else {
                option.disabled = false;
                option.style.color = "#fff";
            }
        });
    });
}

// --- Logic to create a new item dropdown ---
function createItemDropdown(container, referenceNode) {
    const select = document.createElement('select');
    select.className = 'item-select';
    
    const defaultOpt = document.createElement('option');
    defaultOpt.value = "";
    defaultOpt.innerText = "---";
    select.appendChild(defaultOpt);

    allItemsAndSongs.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item;
        opt.innerText = item;
        select.appendChild(opt);
    });

    select.addEventListener('change', function() {
        updateItemDropdowns();
        
        const selectsInRow = container.querySelectorAll('.item-select');
        const isLast = (this === selectsInRow[selectsInRow.length - 1]);
        const isResolved = container.parentElement.querySelector('.path-checkbox').checked;
        
        if (this.value !== "" && isLast && !isResolved) {
            createItemDropdown(container, referenceNode);
        }
    });

    container.insertBefore(select, referenceNode);
    updateItemDropdowns(); 
}

// --- Generate Path Elements ---
const pathContainer = document.getElementById('path-container');
for (let i = 0; i < 8; i++) {
    const group = document.createElement('div');
    group.className = 'path-group';

    const row = document.createElement('div');
    row.className = 'path-row';
    row.innerHTML = `
        <input type="checkbox" class="path-checkbox" title="Mark as resolved">
        <textarea placeholder="Source"></textarea>
        <span class="arrow">→</span>
        <textarea placeholder="Destination"></textarea>
    `;

    const itemRow = document.createElement('div');
    itemRow.className = 'item-row';
    
    const delBtn = document.createElement('button');
    delBtn.className = 'delete-item-btn';
    delBtn.innerHTML = '✖';
    delBtn.title = 'Remove last item';

    delBtn.addEventListener('click', function() {
        const selects = itemRow.querySelectorAll('.item-select');
        if (selects.length > 1) {
            selects[selects.length - 1].remove();
            updateItemDropdowns();
        } 
        else if (selects.length === 1) {
            selects[0].value = "";
            updateItemDropdowns();
        }
    });

    itemRow.appendChild(delBtn);
    createItemDropdown(itemRow, delBtn);

    group.appendChild(row);
    group.appendChild(itemRow);
    pathContainer.appendChild(group);

    const checkbox = row.querySelector('.path-checkbox');
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            group.classList.add('resolved');
            const selects = itemRow.querySelectorAll('.item-select');
            const lastSelect = selects[selects.length - 1];
            if (lastSelect && lastSelect.value === "") {
                lastSelect.remove();
            }
        } else {
            group.classList.remove('resolved');
            const selects = itemRow.querySelectorAll('.item-select');
            if (selects.length === 0 || selects[selects.length - 1].value !== "") {
                createItemDropdown(itemRow, delBtn);
            }
        }
    });
}

// --- Generate Note Elements ---
const notesContainer = document.getElementById('notes-container');
for (let i = 0; i < 7; i++) {
    const row = document.createElement('div');
    row.className = 'row note-row';
    row.innerHTML = `
        <textarea placeholder="Hint / Item"></textarea>
        <span class="arrow">→</span>
        <textarea placeholder="Location"></textarea>
    `;
    notesContainer.appendChild(row);
}

// --- Generate Dungeon Elements ---
const dungeons = ['Deku', 'DC', 'Jabu', 'Forest', 'Fire', 'Water', 'Shadow', 'Spirit', 'BotW', 'Ice', 'GTG'];
const dungeonContainer = document.getElementById('dungeon-container');

dungeons.forEach(dungeon => {
    const row = document.createElement('div');
    row.className = 'row dungeon-row';
    
    const labelHtml = `<span class="dungeon-label">${dungeon}</span> <span class="arrow">→</span>`;
    
    const select = document.createElement('select');
    select.className = 'dungeon-select';
    select.id = `entrance-${dungeon}`;
    
    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.innerText = "---";
    select.appendChild(defaultOption);

    dungeons.forEach(d => {
        const option = document.createElement('option');
        option.value = d;
        option.innerText = d;
        select.appendChild(option);
    });

    row.innerHTML = labelHtml;
    row.appendChild(select);
    dungeonContainer.appendChild(row);
});

// --- Mutually Exclusive Dropdown Logic for Dungeons ---
const dungeonSelects = document.querySelectorAll('.dungeon-select');
function updateDungeonDropdowns() {
    const selectedValues = Array.from(dungeonSelects)
        .map(s => s.value)
        .filter(val => val !== "");

    dungeonSelects.forEach(select => {
        const currentSelectValue = select.value;
        Array.from(select.options).forEach(option => {
            if (option.value === "") return;

            if (selectedValues.includes(option.value) && option.value !== currentSelectValue) {
                option.disabled = true;
                option.style.color = "#555";
            } else {
                option.disabled = false;
                option.style.color = "#fff";
            }
        });
    });
}

dungeonSelects.forEach(select => {
    select.addEventListener('change', updateDungeonDropdowns);
});

// --- Prevent Accidental Refresh / Close ---
window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
});

// ==========================================
// AUTO-TRACKER WEBSOCKET LOGIC
// ==========================================

const trackerSocket = new WebSocket('ws://127.0.0.1:8080');

// Grab the UI elements
const statusContainer = document.getElementById('connection-status');
const statusText = statusContainer.querySelector('.status-text');

trackerSocket.onopen = function(event) {
    console.log("🟢 Connected to RMG Auto-Tracker Server!");
    statusContainer.className = 'status-connected';
    statusText.innerText = 'Auto-Tracker Connected';
};

trackerSocket.onmessage = function(event) {
    const payload = JSON.parse(event.data);
    
    if (payload.type === "entrances") {
        for (const [entranceName, destinationName] of Object.entries(payload.locations)) {
            
            let finalValue = destinationName;
            if (destinationName === "???") finalValue = ""; // Resets to '---'

            const dropdown = document.getElementById(`entrance-${entranceName}`);
            
            if (dropdown && dropdown.value !== finalValue) {
                dropdown.value = finalValue;
                dropdown.dispatchEvent(new Event('change'));
            }
        }
    }
};

trackerSocket.onclose = function(event) {
    console.log("🔴 Disconnected from Auto-Tracker Server.");
    statusContainer.className = 'status-disconnected';
    statusText.innerText = 'Disconnected';
};

trackerSocket.onerror = function(error) {
    console.error("WebSocket Error:", error);
    statusContainer.className = 'status-disconnected';
    statusText.innerText = 'Disconnected';
};