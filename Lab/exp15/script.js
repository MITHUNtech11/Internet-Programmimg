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

    // 1. Dynamic Element Creation
    const elTag = document.getElementById('elTag');
    const elContent = document.getElementById('elContent');
    const btnAppend = document.getElementById('btnAppend');
    const btnPrepend = document.getElementById('btnPrepend');
    const btnClearDyn = document.getElementById('btnClearDyn');
    const dynContainer = document.getElementById('dynContainer');

    let counter = 0;

    function createElementNode() {
        counter++;
        const tag = elTag.value;
        const text = elContent.value.trim() || `Generated ${tag.toUpperCase()} Node #${counter}`;

        const el = document.createElement(tag);
        el.className = 'dyn-item';
        el.innerHTML = `<span>&lt;${tag}&gt; ${text}</span> <button style="background:none; border:none; color:#ef4444; cursor:pointer;" onclick="this.parentElement.remove()">&#10005;</button>`;
        return el;
    }

    btnAppend.addEventListener('click', () => {
        const ph = dynContainer.querySelector('.placeholder-text');
        if (ph) ph.remove();
        dynContainer.appendChild(createElementNode());
    });

    btnPrepend.addEventListener('click', () => {
        const ph = dynContainer.querySelector('.placeholder-text');
        if (ph) ph.remove();
        dynContainer.prepend(createElementNode());
    });

    btnClearDyn.addEventListener('click', () => {
        dynContainer.innerHTML = '<span class="placeholder-text">Dynamic container is empty. Append elements above!</span>';
        counter = 0;
    });

    // 2. Traversal Navigation
    let activeNode = document.getElementById('nodeA');
    const activeLabel = document.getElementById('activeNodeLabel');

    function updateActiveNode(newNode) {
        if (!newNode) return;
        if (activeNode) activeNode.classList.remove('focused-node');
        activeNode = newNode;
        activeNode.classList.add('focused-node');
        activeLabel.textContent = `#${activeNode.id || activeNode.tagName.toLowerCase()} (<${activeNode.tagName.toLowerCase()}>)`;
    }

    document.getElementById('tParent').addEventListener('click', () => {
        if (activeNode && activeNode.parentElement && activeNode.id !== 'treeRoot') {
            updateActiveNode(activeNode.parentElement);
        }
    });

    document.getElementById('tFirstChild').addEventListener('click', () => {
        if (activeNode && activeNode.firstElementChild) {
            updateActiveNode(activeNode.firstElementChild);
        }
    });

    document.getElementById('tNextSib').addEventListener('click', () => {
        if (activeNode && activeNode.nextElementSibling) {
            updateActiveNode(activeNode.nextElementSibling);
        }
    });

    document.getElementById('tPrevSib').addEventListener('click', () => {
        if (activeNode && activeNode.previousElementSibling) {
            updateActiveNode(activeNode.previousElementSibling);
        }
    });

    document.getElementById('tResetNode').addEventListener('click', () => {
        updateActiveNode(document.getElementById('nodeA'));
    });

    updateActiveNode(activeNode);
});
