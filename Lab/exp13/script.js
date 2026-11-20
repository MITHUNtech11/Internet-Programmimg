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

    const form = document.getElementById('fullRegForm');
    const txtName = document.getElementById('txtName');
    const txtAge = document.getElementById('txtAge');
    const txtEmail = document.getElementById('txtEmail');
    const selCountry = document.getElementById('selCountry');
    const txtAddress = document.getElementById('txtAddress');
    const summaryCard = document.getElementById('successSummary');
    const summaryBody = document.getElementById('summaryBody');

    function checkField(groupEl, isValid) {
        if (!isValid) groupEl.classList.add('has-error');
        else groupEl.classList.remove('has-error');
        return isValid;
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let valid = true;

        // Name
        const nameVal = txtName.value.trim();
        valid = checkField(document.getElementById('grp-name'), /^[A-Za-z\s]{3,}$/.test(nameVal)) && valid;

        // Age
        const ageVal = parseInt(txtAge.value, 10);
        valid = checkField(document.getElementById('grp-age'), !isNaN(ageVal) && ageVal >= 18 && ageVal <= 100) && valid;

        // Email
        const emailVal = txtEmail.value.trim();
        valid = checkField(document.getElementById('grp-email'), /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(emailVal)) && valid;

        // Country
        valid = checkField(document.getElementById('grp-country'), selCountry.value !== "") && valid;

        // Address
        const addrVal = txtAddress.value.trim();
        valid = checkField(document.getElementById('grp-address'), addrVal.length >= 10) && valid;

        // Gender (Radio)
        const genderEl = document.querySelector('input[name="gender"]:checked');
        valid = checkField(document.getElementById('grp-gender'), genderEl !== null) && valid;

        // Hobby (Checkboxes)
        const hobbyEls = document.querySelectorAll('input[name="hobby"]:checked');
        valid = checkField(document.getElementById('grp-hobby'), hobbyEls.length > 0) && valid;

        if (valid) {
            const hobbies = Array.from(hobbyEls).map(cb => cb.value);
            const payload = {
                name: nameVal,
                age: ageVal,
                email: emailVal,
                country: selCountry.value,
                address: addrVal,
                gender: genderEl.value,
                hobbies: hobbies,
                registeredAt: new Date().toLocaleString()
            };

            summaryBody.innerHTML = `<pre>${JSON.stringify(payload, null, 2)}</pre>`;
            summaryCard.classList.remove('hidden');
            summaryCard.scrollIntoView({ behavior: 'smooth' });
        } else {
            summaryCard.classList.add('hidden');
        }
    });

    document.getElementById('btnFormReset').addEventListener('click', () => {
        document.querySelectorAll('.form-group').forEach(g => g.classList.remove('has-error'));
        summaryCard.classList.add('hidden');
    });
});
