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

    const para = document.getElementById('targetParagraph');
    const btnTheme = document.getElementById('btnTheme');
    const btnFontSize = document.getElementById('btnFontSize');
    const btnFontFamily = document.getElementById('btnFontFamily');
    const btnHighlightAll = document.getElementById('btnHighlightAll');
    const btnReset = document.getElementById('btnReset');

    const statFontSize = document.getElementById('statFontSize');
    const statFontFamily = document.getElementById('statFontFamily');
    const statColor = document.getElementById('statColor');
    const statBg = document.getElementById('statBg');

    const tooltip = document.getElementById('wordTooltip');
    const tooltipTerm = document.getElementById('tooltipTerm');
    const tooltipDef = document.getElementById('tooltipDef');

    let sizeStep = 0; // 0: normal, 1: large, 2: xlarge
    let fontStep = 0; // 0: sans, 1: mono, 2: serif

    function updateHud() {
        const cs = window.getComputedStyle(para);
        statFontSize.textContent = cs.fontSize;
        statFontFamily.textContent = cs.fontFamily.split(',')[0];
        statColor.textContent = cs.color;
        statBg.textContent = cs.backgroundColor;
    }

    // Toggle Theme
    btnTheme.addEventListener('click', () => {
        para.classList.toggle('theme-light');
        updateHud();
    });

    // Cycle Font Size
    btnFontSize.addEventListener('click', () => {
        sizeStep = (sizeStep + 1) % 3;
        para.classList.remove('font-large', 'font-xlarge');
        if (sizeStep === 1) para.classList.add('font-large');
        if (sizeStep === 2) para.classList.add('font-xlarge');
        updateHud();
    });

    // Cycle Font Family
    btnFontFamily.addEventListener('click', () => {
        fontStep = (fontStep + 1) % 3;
        para.classList.remove('font-mono', 'font-serif');
        if (fontStep === 1) para.classList.add('font-mono');
        if (fontStep === 2) para.classList.add('font-serif');
        updateHud();
    });

    // Toggle Highlight All
    let allHighlighted = false;
    btnHighlightAll.addEventListener('click', () => {
        allHighlighted = !allHighlighted;
        document.querySelectorAll('.highlight-word').forEach(w => {
            if (allHighlighted) w.classList.add('forced-highlight');
            else w.classList.remove('forced-highlight');
        });
        btnHighlightAll.textContent = allHighlighted ? 'Remove Highlights' : 'Highlight All Core Terms';
    });

    // Reset All
    btnReset.addEventListener('click', () => {
        para.className = 'target-para default-style';
        sizeStep = 0;
        fontStep = 0;
        allHighlighted = false;
        document.querySelectorAll('.highlight-word').forEach(w => w.classList.remove('forced-highlight'));
        btnHighlightAll.textContent = 'Highlight All Core Terms';
        updateHud();
    });

    // Word Hover Listeners
    document.querySelectorAll('.highlight-word').forEach(word => {
        word.addEventListener('mouseenter', (e) => {
            const rect = e.target.getBoundingClientRect();
            tooltipTerm.textContent = e.target.textContent;
            tooltipDef.textContent = e.target.dataset.definition;
            tooltip.style.left = `${rect.left + window.scrollX}px`;
            tooltip.style.top = `${rect.top + window.scrollY - 55}px`;
            tooltip.classList.remove('hidden');
        });

        word.addEventListener('mouseleave', () => {
            tooltip.classList.add('hidden');
        });
    });

    updateHud();
});
