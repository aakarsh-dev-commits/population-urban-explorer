function switchView(viewType) {
    const container = document.getElementById('visual-container');
    const descText = document.getElementById('view-description');
    
    // Reset buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Set active button
    const activeBtn = document.querySelector(`.nav-btn[data-view="${viewType}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    // Update Content
    let content = '';
    let description = '';

    switch(viewType) {
        case 'static':
            content = '<img src="assets/static_population_density.png" alt="Static Map" class="visual-content" style="padding: 2rem;">';
            description = 'High-resolution static choropleth map generated with Matplotlib. Suitable for publication and printing.';
            break;
        case 'interactive':
            content = '<iframe src="assets/interactive_population_density.html" frameborder="0" class="visual-content"></iframe>';
            description = 'Interactive 2D map powered by Plotly. Hover over countries to see detailed population metrics.';
            break;
        case 'globe':
            content = '<iframe src="assets/globe_population_density.html" frameborder="0" class="visual-content"></iframe>';
            description = 'Immersive 3D orthographic globe view. Rotate and explore global density patterns in a realistic projection.';
            break;
    }

    // Smooth transition
    container.style.opacity = 0;
    setTimeout(() => {
        container.innerHTML = content;
        descText.textContent = description;
        container.style.opacity = 1;
    }, 200);
}

// Ensure globe loads by default if iframe caching issues occur
document.addEventListener("DOMContentLoaded", () => {
    // Already set in HTML, but good for safety
    // switchView('globe'); 
});
