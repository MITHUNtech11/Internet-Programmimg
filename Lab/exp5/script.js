/**
 * Client Interactivity & Navigation Logic: Roast & Brew Coffee Roasters (exp5)
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Hamburger Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('nav-open');
        });
    }

    // 2. Active Link Highlight based on current path
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const allNavLinks = document.querySelectorAll('.nav-link');

    allNavLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '' && href === 'index.html')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // 3. Contact Form Validation & Toast Notification (for contact.html)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        const nameInput = document.getElementById('contactName');
        const emailInput = document.getElementById('contactEmail');
        const inquirySelect = document.getElementById('inquiryType');
        const messageInput = document.getElementById('contactMessage');
        const contactToast = document.getElementById('contactToast');

        const nameError = document.getElementById('nameError');
        const emailError = document.getElementById('emailError');
        const inquiryError = document.getElementById('inquiryError');
        const messageError = document.getElementById('messageError');

        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

        function setError(input, errElem, msg) {
            input.classList.add('is-error');
            errElem.textContent = msg;
        }

        function clearError(input, errElem) {
            input.classList.remove('is-error');
            errElem.textContent = '';
        }

        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            let isValid = true;

            // Validate Name
            if (nameInput.value.trim().length < 2) {
                setError(nameInput, nameError, 'Please enter your name (min 2 characters).');
                isValid = false;
            } else {
                clearError(nameInput, nameError);
            }

            // Validate Email
            if (!emailRegex.test(emailInput.value.trim())) {
                setError(emailInput, emailError, 'Please enter a valid email address.');
                isValid = false;
            } else {
                clearError(emailInput, emailError);
            }

            // Validate Inquiry Type
            if (!inquirySelect.value) {
                setError(inquirySelect, inquiryError, 'Please select the nature of your inquiry.');
                isValid = false;
            } else {
                clearError(inquirySelect, inquiryError);
            }

            // Validate Message
            if (messageInput.value.trim().length < 10) {
                setError(messageInput, messageError, 'Please enter a message of at least 10 characters.');
                isValid = false;
            } else {
                clearError(messageInput, messageError);
            }

            if (!isValid) return;

            // Display Toast Alert
            contactToast.style.display = 'block';
            contactToast.innerHTML = `
                ✓ <strong>Thank you, ${escapeHtml(nameInput.value.trim())}!</strong> Your inquiry regarding 
                <em>"${escapeHtml(inquirySelect.value)}"</em> has been received. Our roasting team will reach out to you shortly.
            `;

            // Reset form
            contactForm.reset();
            clearError(nameInput, nameError);
            clearError(emailInput, emailError);
            clearError(inquirySelect, inquiryError);
            clearError(messageInput, messageError);

            // Auto-scroll to toast
            contactToast.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
    }

    function escapeHtml(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
