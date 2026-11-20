document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const target = btn.dataset.tab;
            document.getElementById(target).classList.add('active');
        });
    });

    // Form inputs and live calculation
    const form = document.getElementById('modernForm');
    const fullName = document.getElementById('fullName');
    const userEmail = document.getElementById('userEmail');
    const expRange = document.getElementById('experienceLevel');
    const rangeVal = document.getElementById('rangeVal');
    const favColor = document.getElementById('favColor');
    const colorHex = document.getElementById('colorHex');
    const formProgress = document.getElementById('formProgress');
    const progressText = document.getElementById('progressText');
    const outputJson = document.getElementById('outputJson');
    const toast = document.getElementById('toastSuccess');

    expRange.addEventListener('input', (e) => {
        rangeVal.textContent = e.target.value;
        updatePreview();
    });

    favColor.addEventListener('input', (e) => {
        colorHex.textContent = e.target.value;
        updatePreview();
    });

    function calculateProgress() {
        let filled = 0;
        const total = 5;
        if (fullName.value.trim().length >= 3) filled++;
        if (userEmail.validity.valid && userEmail.value.trim()) filled++;
        if (document.getElementById('userAge').value) filled++;
        if (document.getElementById('birthDate').value) filled++;
        if (document.getElementById('techStack').value) filled++;

        const pct = Math.round((filled / total) * 100);
        formProgress.value = pct;
        progressText.textContent = `${pct}% Completed`;
    }

    function updatePreview() {
        calculateProgress();
        const data = {
            fullName: fullName.value || "(empty)",
            email: userEmail.value || "(empty)",
            age: document.getElementById('userAge').value,
            dob: document.getElementById('birthDate').value || "(unselected)",
            techStack: document.getElementById('techStack').value || "(unselected)",
            experienceRating: `${expRange.value}/10`,
            accentColor: favColor.value,
            timestamp: new Date().toISOString()
        };
        outputJson.textContent = JSON.stringify(data, null, 2);
    }

    form.addEventListener('input', () => {
        updatePreview();
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let valid = true;

        if (fullName.value.trim().length < 3) {
            fullName.classList.add('is-invalid');
            fullName.parentElement.querySelector('.error-msg').textContent = 'Full name must be at least 3 characters.';
            valid = false;
        } else {
            fullName.classList.remove('is-invalid');
            fullName.classList.add('is-valid');
            fullName.parentElement.querySelector('.error-msg').textContent = '';
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(userEmail.value.trim())) {
            userEmail.classList.add('is-invalid');
            userEmail.parentElement.querySelector('.error-msg').textContent = 'Please enter a valid email format.';
            valid = false;
        } else {
            userEmail.classList.remove('is-invalid');
            userEmail.classList.add('is-valid');
            userEmail.parentElement.querySelector('.error-msg').textContent = '';
        }

        if (valid) {
            toast.classList.remove('hidden');
            setTimeout(() => {
                toast.classList.add('hidden');
            }, 4000);
            updatePreview();
        }
    });

    updatePreview();
});
