/**
 * Cosmetic Alena - Main JavaScript File
 * Professional Beauty & Cosmetic Services Website
 */

$(document).ready(function() {
    console.log('Cosmetic Alena website loaded');

    // ========================================================================
    // Newsletter Subscription
    // ========================================================================
    
    let newsletterSubmitting = false;

    $('#newsletter-form').on('submit', function(e) {
        const emailInput = $('#newsletter-email');
        const email = emailInput.val().trim();

        if (!email) {
            e.preventDefault();
            showAlert('Пожалуйста, введите ваш email', 'warning');
            return;
        }

        newsletterSubmitting = true;
        showAlert('Оформляем подписку... Пожалуйста, подождите.', 'info', 3000);
    });

    $('#newsletter-target').on('load', function() {
        if (!newsletterSubmitting) {
            return;
        }

        newsletterSubmitting = false;
        showAlert('Спасибо! Вы подписаны!', 'success');
        $('#newsletter-form')[0].reset();
    });

    // ========================================================================
    // Smooth Scroll for Anchor Links
    // ========================================================================
    
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $($(this).attr('href'));
        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 100
            }, 800);
        }
    });

    // ========================================================================
    // Navbar Scroll Effect
    // ========================================================================
    
    $(window).on('scroll', function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar-custom').addClass('shadow-sm');
        } else {
            $('.navbar-custom').removeClass('shadow-sm');
        }
    });

    // ========================================================================
    // Gallery Filter
    // ========================================================================
    
    $('.gallery-filter-btn').on('click', function() {
        const filter = $(this).data('filter');
        
        $('.gallery-filter-btn').removeClass('active');
        $(this).addClass('active');
        
        if (filter === 'all') {
            $('.gallery-item').fadeIn();
        } else {
            $('.gallery-item').fadeOut();
            $('.gallery-item[data-category="' + filter + '"]').fadeIn();
        }
    });

    // ========================================================================
    // Lazy Loading Images
    // ========================================================================
    
    if ('IntersectionObserver' in window) {
        let imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    let img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('fade-in');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img));
    }

    // ========================================================================
    // Form Validation
    // ========================================================================
    
    $('form').on('submit', function(e) {
        let isValid = true;
        
        $(this).find('[required]').each(function() {
            if (!$(this).val()) {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showAlert('Please fill in all required fields', 'warning');
        }
    });

    // Remove invalid class when user starts typing
    $('input[required], textarea[required]').on('input', function() {
        if ($(this).val()) {
            $(this).removeClass('is-invalid');
        }
    });

    // ========================================================================
    // Appointment Booking
    // ========================================================================
    
    $('#bookingForm').on('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            name: $('#name').val(),
            email: $('#email').val(),
            phone: $('#phone').val(),
            service_id: $('#service').val(),
            appointment_date: new Date($('#appointment_date').val() + ' ' + $('#appointment_time').val()).toISOString(),
            notes: $('#notes').val()
        };
        
        $.ajax({
            url: '/api/appointments',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                showAlert('Appointment booked successfully! Check your email for confirmation.', 'success');
                $('#bookingForm')[0].reset();
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            },
            error: function(xhr) {
                let message = 'Failed to book appointment. Please try again.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    message = xhr.responseJSON.error;
                }
                showAlert(message, 'danger');
            }
        });
    });

    // ========================================================================
    // Contact Form
    // ========================================================================
    
    $('#contactForm').on('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            name: $('#name').val(),
            email: $('#email').val(),
            phone: $('#phone').val(),
            subject: $('#subject').val(),
            message: $('#message').val()
        };
        
        $.ajax({
            url: '/contact',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                showAlert('Thank you for your message! We will respond shortly.', 'success');
                $('#contactForm')[0].reset();
            },
            error: function(xhr) {
                showAlert('Failed to send message. Please try again.', 'danger');
            }
        });
    });

    // ========================================================================
    // Tooltip Initialization
    // ========================================================================
    
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ========================================================================
    // Mobile Menu Close
    // ========================================================================
    
    $('.navbar-collapse a:not(.dropdown-toggle)').on('click', function() {
        $('.navbar-collapse').collapse('hide');
    });

    // ========================================================================
    // Animate Numbers on Scroll
    // ========================================================================
    
    const animateNumbers = () => {
        const numberElements = document.querySelectorAll('[data-target-number]');
        
        if ('IntersectionObserver' in window) {
            const numberObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                        animateNumber(entry.target);
                        entry.target.classList.add('animated');
                    }
                });
            });
            
            numberElements.forEach(el => numberObserver.observe(el));
        }
    };

    const animateNumber = (element) => {
        const target = parseInt(element.dataset.targetNumber);
        const duration = 2000;
        const start = 0;
        const startTime = Date.now();

        const updateNumber = () => {
            const elapsed = Date.now() - startTime;
            const progress = elapsed / duration;
            const current = Math.round(start + (target - start) * progress);
            
            element.textContent = current;

            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            } else {
                element.textContent = target;
            }
        };

        updateNumber();
    };

    animateNumbers();

    // ========================================================================
    // Utility Functions
    // ========================================================================
    
    /**
     * Show alert message
     * @param {string} message - Alert message
     * @param {string} type - Alert type (success, danger, warning, info)
     * @param {number} duration - Dismiss after duration (ms)
     */
    window.showAlert = function(message, type = 'info', duration = 5000) {
        const alertId = 'alert-' + Date.now();
        const alertHTML = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const alertContainer = $('#alert-container');
        if (alertContainer.length) {
            alertContainer.prepend(alertHTML);
        } else {
            $('body').prepend(alertHTML);
        }
        
        // Auto-dismiss
        if (duration > 0) {
            setTimeout(() => {
                $('#' + alertId).fadeOut(() => $('#' + alertId).remove());
            }, duration);
        }
    };

    /**
     * Format currency
     * @param {number} amount - Amount to format
     * @param {string} currency - Currency code (default: USD)
     * @returns {string} Formatted currency string
     */
    window.formatCurrency = function(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    };

    /**
     * Format date
     * @param {Date} date - Date to format
     * @param {string} format - Format string (default: en-US)
     * @returns {string} Formatted date string
     */
    window.formatDate = function(date, format = 'en-US') {
        return new Intl.DateTimeFormat(format, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    };

    /**
     * Debounce function
     * @param {function} func - Function to debounce
     * @param {number} wait - Wait time (ms)
     * @returns {function} Debounced function
     */
    window.debounce = function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };

    /**
     * Throttle function
     * @param {function} func - Function to throttle
     * @param {number} limit - Time limit (ms)
     * @returns {function} Throttled function
     */
    window.throttle = function(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    };

    // ========================================================================
    // Accessibility
    // ========================================================================
    
    // Add keyboard navigation for dropdowns
    $('[data-bs-toggle="dropdown"]').on('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            $(this).dropdown('toggle');
        }
    });

    // Skip to main content link
    const skipLink = document.querySelector('.skip-to-main');
    if (skipLink) {
        skipLink.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelector('main').focus();
        });
    }

    console.log('✓ All scripts initialized');
});

// ============================================================================
// Page Load Animation
// ============================================================================

$(window).on('load', function() {
    $('body').addClass('loaded');
    
    // Fade in elements with fade-in class
    $('.fade-in').each(function(index) {
        $(this).delay(index * 100).fadeIn(500);
    });
});

// ============================================================================
// Service Worker (for PWA support)
// ============================================================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/sw.js').catch(err => {
            console.log('Service Worker registration failed:', err);
        });
    });
}
