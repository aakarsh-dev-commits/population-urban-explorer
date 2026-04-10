// Visualization Drawer Toggle Logic
const vizDrawer = document.getElementById('viz-drawer');
const vizToggleBtn = document.getElementById('viz-toggle');

vizToggleBtn.addEventListener('click', () => {
    vizDrawer.classList.toggle('collapsed');
});

// State Matrix Logic
let currentModel = 'density';
let currentMode = '3d';

const fileMap = {
    'density': {
        '3d': 'assets/globe_population_density.html',
        '2d': 'assets/interactive_population_density.html'
    },
    'hotspots': {
        '3d': 'assets/globe_hotspots.html',
        '2d': 'assets/interactive_hotspots.html'
    },
    'clusters': {
        '3d': 'assets/globe_clusters.html',
        '2d': 'assets/interactive_clusters.html'
    },
    'idw': {
        '3d': 'assets/interactive_idw_surface.html',
        '2d': 'assets/interactive_idw_surface.html'
    }
};

const globeFrame = document.getElementById('globe-frame');

function updateViz() {
    const src = fileMap[currentModel][currentMode];
    if(globeFrame.src !== new URL(src, document.baseURI).href) {
        globeFrame.src = src;
    }
}

// Mode Toggle Logic (2D vs 3D) Left
const modeOptions = document.querySelectorAll('.mode-option');
modeOptions.forEach(option => {
    option.addEventListener('click', () => {
        modeOptions.forEach(opt => opt.classList.remove('active'));
        option.classList.add('active');
        currentMode = option.dataset.mode;
        updateViz();
    });
});

// Model Toggle Logic (Top Nav)
const topTabs = document.querySelectorAll('.top-tab');
topTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        topTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentModel = tab.dataset.model;
        updateViz();
    });
});

// Scrollytelling Animation Logic
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.3
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        } else {
            entry.target.classList.remove('active');
        }
    });
}, observerOptions);

document.querySelectorAll('.story-section').forEach(section => {
    observer.observe(section);
});

// Default drawer behavior
if (window.innerWidth < 768) {
    vizDrawer.classList.add('collapsed');
}
