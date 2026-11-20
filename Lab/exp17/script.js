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

    // 1. Show / Hide Text
    const btnShow = document.getElementById('btnShow');
    const btnHide = document.getElementById('btnHide');
    const secretBox = document.getElementById('secretTextBox');

    btnShow.addEventListener('click', () => {
        secretBox.classList.remove('is-hidden');
    });

    btnHide.addEventListener('click', () => {
        secretBox.classList.add('is-hidden');
    });

    // 2. Hover & Restore Colors
    const squares = document.querySelectorAll('.square-box');
    const hudColor = document.getElementById('hudColor');
    const defaultColor = '#090e17';

    squares.forEach(sq => {
        sq.addEventListener('mouseenter', () => {
            const color = sq.dataset.color;
            const name = sq.dataset.name;
            document.body.style.backgroundColor = color;
            hudColor.textContent = `${name} (${color})`;
        });

        sq.addEventListener('mouseleave', () => {
            document.body.style.backgroundColor = defaultColor;
            hudColor.textContent = `${defaultColor} (Default Restored)`;
        });
    });
});
