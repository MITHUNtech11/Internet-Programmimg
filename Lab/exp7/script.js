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

    // Form elements
    const form = document.getElementById('regForm');
    const userName = document.getElementById('userName');
    const userEmail = document.getElementById('userEmail');
    const userMessage = document.getElementById('userMessage');
    const charCount = document.getElementById('charCount');
    const btnCancel = document.getElementById('btnCancel');
    const jsonPreview = document.getElementById('jsonPreview');
    const statusAlert = document.getElementById('statusAlert');

    const chkName = document.getElementById('chk-name');
    const chkEmail = document.getElementById('chk-email');
    const chkMessage = document.getElementById('chk-message');

    // Validators
    function validateName() {
        const val = userName.value.trim();
        const valid = /^[A-Za-z\s]{3,50}$/.test(val);
        const group = document.getElementById('group-name');
        if (valid) {
            group.classList.remove('has-error');
            group.classList.add('has-success');
            chkName.textContent = '✓ Name: Validated';
            chkName.className = 'valid';
        } else {
            group.classList.add('has-error');
            group.classList.remove('has-success');
            chkName.textContent = '○ Name: Letters only, min 3 chars';
            chkName.className = '';
        }
        return valid;
    }

    function validateEmail() {
        const val = userEmail.value.trim();
        const valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val);
        const group = document.getElementById('group-email');
        if (valid) {
            group.classList.remove('has-error');
            group.classList.add('has-success');
            chkEmail.textContent = '✓ Email: Validated RFC format';
            chkEmail.className = 'valid';
        } else {
            group.classList.add('has-error');
            group.classList.remove('has-success');
            chkEmail.textContent = '○ Email: RFC standard format';
            chkEmail.className = '';
        }
        return valid;
    }

    function validateMessage() {
        const val = userMessage.value.trim();
        const valid = val.length >= 20;
        const group = document.getElementById('group-message');
        charCount.textContent = val.length;

        if (valid) {
            group.classList.remove('has-error');
            group.classList.add('has-success');
            chkMessage.textContent = '✓ Message: Length requirement met';
            chkMessage.className = 'valid';
        } else {
            group.classList.add('has-error');
            group.classList.remove('has-success');
            chkMessage.textContent = '○ Message: Minimum 20 characters';
            chkMessage.className = '';
        }
        return valid;
    }

    userName.addEventListener('input', validateName);
    userEmail.addEventListener('input', validateEmail);
    userMessage.addEventListener('input', validateMessage);

    btnCancel.addEventListener('click', () => {
        form.reset();
        charCount.textContent = '0';
        document.querySelectorAll('.form-group').forEach(g => {
            g.classList.remove('has-error', 'has-success');
        });
        chkName.textContent = '○ Name: Letters only, min 3 chars';
        chkName.className = '';
        chkEmail.textContent = '○ Email: RFC standard format';
        chkEmail.className = '';
        chkMessage.textContent = '○ Message: Minimum 20 characters';
        chkMessage.className = '';

        statusAlert.className = 'alert-box idle';
        statusAlert.querySelector('.alert-content').innerHTML = `
            <strong>Form Cleared</strong>
            <p>Ready for new applicant data entry.</p>
        `;
        jsonPreview.textContent = JSON.stringify({ status: "cleared_and_idle" }, null, 2);
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const isNameOk = validateName();
        const isEmailOk = validateEmail();
        const isMsgOk = validateMessage();

        if (isNameOk && isEmailOk && isMsgOk) {
            const payload = {
                applicantName: userName.value.trim(),
                emailAddress: userEmail.value.trim(),
                message: userMessage.value.trim(),
                submittedAt: new Date().toISOString(),
                status: "APPROVED_FOR_PROCESSING"
            };

            jsonPreview.textContent = JSON.stringify(payload, null, 2);
            statusAlert.className = 'alert-box success';
            statusAlert.querySelector('.alert-content').innerHTML = `
                <strong>Application Successfully Submitted!</strong>
                <p>Client-side validation passed with zero errors.</p>
            `;
        } else {
            statusAlert.className = 'alert-box has-error';
            statusAlert.querySelector('.alert-content').innerHTML = `
                <strong style="color: #ef4444;">Validation Failed</strong>
                <p>Please review and fix highlighted red fields above.</p>
            `;
        }
    });
});
