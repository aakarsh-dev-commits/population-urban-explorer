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

// Map each model tab to the section it should scroll to
const tabSectionMap = {
    'density':  'hero',
    'hotspots': 'phase2',
    'clusters': 'phase3',
    'idw':      'phase4'
};

const storyScroller = document.getElementById('story-scroller');

topTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        topTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentModel = tab.dataset.model;
        updateViz();

        // Scroll the left panel to the matching section
        const targetId = tabSectionMap[currentModel];
        const targetEl = targetId ? document.getElementById(targetId) : null;
        if (targetEl && storyScroller) {
            isTabScrolling = true;
            storyScroller.scrollTo({
                top: targetEl.offsetTop,
                behavior: 'smooth'
            });
            // Re-enable scroll observer after animation completes (~700ms)
            setTimeout(() => { isTabScrolling = false; }, 700);
        }
    });
});

// ─── Scroll-driven visualization sync ───────────────────────────────────────
// Map each section to the model it represents. Sections not listed keep the
// current model (e.g. phase5, future, footer).
const sectionModelMap = {
    'hero':   'density',
    'problem':'density',
    'solution':'density',
    'phase1': 'density',
    'phase2': 'hotspots',
    'phase3': 'clusters',
    'phase4': 'idw',
    'phase5': 'idw',
    'future': 'idw'
};

// Flag to suppress scroll-driven updates while a tab click is animating
let isTabScrolling = false;

function setActiveModel(model) {
    if (model === currentModel) return;
    currentModel = model;
    updateViz();

    // Sync the top-nav highlight
    topTabs.forEach(t => {
        t.classList.toggle('active', t.dataset.model === model);
    });
}

// Use the story scroller as the IntersectionObserver root so it fires
// relative to the visible scroll area, not the whole viewport.
const scrollObserverOptions = {
    root: storyScroller,
    rootMargin: '-40% 0px -40% 0px',  // trigger when section is roughly centred
    threshold: 0
};

const scrollObserver = new IntersectionObserver((entries) => {
    if (isTabScrolling) return;  // ignore during programmatic scrolls
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            const model = sectionModelMap[entry.target.id];
            if (model) setActiveModel(model);
        } else {
            entry.target.classList.remove('active');
        }
    });
}, scrollObserverOptions);

document.querySelectorAll('.story-section').forEach(section => {
    scrollObserver.observe(section);
});

// ─── Default drawer behaviour ────────────────────────────────────────────────
if (window.innerWidth < 768) {
    vizDrawer.classList.add('collapsed');
}
