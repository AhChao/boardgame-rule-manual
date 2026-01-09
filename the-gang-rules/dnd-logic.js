let draggedElement = null;
let offset = { x: 0, y: 0 };
let currentTarget = null;

export function setupDraggable(element, onDrop, onCancel) {
    element.addEventListener('pointerdown', startDrag);

    function startDrag(e) {
        if(e.button !== 0 && e.pointerType === 'mouse') return;

        draggedElement = element;
        const rect = element.getBoundingClientRect();

        // Store original parent and position
        const originalParent = element.parentElement;
        const originalRect = rect;

        offset.x = e.clientX - rect.left;
        offset.y = e.clientY - rect.top;

        element.style.position = 'fixed';
        element.style.width = `${rect.width}px`;
        element.style.height = `${rect.height}px`;
        element.style.zIndex = '1000';
        element.style.transform = 'none'; // Clear stacking transforms
        element.style.pointerEvents = 'none'; // Allow target detection

        updatePosition(e);

        window.addEventListener('pointermove', moveDrag);
        window.addEventListener('pointerup', stopDrag);

        document.querySelectorAll('.drop-zone').forEach(zone => {
            zone.classList.add('can-drop');
        });
    }

    function moveDrag(e) {
        if(!draggedElement) return;
        updatePosition(e);

        // Simple hit detection for discard zone
        const target = document.elementFromPoint(e.clientX, e.clientY);
        const zone = target?.closest('.drop-zone');

        if(currentTarget) currentTarget.classList.remove('drag-over');
        if(zone) {
            zone.classList.add('drag-over');
            currentTarget = zone;
        } else {
            currentTarget = null;
        }
    }

    function stopDrag(e) {
        if(!draggedElement) return;

        const zone = currentTarget;

        window.removeEventListener('pointermove', moveDrag);
        window.removeEventListener('pointerup', stopDrag);

        if(zone) {
            onDrop(draggedElement, zone);
        } else {
            // Snap back
            draggedElement.style.position = '';
            draggedElement.style.width = '';
            draggedElement.style.height = '';
            draggedElement.style.zIndex = '';
            draggedElement.style.transform = '';
            draggedElement.style.pointerEvents = '';
            draggedElement.style.top = '';
            draggedElement.style.left = '';

            if(onCancel) onCancel(draggedElement);
        }

        document.querySelectorAll('.drop-zone').forEach(zone => {
            zone.classList.remove('can-drop', 'drag-over');
        });

        draggedElement = null;
        currentTarget = null;
    }

    function updatePosition(e) {
        draggedElement.style.left = `${e.clientX - offset.x}px`;
        draggedElement.style.top = `${e.clientY - offset.y}px`;
    }
}
