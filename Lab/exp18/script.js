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

    // 1. Image Click Toggle
    const imgCard = document.getElementById('imageToggleCard');
    const imgA = document.getElementById('imageStateA');
    const imgB = document.getElementById('imageStateB');
    const activeLabel = document.getElementById('activeImgLabel');
    const toggleCount = document.getElementById('toggleCount');

    let isStateA = true;
    let count = 0;

    imgCard.addEventListener('click', () => {
        isStateA = !isStateA;
        count++;
        toggleCount.textContent = count;

        if (isStateA) {
            imgA.className = 'toggle-img active';
            imgB.className = 'toggle-img hidden';
            activeLabel.textContent = 'Mode A (Daylight Horizon)';
        } else {
            imgA.className = 'toggle-img hidden';
            imgB.className = 'toggle-img active';
            activeLabel.textContent = 'Mode B (Deep Space Night)';
        }
    });

    // 2. Text Hover Status Tracker
    const hover1 = document.getElementById('hoverText1');
    const hover2 = document.getElementById('hoverText2');
    const hoverStatus = document.getElementById('hoverStatus');

    hover1.addEventListener('mouseenter', () => {
        hoverStatus.textContent = 'Active: Neon Glow Effect (Item #1 Hovered)';
        hoverStatus.style.color = '#38bdf8';
    });
    hover1.addEventListener('mouseleave', () => {
        hoverStatus.textContent = 'Awaiting cursor hover event...';
        hoverStatus.style.color = '';
    });

    hover2.addEventListener('mouseenter', () => {
        hoverStatus.textContent = 'Active: Typographic Oblique Tilt (Item #2 Hovered)';
        hoverStatus.style.color = '#f59e0b';
    });
    hover2.addEventListener('mouseleave', () => {
        hoverStatus.textContent = 'Awaiting cursor hover event...';
        hoverStatus.style.color = '';
    });
});
