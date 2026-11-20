document.addEventListener('DOMContentLoaded', () => {
    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // Layout switcher
    const modeBtns = document.querySelectorAll('.mode-btn');
    const sandbox = document.getElementById('layoutSandbox');
    const modeLabel = document.getElementById('currentModeLabel');
    const simWidth = document.getElementById('simWidth');

    modeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modeBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const mode = btn.dataset.mode;

            sandbox.className = `layout-sandbox mode-${mode}`;
            if (mode === 'fixed') {
                modeLabel.textContent = 'Fixed (960px Width)';
                simWidth.textContent = '960px (Scrollable on small displays)';
            } else if (mode === 'fluid') {
                modeLabel.textContent = 'Fluid (Percentage Scaled)';
                simWidth.textContent = '98% Relative Width';
            } else {
                modeLabel.textContent = 'Responsive (Flexbox & CSS Grid)';
                simWidth.textContent = 'Auto / Fluid Breakpoints';
            }
        });
    });
});
