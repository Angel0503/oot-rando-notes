// ==========================================
// GAME DATA
// ==========================================
const gameItems = [
    "Bow", "Hookshot", "Longshot", "Hammer", "Bombs", "Bombchus", "Scale",
    "Strength 1", "Strength 2", "Strength 3", "KokiriSword", "BiggoronSword",
    "MirrorShield", "ZoraTunic", "GoronTunic", "IronBoots", "HoverBoots",
    "Dins", "Farores", "Nayrus", "Magic", "Fire", "Ice", "Light", "Slingshot",
    "Boomerang", "Lens", "Bottle", "ZoraLetter", "Rien", "BK", "Key"
];
const gameSongs = [
    "ZL", "Epona", "Saria", "Sun", "Time", "Storms",
    "Minuet", "Bolero", "Serenade", "Nocturne", "Requiem", "Prelude"
];
const allItemsAndSongs = [...gameItems, ...gameSongs];

// Path hints: source = dungeon or place, destination = boss or Evil
const PATH_SOURCES = [
    // dungeons
    "Deku", "DC", "Jabu", "Forest", "Fire", "Water", "Shadow", "Spirit", "BotW", "Ice", "GTG",
    // places
    "KF", "LW", "SFM", "HF", "LLR",
    "Market", "TOT", "Hyrule Castle", "Ganon's Castle", "KAK", "Graveyard",
    "DMT", "GC", "DMC", "ZR", "ZD", "ZF",
    "Lake", "GV", "GF", "Wasteland", "Colossus"
];
const PATH_DESTINATIONS = [
    "Gohma", "Dodongo", "Barinade", "PG",
    "Volvagia", "Morpha", "Bongo", "Twin", "Evil"
];

// Hint layout (edit these lists to change the number of fields)
const ALWAYS_HINTS = ["Biggoron", "Frogs 2", "Skull Mask", "AD", "Kak song"];
const SONG_HINTS = ["AD", "Kak song"]; // these rows get a song-only dropdown
const SKULL_HINTS = ["30 Skulls", "40 Skulls", "50 Skulls"];
const PATH_COUNT = 5;
const IMPORTANT_COUNT = 2;
const SOMETIMES_COUNT = 4;
const DUAL_COUNT = 2;
const NOTES_COUNT = 2;

// ==========================================
// SMALL UI HELPERS
// ==========================================
function makeTextarea(placeholder) {
    const t = document.createElement('textarea');
    t.className = 'hint-input';
    t.rows = 1;
    t.setAttribute('wrap', 'off'); // single line: text never wraps, so it can't scroll/shift vertically
    t.placeholder = placeholder;
    return t;
}

// Free text input with autocomplete on items/songs (you can still type anything)
function makeItemInput(placeholder = "Item") {
    const i = document.createElement('input');
    i.type = 'text';
    i.className = 'hint-input';
    i.setAttribute('list', 'item-list');
    i.setAttribute('autocomplete', 'off');
    i.placeholder = placeholder;
    return i;
}

function makeArrow() {
    const a = document.createElement('span');
    a.className = 'arrow';
    a.textContent = '→';
    return a;
}

// "LABEL  [ field ]"
function makeLabelledRow(label, field) {
    const row = document.createElement('div');
    row.className = 'hint-row';
    const l = document.createElement('span');
    l.className = 'hint-label';
    l.textContent = label;
    row.appendChild(l);
    row.appendChild(field);

    // Toggle: "this check is not worth doing" (greys the row out, keeps what you typed)
    const skipBtn = document.createElement('button');
    skipBtn.className = 'skip-btn';
    skipBtn.textContent = '✖';
    skipBtn.title = 'Mark as not worth doing';
    skipBtn.addEventListener('click', () => {
        const skipped = row.classList.toggle('skipped');
        field.disabled = skipped;
        skipBtn.textContent = skipped ? '↺' : '✖';
        skipBtn.title = skipped ? 'Undo' : 'Mark as not worth doing';
    });
    row.appendChild(skipBtn);
    return row;
}

// "[ Location ] → [ Item ]"
function makePairRow(locPlaceholder = "Location", itemPlaceholder = "Item") {
    const row = document.createElement('div');
    row.className = 'pair-row';
    row.appendChild(makeTextarea(locPlaceholder));
    row.appendChild(makeArrow());
    row.appendChild(makeItemInput(itemPlaceholder));
    return row;
}

// Closed list (dropdown) with a blank first option
function makeSelect(options, placeholder) {
    const s = document.createElement('select');
    s.className = 'hint-input';
    const first = document.createElement('option');
    first.value = "";
    first.textContent = placeholder;
    s.appendChild(first);
    options.forEach(o => {
        const opt = document.createElement('option');
        opt.value = o;
        opt.textContent = o;
        s.appendChild(opt);
    });
    return s;
}

// Text input with autocomplete on dungeons / places (you can still type anything)
function makeSourceInput() {
    const i = document.createElement('input');
    i.type = 'text';
    i.className = 'hint-input';
    i.setAttribute('list', 'source-list');
    i.setAttribute('autocomplete', 'off');
    i.placeholder = "Source";
    return i;
}

// "[ Location ] → [ 1-9 ]"  (important checks: number of items)
function makeCountRow(locPlaceholder = "Location") {
    const row = document.createElement('div');
    row.className = 'pair-row pair-count';
    row.appendChild(makeTextarea(locPlaceholder));
    row.appendChild(makeArrow());
    row.appendChild(makeSelect(["1", "2", "3", "4", "5", "6", "7", "8", "9"], "#"));
    return row;
}

const sourceList = document.createElement('datalist');
sourceList.id = 'source-list';
PATH_SOURCES.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p;
    sourceList.appendChild(opt);
});
document.body.appendChild(sourceList);

// No line breaks in the fields (Enter would scroll the text inside a 1-line box)
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.matches('textarea')) e.preventDefault();
});

// Highlight filled fields
document.addEventListener('input', (e) => {
    if (e.target.matches('.hint-input')) {
        e.target.classList.toggle('has-value', e.target.value.trim() !== '');
    }
});

// Autocomplete list
const itemList = document.getElementById('item-list');
allItemsAndSongs.forEach(item => {
    const opt = document.createElement('option');
    opt.value = item;
    itemList.appendChild(opt);
});

// ==========================================
// PATH (goal hints) - dropdowns are mutually exclusive
// ==========================================
function updateItemDropdowns() {
    const allItemSelects = document.querySelectorAll('.path-group .item-select');
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

    select.addEventListener('change', function () {
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

const pathContainer = document.getElementById('path-container');
for (let i = 0; i < PATH_COUNT; i++) {
    const group = document.createElement('div');
    group.className = 'path-group';

    const row = document.createElement('div');
    row.className = 'path-row';
    row.innerHTML = `
        <div class="path-controls">
            <input type="checkbox" class="path-checkbox" title="Mark as resolved">
            <div class="drag-handle" title="Drag to reorder">☰</div>
        </div>
    `;
    row.appendChild(makeSourceInput());
    row.appendChild(makeArrow());
    row.appendChild(makeSelect(PATH_DESTINATIONS, "Boss / Evil"));

    const itemRow = document.createElement('div');
    itemRow.className = 'item-row';

    const delBtn = document.createElement('button');
    delBtn.className = 'delete-item-btn';
    delBtn.innerHTML = '✖';
    delBtn.title = 'Remove last item';

    delBtn.addEventListener('click', function () {
        const selects = itemRow.querySelectorAll('.item-select');
        if (selects.length > 1) {
            selects[selects.length - 1].remove();
            updateItemDropdowns();
        } else if (selects.length === 1) {
            selects[0].value = "";
            updateItemDropdowns();
        }
    });

    itemRow.appendChild(delBtn);
    createItemDropdown(itemRow, delBtn);

    group.appendChild(row);
    group.appendChild(itemRow);
    pathContainer.appendChild(group);

    setupDragAndDrop(group, row.querySelector('.drag-handle'));

    const checkbox = row.querySelector('.path-checkbox');
    checkbox.addEventListener('change', function () {
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

// ==========================================
// ALWAYS HINTS (fixed labels: Biggoron, Frogs 2, Skull Mask, OoT, Burning Kak, Big Poe)
// ==========================================
const alwaysContainer = document.getElementById('always-container');
ALWAYS_HINTS.forEach(name => {
    const field = SONG_HINTS.includes(name) ? makeSelect(gameSongs, "Song") : makeItemInput("Item");
    alwaysContainer.appendChild(makeLabelledRow(name, field));
});

// ==========================================
// LIGHT ARROWS (Dampé's Diary) + SKULL HINTS
// ==========================================
const specialContainer = document.getElementById('special-container');
specialContainer.appendChild(makeLabelledRow("Light Arr.", makeTextarea("Location")));
SKULL_HINTS.forEach(name => {
    specialContainer.appendChild(makeLabelledRow(name, makeItemInput("Item")));
});

// ==========================================
// IMPORTANT CHECKS / SOMETIMES / DUAL / NOTES
// ==========================================
const importantContainer = document.getElementById('important-container');
for (let i = 0; i < IMPORTANT_COUNT; i++) {
    importantContainer.appendChild(makeCountRow("Location"));
}

const sometimesContainer = document.getElementById('sometimes-container');
for (let i = 0; i < SOMETIMES_COUNT; i++) {
    sometimesContainer.appendChild(makePairRow("Location", "Item"));
}

// A dual hint = ONE location with TWO checks
const dualContainer = document.getElementById('dual-container');
for (let i = 0; i < DUAL_COUNT; i++) {
    const group = document.createElement('div');
    group.className = 'dual-group';
    const loc = makeTextarea("Location");
    loc.classList.add('dual-location');
    loc.setAttribute('wrap', 'soft'); // the tall location box may wrap on 2 lines
    const items = document.createElement('div');
    items.className = 'dual-items';
    items.appendChild(makeItemInput("Check 1"));
    items.appendChild(makeItemInput("Check 2"));
    group.appendChild(loc);
    group.appendChild(makeArrow());
    group.appendChild(items);
    dualContainer.appendChild(group);
}

const notesContainer = document.getElementById('notes-container');
for (let i = 0; i < NOTES_COUNT; i++) {
    const row = document.createElement('div');
    row.className = 'pair-row';
    row.appendChild(makeTextarea("Hint / Item"));
    row.appendChild(makeArrow());
    row.appendChild(makeTextarea("Location"));
    notesContainer.appendChild(row);
}

// --- Prevent Accidental Refresh / Close ---
window.addEventListener('beforeunload', function (e) {
    e.preventDefault();
    e.returnValue = '';
});

// ==========================================
// DRAG AND DROP REORDERING (path rows)
// ==========================================
function setupDragAndDrop(pathRow, dragHandle) {
    dragHandle.addEventListener('mousedown', () => { pathRow.setAttribute('draggable', 'true'); });
    dragHandle.addEventListener('mouseup', () => { pathRow.removeAttribute('draggable'); });
    dragHandle.addEventListener('mouseleave', () => { pathRow.removeAttribute('draggable'); });

    pathRow.addEventListener('dragstart', (e) => {
        pathRow.classList.add('dragging');
        e.dataTransfer.setData('text/plain', '');
    });

    pathRow.addEventListener('dragend', () => {
        pathRow.classList.remove('dragging');
        pathRow.removeAttribute('draggable');
    });
}

const pathContainerDrag = document.getElementById('path-container');

pathContainerDrag.addEventListener('dragover', (e) => {
    e.preventDefault();
    const draggingRow = document.querySelector('.dragging');
    if (!draggingRow) return;

    const afterElement = getDragAfterElement(pathContainerDrag, e.clientY);
    if (afterElement == null) {
        pathContainerDrag.appendChild(draggingRow);
    } else {
        pathContainerDrag.insertBefore(draggingRow, afterElement);
    }
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.path-group:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}