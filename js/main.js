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
 * Dropdown Menu for Mobile and Touch Devices
 */
function initDropdownMenus() {
    const dropdowns = document.querySelectorAll('.dropdown');
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    dropdowns.forEach(function(dropdown) {
        const link = dropdown.querySelector(':scope > a');
        const menu = dropdown.querySelector('.dropdown-menu');

        if (link && menu) {
            // Handle click/touch for mobile and touch devices
            link.addEventListener('click', function(e) {
                if (window.innerWidth <= 992 || isTouchDevice) {
                    e.preventDefault();
                    e.stopPropagation();

                    // Close other dropdowns
                    dropdowns.forEach(function(otherDropdown) {
                        if (otherDropdown !== dropdown) {
                            otherDropdown.classList.remove('active');
                        }
                    });

                    dropdown.classList.toggle('active');
                }
            });

            // Add keyboard accessibility
            link.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                }
                if (e.key === 'Escape') {
                    dropdown.classList.remove('active');
                    link.focus();
                }
            });

            // Handle keyboard navigation within dropdown
            menu.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    dropdown.classList.remove('active');
                    link.focus();
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

    // Close dropdowns on scroll (for mobile)
    window.addEventListener('scroll', function() {
        if (window.innerWidth <= 992) {
            dropdowns.forEach(function(dropdown) {
                dropdown.classList.remove('active');
            });
        }
    }, { passive: true });
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
