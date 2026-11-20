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

    // 1. Factorial caller
    const inputFact = document.getElementById('inputFact');
    const btnRunFact = document.getElementById('btnRunFact');
    const valFact = document.getElementById('valFact');
    const traceFact = document.getElementById('traceFact');

    btnRunFact.addEventListener('click', () => {
        const n = parseInt(inputFact.value, 10);
        // Call the external reusable function from operations.js
        const result = calculateFactorial(n);

        valFact.textContent = result;
        if (typeof result === 'number') {
            valFact.className = 'res-value ok';
            if (n <= 8) {
                const terms = [];
                for (let i = n; i >= 1; i--) terms.push(i);
                traceFact.textContent = `${n}! = ${terms.join(' × ')} = ${result}`;
            } else {
                traceFact.textContent = `Calculated ${n}! via iterative loop.`;
            }
        } else {
            valFact.className = 'res-value err';
            traceFact.textContent = result;
        }
    });

    // 2. Sum of digits caller
    const inputSum = document.getElementById('inputSum');
    const btnRunSum = document.getElementById('btnRunSum');
    const valSum = document.getElementById('valSum');
    const traceSum = document.getElementById('traceSum');

    btnRunSum.addEventListener('click', () => {
        const val = inputSum.value;
        // Call the external reusable function from operations.js
        const result = sumOfDigits(val);

        valSum.textContent = result;
        if (typeof result === 'number') {
            valSum.className = 'res-value ok';
            const digits = String(val).replace(/[^0-9]/g, '').split('');
            traceSum.textContent = `${digits.join(' + ')} = ${result}`;
        } else {
            valSum.className = 'res-value err';
            traceSum.textContent = result;
        }
    });

    // 3. Palindrome caller
    const inputPalin = document.getElementById('inputPalin');
    const btnRunPalin = document.getElementById('btnRunPalin');
    const valPalin = document.getElementById('valPalin');
    const tracePalin = document.getElementById('tracePalin');

    btnRunPalin.addEventListener('click', () => {
        const str = inputPalin.value;
        // Call the external reusable function from operations.js
        const result = isPalindrome(str);

        if (typeof result === 'boolean') {
            if (result) {
                valPalin.textContent = 'true (PALINDROME)';
                valPalin.className = 'res-value ok';
            } else {
                valPalin.textContent = 'false (NOT PALINDROME)';
                valPalin.className = 'res-value err';
            }
            const norm = str.toLowerCase().replace(/[^a-z0-9]/g, '');
            tracePalin.textContent = `Normalized: "${norm}" (Length: ${norm.length})`;
        } else {
            valPalin.textContent = 'Error';
            valPalin.className = 'res-value err';
            tracePalin.textContent = result;
        }
    });
});
