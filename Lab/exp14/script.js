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

    // 1. Color Squares
    const squares = document.querySelectorAll('.color-square');
    const toneLabel = document.getElementById('currentToneLabel');
    const defaultColor = '#090e17';

    squares.forEach(sq => {
        sq.addEventListener('mouseenter', () => {
            const c = sq.dataset.color;
            const l = sq.dataset.label;
            document.body.style.backgroundColor = c;
            toneLabel.textContent = `${l} (${c})`;
        });

        sq.addEventListener('mouseleave', () => {
            document.body.style.backgroundColor = defaultColor;
            toneLabel.textContent = `Default Dark (${defaultColor})`;
        });
    });

    // 2. Shake Effect
    const btnShake = document.getElementById('btnShake');
    const btnStopShake = document.getElementById('btnStopShake');
    const shakeWrapper = document.getElementById('shakeWrapper');
    const shakeBadge = document.getElementById('shakeBadge');

    btnShake.addEventListener('click', () => {
        shakeWrapper.classList.add('is-shaking');
        shakeBadge.textContent = 'Status: SHAKING ACTIVE';
        shakeBadge.classList.add('active-shake');
    });

    btnStopShake.addEventListener('click', () => {
        shakeWrapper.classList.remove('is-shaking');
        shakeBadge.textContent = 'Status: STABLE';
        shakeBadge.classList.remove('active-shake');
    });
});
