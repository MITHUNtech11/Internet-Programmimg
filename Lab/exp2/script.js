/**
 * Client-Side Validation & Interactivity for Job Application Form (exp2)
 * Features:
 * - Real-time input validation on blur and input
 * - Regex format validation for Email and Name
 * - Radio button group validation for Gender
 * - Dropdown validation for Qualification Degree
 * - Cancel / Reset button confirmation and state cleanup
 * - Submission modal popup displaying sanitized applicant summary
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('jobAppForm');
    const nameInput = document.getElementById('applicantName');
    const emailInput = document.getElementById('applicantEmail');
    const phoneInput = document.getElementById('applicantPhone');
    const degreeSelect = document.getElementById('highestDegree');
    const positionSelect = document.getElementById('targetPosition');
    const coverNote = document.getElementById('coverNote');
    const charCountSpan = document.getElementById('charCount');
    const cancelBtn = document.getElementById('cancelBtn');
    const statusAlert = document.getElementById('statusAlert');
    const confirmationModal = document.getElementById('confirmationModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const modalSubmittedData = document.getElementById('modalSubmittedData');

    // Error message containers
    const nameError = document.getElementById('nameError');
    const emailError = document.getElementById('emailError');
    const phoneError = document.getElementById('phoneError');
    const degreeError = document.getElementById('degreeError');
    const genderError = document.getElementById('genderError');
    const positionError = document.getElementById('positionError');

    // Regular Expression patterns
    const regexName = /^[A-Za-z\s.'-]{3,60}$/;
    const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const regexPhone = /^[+]?[(]?[0-9]{1,4}[)]?[-\s./0-9]{7,15}$/;

    // Character Counter for Cover Note
    coverNote.addEventListener('input', () => {
        const length = coverNote.value.length;
        charCountSpan.textContent = length;
        if (length > 500) {
            coverNote.value = coverNote.value.substring(0, 500);
            charCountSpan.textContent = 500;
        }
    });

    // Helper: Mark field valid
    function setValid(inputElement, errorElement) {
        inputElement.classList.remove('is-invalid');
        inputElement.classList.add('is-valid');
        errorElement.textContent = '';
    }

    // Helper: Mark field invalid
    function setInvalid(inputElement, errorElement, message) {
        inputElement.classList.remove('is-valid');
        inputElement.classList.add('is-invalid');
        errorElement.textContent = message;
    }

    // Helper: Clear field state
    function clearFieldState(inputElement, errorElement) {
        inputElement.classList.remove('is-valid', 'is-invalid');
        errorElement.textContent = '';
    }

    // Validation: Name
    function validateName() {
        const val = nameInput.value.trim();
        if (val === '') {
            setInvalid(nameInput, nameError, 'Full name is mandatory.');
            return false;
        } else if (!regexName.test(val)) {
            setInvalid(nameInput, nameError, 'Please enter a valid full name (letters only, min 3 characters).');
            return false;
        }
        setValid(nameInput, nameError);
        return true;
    }

    // Validation: Email
    function validateEmail() {
        const val = emailInput.value.trim();
        if (val === '') {
            setInvalid(emailInput, emailError, 'Email address is mandatory.');
            return false;
        } else if (!regexEmail.test(val)) {
            setInvalid(emailInput, emailError, 'Please enter a valid email format (e.g., user@domain.com).');
            return false;
        }
        setValid(emailInput, emailError);
        return true;
    }

    // Validation: Phone
    function validatePhone() {
        const val = phoneInput.value.trim();
        if (val === '') {
            setInvalid(phoneInput, phoneError, 'Contact phone number is mandatory.');
            return false;
        } else if (!regexPhone.test(val)) {
            setInvalid(phoneInput, phoneError, 'Please enter a valid phone number (min 7 digits).');
            return false;
        }
        setValid(phoneInput, phoneError);
        return true;
    }

    // Validation: Degree
    function validateDegree() {
        if (!degreeSelect.value) {
            setInvalid(degreeSelect, degreeError, 'Please select your highest qualified degree.');
            return false;
        }
        setValid(degreeSelect, degreeError);
        return true;
    }

    // Validation: Position
    function validatePosition() {
        if (!positionSelect.value) {
            setInvalid(positionSelect, positionError, 'Please select the position you are applying for.');
            return false;
        }
        setValid(positionSelect, positionError);
        return true;
    }

    // Validation: Gender
    function validateGender() {
        const selectedGender = document.querySelector('input[name="gender"]:checked');
        if (!selectedGender) {
            genderError.textContent = 'Please select your gender.';
            return false;
        }
        genderError.textContent = '';
        return true;
    }

    // Real-time Event Listeners for inputs
    nameInput.addEventListener('input', validateName);
    nameInput.addEventListener('blur', validateName);

    emailInput.addEventListener('input', validateEmail);
    emailInput.addEventListener('blur', validateEmail);

    phoneInput.addEventListener('input', validatePhone);
    phoneInput.addEventListener('blur', validatePhone);

    degreeSelect.addEventListener('change', validateDegree);
    positionSelect.addEventListener('change', validatePosition);

    document.querySelectorAll('input[name="gender"]').forEach(radio => {
        radio.addEventListener('change', validateGender);
    });

    // Form Submission Handler
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Run all field validations
        const isNameOk = validateName();
        const isEmailOk = validateEmail();
        const isPhoneOk = validatePhone();
        const isDegreeOk = validateDegree();
        const isGenderOk = validateGender();
        const isPositionOk = validatePosition();

        const isFormValid = isNameOk && isEmailOk && isPhoneOk && isDegreeOk && isGenderOk && isPositionOk;

        if (!isFormValid) {
            statusAlert.className = 'status-alert alert-error';
            statusAlert.textContent = '⚠️ Application validation failed. Please correct the highlighted errors above before submitting.';
            statusAlert.style.display = 'block';

            // Smooth scroll to the first invalid element
            const firstInvalid = form.querySelector('.is-invalid') || form.querySelector('input[name="gender"]:not(:checked)');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            return;
        }

        // Hide alert if valid
        statusAlert.style.display = 'none';

        // Retrieve submitted values
        const selectedGender = document.querySelector('input[name="gender"]:checked').value;
        const note = coverNote.value.trim() || 'No additional note provided.';

        // Populate Modal Details
        modalSubmittedData.innerHTML = `
            <div><strong>Applicant Name:</strong> ${escapeHtml(nameInput.value.trim())}</div>
            <div><strong>Email Address:</strong> ${escapeHtml(emailInput.value.trim())}</div>
            <div><strong>Contact Number:</strong> ${escapeHtml(phoneInput.value.trim())}</div>
            <div><strong>Highest Degree:</strong> ${escapeHtml(degreeSelect.value)}</div>
            <div><strong>Gender:</strong> ${escapeHtml(selectedGender)}</div>
            <div><strong>Position Applied:</strong> ${escapeHtml(positionSelect.value)}</div>
            <div style="margin-top: 6px;"><strong>Statement / Note:</strong> <em>${escapeHtml(note)}</em></div>
        `;

        // Show Confirmation Modal
        confirmationModal.style.display = 'flex';
    });

    // Cancel / Reset Button Handler
    cancelBtn.addEventListener('click', () => {
        const userChoice = confirm('Are you sure you want to cancel and reset the job application form? Any unsaved entries will be discarded.');
        if (userChoice) {
            form.reset();
            clearFieldState(nameInput, nameError);
            clearFieldState(emailInput, emailError);
            clearFieldState(phoneInput, phoneError);
            clearFieldState(degreeSelect, degreeError);
            clearFieldState(positionSelect, positionError);
            genderError.textContent = '';
            charCountSpan.textContent = '0';
            statusAlert.style.display = 'none';
        }
    });

    // Close Confirmation Modal Handler
    closeModalBtn.addEventListener('click', () => {
        confirmationModal.style.display = 'none';
        form.reset();
        clearFieldState(nameInput, nameError);
        clearFieldState(emailInput, emailError);
        clearFieldState(phoneInput, phoneError);
        clearFieldState(degreeSelect, degreeError);
        clearFieldState(positionSelect, positionError);
        genderError.textContent = '';
        charCountSpan.textContent = '0';
    });

    // Security helper to escape HTML tags
    function escapeHtml(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
