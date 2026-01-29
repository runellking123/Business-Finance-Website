/**
 * Wiley University - Online Form Handler
 * Handles form submission to Google Sheets
 */

// IMPORTANT: Replace this URL with your Google Apps Script Web App URL
const GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_SCRIPT_URL_HERE';

/**
 * Initialize form handling
 */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('wiley-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const formType = form.dataset.formType;

    // Disable submit button and show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Submitting...';

    // Collect form data
    const formData = new FormData(form);
    const fields = {};

    formData.forEach((value, key) => {
        // Handle checkboxes (multiple values)
        if (fields[key]) {
            if (Array.isArray(fields[key])) {
                fields[key].push(value);
            } else {
                fields[key] = [fields[key], value];
            }
        } else {
            fields[key] = value;
        }
    });

    // Convert arrays to comma-separated strings
    for (let key in fields) {
        if (Array.isArray(fields[key])) {
            fields[key] = fields[key].join(', ');
        }
    }

    // Prepare payload
    const payload = {
        formType: formType,
        fields: fields,
        submittedAt: new Date().toISOString()
    };

    try {
        // Check if Google Script URL is configured
        if (GOOGLE_SCRIPT_URL === 'YOUR_GOOGLE_SCRIPT_URL_HERE') {
            throw new Error('Google Script URL not configured. Please follow the setup instructions.');
        }

        const response = await fetch(GOOGLE_SCRIPT_URL, {
            method: 'POST',
            mode: 'no-cors', // Required for Google Apps Script
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        // Since we're using no-cors, we can't read the response
        // Show success message
        showSuccessMessage(form, formType);

    } catch (error) {
        console.error('Form submission error:', error);
        showErrorMessage(form, error.message);

        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Submit Form';
    }
}

/**
 * Show success message
 */
function showSuccessMessage(form, formType) {
    const container = form.parentElement;

    // Generate a reference number
    const refNumber = 'WU-' + formType.substring(0, 3).toUpperCase() + '-' + Date.now().toString().slice(-8);

    container.innerHTML = `
        <div class="submission-success">
            <div class="success-icon">&#10003;</div>
            <h2>Form Submitted Successfully!</h2>
            <p>Thank you for your submission. Your request has been received and will be processed.</p>
            <div class="reference-number">
                <strong>Reference Number:</strong><br>
                <span class="ref-code">${refNumber}</span>
            </div>
            <p class="success-note">Please save this reference number for your records. You will also receive a confirmation email shortly.</p>
            <div class="success-actions">
                <a href="javascript:location.reload()" class="btn btn-outline">Submit Another Form</a>
                <a href="../../departments/transportation-fleet.html" class="btn btn-primary">Back to Transportation & Fleet</a>
            </div>
        </div>
    `;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Show error message
 */
function showErrorMessage(form, message) {
    // Remove any existing error messages
    const existingError = form.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }

    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error alert alert-warning';
    errorDiv.innerHTML = `
        <strong>Submission Error</strong><br>
        ${message}<br>
        <small>Please try again or contact Transportation & Fleet at (903) 927-3300.</small>
    `;

    form.insertBefore(errorDiv, form.firstChild);

    // Scroll to error
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
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

function validateRequired(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });

    return isValid;
}
