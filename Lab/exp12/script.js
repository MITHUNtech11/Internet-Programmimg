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

    // 1. Number Equality Logic
    const num1 = document.getElementById('num1');
    const num2 = document.getElementById('num2');
    const btnCompare = document.getElementById('btnCompare');
    const btnFloatTest = document.getElementById('btnFloatTest');
    const equalityResult = document.getElementById('equalityResult');
    const equalityMsg = document.getElementById('equalityMsg');

    function runCompare(n1, n2) {
        if (n1 === '' || n2 === '') {
            equalityResult.className = 'result-box fail';
            equalityMsg.textContent = 'Please enter both numbers to perform comparison.';
            return;
        }

        const v1 = parseFloat(n1);
        const v2 = parseFloat(n2);

        if (isNaN(v1) || isNaN(v2)) {
            equalityResult.className = 'result-box fail';
            equalityMsg.textContent = 'Invalid numerical format.';
            return;
        }

        if (v1 === v2) {
            equalityResult.className = 'result-box success';
            equalityMsg.innerHTML = `<strong>EQUAL:</strong> ${v1} and ${v2} have identical numerical value and type.<br><small>Strict Check (===): true</small>`;
        } else {
            equalityResult.className = 'result-box fail';
            equalityMsg.innerHTML = `<strong>NOT EQUAL:</strong> ${v1} &ne; ${v2}. Difference is ${Math.abs(v1 - v2)}.<br><small>Strict Check (===): false</small>`;
        }
    }

    btnCompare.addEventListener('click', () => {
        runCompare(num1.value, num2.value);
    });

    btnFloatTest.addEventListener('click', () => {
        num1.value = 0.1 + 0.2;
        num2.value = 0.3;
        const rawV1 = 0.1 + 0.2;
        const rawV2 = 0.3;
        const diff = Math.abs(rawV1 - rawV2);

        equalityResult.className = 'result-box fail';
        equalityMsg.innerHTML = `<strong>Floating Point Quirk:</strong> (0.1 + 0.2 = ${rawV1}) vs 0.3.<br>Direct strict equality: <code>0.1 + 0.2 === 0.3 &rarr; false</code><br>Epsilon check <code>diff &lt; Number.EPSILON &rarr; ${diff < Number.EPSILON}</code>`;
    });

    // 2. Sentence Array Word Search
    const sentenceInput = document.getElementById('sentenceInput');
    const arrayChips = document.getElementById('arrayChips');
    const searchWord = document.getElementById('searchWord');
    const btnSearchWord = document.getElementById('btnSearchWord');
    const searchResult = document.getElementById('searchResult');
    const searchMsg = document.getElementById('searchMsg');

    let currentTokens = [];

    function renderTokens() {
        const text = sentenceInput.value.trim();
        currentTokens = text ? text.split(/\s+/) : [];
        arrayChips.innerHTML = '';
        currentTokens.forEach((word, idx) => {
            const chip = document.createElement('span');
            chip.className = 'word-chip';
            chip.dataset.idx = idx;
            chip.innerHTML = `<span class="idx">[${idx}]</span>${word}`;
            arrayChips.appendChild(chip);
        });
    }

    sentenceInput.addEventListener('input', renderTokens);
    renderTokens();

    btnSearchWord.addEventListener('click', () => {
        const target = searchWord.value.trim();
        if (!target) {
            searchResult.className = 'result-box fail';
            searchMsg.textContent = 'Please enter a word to search for.';
            return;
        }

        // Reset chips
        document.querySelectorAll('.word-chip').forEach(c => c.classList.remove('match'));

        const clean = str => str.toLowerCase().replace(/[^a-z0-9]/g, '');
        const targetClean = clean(target);

        const foundIndex = currentTokens.findIndex(token => clean(token) === targetClean);

        if (foundIndex !== -1) {
            const matchedChip = arrayChips.children[foundIndex];
            if (matchedChip) matchedChip.classList.add('match');

            searchResult.className = 'result-box success';
            searchMsg.innerHTML = `<strong>Word Found!</strong><br>Found "${target}" at zero-based array index <code>[${foundIndex}]</code> (Word #${foundIndex + 1} of ${currentTokens.length}).`;
        } else {
            searchResult.className = 'result-box fail';
            searchMsg.innerHTML = `<strong>Word Not Found:</strong> "${target}" does not exist in the array. <code>indexOf() &rarr; -1</code>.`;
        }
    });
});
