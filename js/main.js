/**
 * Wiley University - Business & Finance Website
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initDropdownMenus();
    initFAQAccordion();
    initSmoothScroll();
});

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');

            // Update aria-expanded
            const isExpanded = mainNav.classList.contains('active');
            menuToggle.setAttribute('aria-expanded', isExpanded);

            // Change icon
            menuToggle.innerHTML = isExpanded ? '&times;' : '&#9776;';
        });
    }
}

/**
 * Dropdown Menu for Mobile
 */
function initDropdownMenus() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function(dropdown) {
        const link = dropdown.querySelector('a');

        // For mobile: toggle dropdown on click
        if (link) {
            link.addEventListener('click', function(e) {
                // Only prevent default on mobile
                if (window.innerWidth <= 992) {
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                }
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            dropdowns.forEach(function(dropdown) {
                dropdown.classList.remove('active');
            });
        }
    });
}

/**
 * FAQ Accordion
 */
function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(function(item) {
        const question = item.querySelector('.faq-question');

        if (question) {
            question.addEventListener('click', function() {
                // Close other open items (optional - remove for multi-open)
                faqItems.forEach(function(otherItem) {
                    if (otherItem !== item && otherItem.classList.contains('active')) {
                        otherItem.classList.remove('active');
                    }
                });

                // Toggle current item
                item.classList.toggle('active');
            });
        }
    });
}

/**
 * Smooth Scroll for Anchor Links
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Skip if it's just "#" or empty
            if (href === '#' || href === '') {
                return;
            }

            const target = document.querySelector(href);

            if (target) {
                e.preventDefault();

                // Calculate offset for sticky header
                const headerHeight = document.querySelector('.site-header')?.offsetHeight || 0;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Handle window resize
 */
window.addEventListener('resize', debounce(function() {
    // Reset mobile menu on resize to desktop
    if (window.innerWidth > 992) {
        const mainNav = document.querySelector('.main-nav');
        const menuToggle = document.querySelector('.mobile-menu-toggle');

        if (mainNav) {
            mainNav.classList.remove('active');
        }
        if (menuToggle) {
            menuToggle.innerHTML = '&#9776;';
            menuToggle.setAttribute('aria-expanded', 'false');
        }

        // Reset dropdowns
        document.querySelectorAll('.dropdown').forEach(function(dropdown) {
            dropdown.classList.remove('active');
        });
    }
}, 250));
