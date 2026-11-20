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

    // Mobile Hamburger
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    menuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });

    // Viewport HUD
    const hudWidth = document.getElementById('hudWidth');
    const hudBp = document.getElementById('hudBp');

    function updateHud() {
        const width = window.innerWidth;
        hudWidth.textContent = `${width}px`;
        if (width < 480) {
            hudBp.textContent = 'Mobile (<480px)';
        } else if (width <= 768) {
            hudBp.textContent = 'Tablet (481px - 768px)';
        } else if (width <= 1024) {
            hudBp.textContent = 'Laptop (769px - 1024px)';
        } else {
            hudBp.textContent = 'Desktop (>1024px)';
        }
    }

    window.addEventListener('resize', updateHud);
    updateHud();
});
