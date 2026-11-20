document.addEventListener('DOMContentLoaded', () => {
    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // 1. DOM Events Monitor
    const eventInput = document.getElementById('eventInput');
    const chipFocus = document.getElementById('chipFocus');
    const chipBlur = document.getElementById('chipBlur');
    const chipKeydown = document.getElementById('chipKeydown');
    const logList = document.getElementById('eventLogList');
    const btnClearLog = document.getElementById('btnClearLog');

    function addLog(type, msg) {
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        const time = new Date().toLocaleTimeString();
        entry.textContent = `[${time}] ${msg}`;
        logList.prepend(entry);
    }

    eventInput.addEventListener('focus', () => {
        chipFocus.classList.add('active');
        chipFocus.querySelector('span').textContent = 'FOCUSED';
        chipBlur.classList.remove('active');
        chipBlur.querySelector('span').textContent = 'Inactive';
        addLog('focus', 'EVENT: onfocus -> Input element gained user focus.');
    });

    eventInput.addEventListener('blur', () => {
        chipBlur.classList.add('active');
        chipBlur.querySelector('span').textContent = 'BLURRED';
        chipFocus.classList.remove('active');
        chipFocus.querySelector('span').textContent = 'Inactive';
        addLog('blur', 'EVENT: onblur -> Input element lost focus.');
    });

    eventInput.addEventListener('keydown', (e) => {
        chipKeydown.classList.add('active');
        chipKeydown.querySelector('span').textContent = `Key: "${e.key}"`;
        addLog('keydown', `EVENT: onkeydown -> Key="${e.key}", Code="${e.code}"`);
    });

    btnClearLog.addEventListener('click', () => {
        logList.innerHTML = '';
    });

    // 2. AJAX Auto-Complete
    const searchInput = document.getElementById('ajaxSearch');
    const dropdown = document.getElementById('suggestionsList');
    const spinner = document.getElementById('searchSpinner');
    const selectionCard = document.getElementById('selectionCard');
    const selectionText = document.getElementById('selectionText');

    let cachedData = null;

    async function fetchData() {
        if (!cachedData) {
            spinner.classList.remove('hidden');
            try {
                const res = await fetch('data.json');
                cachedData = await res.json();
            } catch (err) {
                console.error("AJAX Error:", err);
                cachedData = [
                    "JavaScript", "HTML5 Semantics", "CSS Grid Layout", "CSS Flexbox",
                    "Node.js", "Express.js", "React.js", "AJAX Asynchronous Requests",
                    "DOM Document Object Model", "DHTML Interactive Web", "Regular Expressions"
                ];
            } finally {
                spinner.classList.add('hidden');
            }
        }
        return cachedData;
    }

    searchInput.addEventListener('input', async (e) => {
        const query = e.target.value.trim().toLowerCase();
        if (!query) {
            dropdown.classList.add('hidden');
            return;
        }

        const data = await fetchData();
        const matches = data.filter(item => item.toLowerCase().includes(query));

        if (matches.length > 0) {
            dropdown.innerHTML = '';
            matches.forEach(match => {
                const item = document.createElement('div');
                item.className = 'suggestion-item';

                // Highlight matched substring
                const regex = new RegExp(`(${query})`, 'gi');
                item.innerHTML = match.replace(regex, '<strong>$1</strong>');

                item.addEventListener('click', () => {
                    searchInput.value = match;
                    dropdown.classList.add('hidden');
                    selectionCard.className = 'selection-card selected';
                    selectionText.textContent = match;
                });

                dropdown.appendChild(item);
            });
            dropdown.classList.remove('hidden');
        } else {
            dropdown.innerHTML = '<div class="suggestion-item" style="color:#64748b; cursor:default;">No matching technology found</div>';
            dropdown.classList.remove('hidden');
        }
    });

    // Hide dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-wrapper')) {
            dropdown.classList.add('hidden');
        }
    });
});
