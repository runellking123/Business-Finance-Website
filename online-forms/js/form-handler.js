/**
 * Wiley University - Online Form Handler
 * Handles form submission via Netlify Forms
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('wiley-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

/**
 * Handle form submission with loading state
 */
async function handleFormSubmit(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Submitting...';

    // Let the form submit naturally to Netlify
    // The form will redirect to the success page via the action attribute
}

/**
 * Form validation helpers
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\(\)\.]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}
