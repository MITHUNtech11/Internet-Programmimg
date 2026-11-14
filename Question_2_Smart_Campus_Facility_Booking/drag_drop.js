/**
 * Smart Campus Facility Allocation - HTML5 Drag and Drop Implementation
 * Demonstrates: dragstart, dragend, dragover, dragenter, dragleave, drop events
 * using native DataTransfer object.
 */

document.addEventListener('DOMContentLoaded', () => {
  const draggables = document.querySelectorAll('.draggable-item');
  const dropZones = document.querySelectorAll('.drop-zone');
  const venuePool = document.getElementById('venuePool');
  const resetBtn = document.getElementById('resetDndBtn');
  const sourceCount = document.getElementById('sourceCount');
  const toast = document.getElementById('dndStatusToast');

  // Update count of items remaining in the unallocated pool
  function updatePoolCount() {
    const remaining = venuePool.querySelectorAll('.draggable-item').length;
    sourceCount.textContent = `${remaining} Available`;
  }

  // Display status feedback toast
  function showToast(message) {
    toast.textContent = message;
    toast.style.display = 'block';
    setTimeout(() => {
      toast.style.display = 'none';
    }, 3500);
  }

  // Attach event listeners to all draggable items
  draggables.forEach(item => {
    item.addEventListener('dragstart', (e) => {
      item.classList.add('dragging');
      // Store the element's id and readable name in the dataTransfer payload
      e.dataTransfer.setData('text/plain', item.id);
      e.dataTransfer.effectAllowed = 'move';
    });

    item.addEventListener('dragend', () => {
      item.classList.remove('dragging');
      updatePoolCount();
    });
  });

  // Attach event listeners to drop zones
  dropZones.forEach(zone => {
    zone.addEventListener('dragover', (e) => {
      e.preventDefault(); // Necessary to allow dropping
      e.dataTransfer.dropEffect = 'move';
      zone.classList.add('drag-over');
    });

    zone.addEventListener('dragenter', (e) => {
      e.preventDefault();
      zone.classList.add('drag-over');
    });

    zone.addEventListener('dragleave', () => {
      zone.classList.remove('drag-over');
    });

    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('drag-over');

      const itemId = e.dataTransfer.getData('text/plain');
      const draggedElement = document.getElementById(itemId);

      if (draggedElement) {
        // If the zone already contains an allocated item, return the old one to the pool
        const existingItem = zone.querySelector('.draggable-item');
        if (existingItem) {
          venuePool.appendChild(existingItem);
        }

        // Hide placeholder text in this zone
        const placeholder = zone.querySelector('.drop-placeholder');
        if (placeholder) {
          placeholder.style.display = 'none';
        }

        // Append the new dragged element into this slot
        zone.appendChild(draggedElement);

        const slotName = zone.closest('.drop-target-slot').dataset.slot;
        const venueName = draggedElement.dataset.venue;
        showToast(`✓ Successfully Allocated: "${venueName}" to ${slotName}`);
        updatePoolCount();
      }
    });
  });

  // Also allow dragging an item back to the main pool
  venuePool.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    venuePool.classList.add('drag-over');
  });

  venuePool.addEventListener('dragleave', () => {
    venuePool.classList.remove('drag-over');
  });

  venuePool.addEventListener('drop', (e) => {
    e.preventDefault();
    venuePool.classList.remove('drag-over');
    const itemId = e.dataTransfer.getData('text/plain');
    const draggedElement = document.getElementById(itemId);

    if (draggedElement) {
      venuePool.appendChild(draggedElement);
      // Check all drop zones to restore placeholder if empty
      dropZones.forEach(zone => {
        if (!zone.querySelector('.draggable-item')) {
          const placeholder = zone.querySelector('.drop-placeholder');
          if (placeholder) placeholder.style.display = 'inline';
        }
      });
      showToast(`Returned venue back to unallocated pool.`);
      updatePoolCount();
    }
  });

  // Reset button: moves all draggable items back to venuePool
  resetBtn.addEventListener('click', () => {
    draggables.forEach(item => {
      venuePool.appendChild(item);
    });

    dropZones.forEach(zone => {
      const placeholder = zone.querySelector('.drop-placeholder');
      if (placeholder) {
        placeholder.style.display = 'inline';
      }
    });

    showToast('All facility allocations have been reset to the pool.');
    updatePoolCount();
  });
});
