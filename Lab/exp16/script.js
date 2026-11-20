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

    // 1. Password Validator
    const pwdInput = document.getElementById('pwdInput');
    const togglePwd = document.getElementById('togglePwd');
    const fill = document.getElementById('strengthFill');
    const label = document.getElementById('strengthLabel');

    const cLen = document.getElementById('c-len');
    const cUpper = document.getElementById('c-upper');
    const cLower = document.getElementById('c-lower');
    const cNum = document.getElementById('c-num');
    const cSym = document.getElementById('c-sym');

    togglePwd.addEventListener('click', () => {
        pwdInput.type = pwdInput.type === 'password' ? 'text' : 'password';
    });

    pwdInput.addEventListener('input', () => {
        const val = pwdInput.value;
        const hasLen = val.length >= 8;
        const hasUpper = /[A-Z]/.test(val);
        const hasLower = /[a-z]/.test(val);
        const hasNum = /[0-9]/.test(val);
        const hasSym = /[^A-Za-z0-9]/.test(val);

        function updateCheck(el, condition, text) {
            if (condition) {
                el.className = 'valid';
                el.innerHTML = `&#10004; ${text}`;
            } else {
                el.className = '';
                el.innerHTML = `&#9675; ${text}`;
            }
        }

        updateCheck(cLen, hasLen, 'At least 8 characters long (<code>.{8,}</code>)');
        updateCheck(cUpper, hasUpper, 'Contains uppercase letter (<code>[A-Z]</code>)');
        updateCheck(cLower, hasLower, 'Contains lowercase letter (<code>[a-z]</code>)');
        updateCheck(cNum, hasNum, 'Contains numeric digit (<code>[0-9]</code>)');
        updateCheck(cSym, hasSym, 'Contains special symbol (<code>[!@#$%^&*]</code>)');

        let score = 0;
        if (hasLen) score += 20;
        if (hasUpper) score += 20;
        if (hasLower) score += 20;
        if (hasNum) score += 20;
        if (hasSym) score += 20;

        fill.style.width = `${score}%`;
        if (score <= 20) {
            fill.style.backgroundColor = '#ef4444';
            label.textContent = 'Password Strength: Very Weak';
            label.style.color = '#ef4444';
        } else if (score <= 60) {
            fill.style.backgroundColor = '#f59e0b';
            label.textContent = 'Password Strength: Moderate';
            label.style.color = '#f59e0b';
        } else if (score < 100) {
            fill.style.backgroundColor = '#3b82f6';
            label.textContent = 'Password Strength: Strong';
            label.style.color = '#3b82f6';
        } else {
            fill.style.backgroundColor = '#10b981';
            label.textContent = 'Password Strength: Excellent / Production Ready';
            label.style.color = '#10b981';
        }
    });

    // 2. RegExp Methods Explorer
    const patternInput = document.getElementById('patternInput');
    const sampleText = document.getElementById('sampleText');
    const btnTest = document.getElementById('btnTest');
    const btnExec = document.getElementById('btnExec');
    const btnMatch = document.getElementById('btnMatch');
    const consoleOut = document.getElementById('consoleOut');

    function getRegex() {
        try {
            return new RegExp(patternInput.value, 'g');
        } catch (err) {
            consoleOut.textContent = `Regex Compile Error: ${err.message}`;
            return null;
        }
    }

    btnTest.addEventListener('click', () => {
        const re = getRegex();
        if (!re) return;
        const res = re.test(sampleText.value);
        consoleOut.textContent = `RegExp.prototype.test() executed:
Target: "${sampleText.value}"
Pattern: ${re.toString()}
Result: ${res} (${res ? "Match Found" : "No Match"})`;
    });

    btnExec.addEventListener('click', () => {
        const re = getRegex();
        if (!re) return;
        const res = re.exec(sampleText.value);
        if (res) {
            consoleOut.textContent = `RegExp.prototype.exec() executed:
Matched String: "${res[0]}"
Match Index: ${res.index}
Groups Count: ${res.length - 1}
Input String: "${res.input}"`;
        } else {
            consoleOut.textContent = `RegExp.prototype.exec() executed:
Result: null (No matches found)`;
        }
    });

    btnMatch.addEventListener('click', () => {
        const re = getRegex();
        if (!re) return;
        const matches = sampleText.value.match(re);
        consoleOut.textContent = `String.prototype.match() executed:
All Matches Array: ${JSON.stringify(matches, null, 2)}`;
    });
});
