// Visualization Drawer Toggle Logic
const vizDrawer = document.getElementById('viz-drawer');
const vizToggleBtn = document.getElementById('viz-toggle');

vizToggleBtn.addEventListener('click', () => {
    vizDrawer.classList.toggle('collapsed');
});

// Mode Toggle Logic (2D vs 3D)
const modeOptions = document.querySelectorAll('.mode-option');
const globeFrame = document.getElementById('globe-frame');

modeOptions.forEach(option => {
    option.addEventListener('click', () => {
        // Remove active class from all
        modeOptions.forEach(opt => opt.classList.remove('active'));
        // Add active class to clicked
        option.classList.add('active');
        
        // Switch iframe source
        const mode = option.dataset.mode;
        if (mode === '3d') {
            globeFrame.src = 'assets/globe_population_density.html';
        } else if (mode === '2d') {
            globeFrame.src = 'assets/interactive_population_density.html';
        }
    });
});

// Scrollytelling Animation Logic
// Uses IntersectionObserver to fade in sections as they scroll into view
const observerOptions = {
    root: null, // viewport
    rootMargin: '0px',
    threshold: 0.3 // Trigger when 30% of the section is visible
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            // Optional: Log current phase for debugging or future map triggers
            console.log('Active Section:', entry.target.id);
        } else {
            // Optional: Remove class to fade out when scrolling away
            entry.target.classList.remove('active');
        }
    });
}, observerOptions);

document.querySelectorAll('.story-section').forEach(section => {
    observer.observe(section);
});

// Start with drawer expanded on large screens, collapsed on mobile?
// For now, default is expanded (50% width) as defined in CSS.
if (window.innerWidth < 768) {
    vizDrawer.classList.add('collapsed');
}
