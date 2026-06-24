// ========================================================================
// ANIMATIONS - Scale Animation and Other Effects
// ========================================================================

// Animate scale value
function animateScale(targetWeight) {
    const scaleValue = document.getElementById('scaleValue');
    const duration = 2000; // 2 seconds
    const startValue = 0;
    const startTime = Date.now();

    function updateValue() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutCubic = (t) => 1 - Math.pow(1 - t, 3);
        const eased = easeOutCubic(progress);
        
        const currentValue = startValue + (targetWeight - startValue) * eased;
        scaleValue.textContent = Math.round(currentValue);

        if (progress < 1) {
            requestAnimationFrame(updateValue);
        }
    }

    requestAnimationFrame(updateValue);
}

// Trigger scale animation on weight input change
const weightInput = document.getElementById('weight');
if (weightInput) {
    weightInput.addEventListener('input', (e) => {
        const weight = parseFloat(e.target.value) || 0;
        if (weight > 0) {
            animateScale(weight);
        }
    });
}

// Animate progress bars
function animateProgressBars() {
    const bars = document.querySelectorAll('.bar-fill');
    bars.forEach(bar => {
        const finalWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = '1s ease-out';
            bar.style.width = finalWidth;
        }, 100);
    });
}

// Scroll reveal animation for chart cards
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe chart cards
document.querySelectorAll('.chart-card').forEach(card => {
    observer.observe(card);
});

// Observe recommendation cards
document.querySelectorAll('.recommendation-card').forEach(card => {
    observer.observe(card);
});

// Range slider animation
document.querySelectorAll('input[type="range"]').forEach(slider => {
    slider.addEventListener('input', function() {
        const value = (this.value - this.min) / (this.max - this.min) * 100;
        this.style.background = `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${value}%, var(--bg-tertiary) ${value}%, var(--bg-tertiary) 100%)`;
    });
    
    // Initialize on load
    const value = (slider.value - slider.min) / (slider.max - slider.min) * 100;
    slider.style.background = `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${value}%, var(--bg-tertiary) ${value}%, var(--bg-tertiary) 100%)`;
});

// Ripple effect on buttons
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        // Remove previous ripple
        const oldRipple = this.querySelector('.ripple');
        if (oldRipple) oldRipple.remove();

        this.appendChild(ripple);
    });
});

// Add ripple CSS dynamically
const style = document.createElement('style');
style.textContent = `
    button {
        position: relative;
        overflow: hidden;
    }

    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth scroll for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Parallax effect on scroll (subtle)
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    parallaxElements.forEach(element => {
        const speed = element.getAttribute('data-parallax') || 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Fade in on scroll
const fadeInElements = document.querySelectorAll('.section-title, .section-subtitle');
fadeInElements.forEach(el => {
    observer.observe(el);
});

// Export functions for use in other scripts
window.animateScale = animateScale;
window.animateProgressBars = animateProgressBars;
