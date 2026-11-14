# Question 2: Smart Campus Facility Booking Website

## Overview & Scenario
A centralized campus facility booking and resource management portal for engineering colleges and universities. Faculty members and department administrators can inspect venue specifications, review real-time availability across morning/afternoon/evening slots, allocate venues dynamically via an interactive HTML5 Drag-and-Drop scheduling board, and submit official reservation requisitions.

---

## Requirements & Implementation Matrix

| Requirement | Implementation Details | File / Location |
|---|---|---|
| **HTML5 Booking Forms & Controls** | `text`, `email`, `date`, `number`, `select`, `checkbox`, `textarea`, `min`, `max`, `pattern`, `required` | Booking Form in `index.html` |
| **Facility Availability Tables** | Structured matrix with column slots and color-coded status badges (`Available`, `Booked`, `Maintenance`) | Availability Grid in `index.html` |
| **Facility Images** | Responsive, high-resolution inline SVG architectural diagrams (Auditorium, AI HPC Lab, Senate Boardroom) | Facility Cards in `index.html` |
| **Semantic HTML5 Elements** | `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<figure>` | `index.html` |
| **CSS3 Animations & Transitions** | `@keyframes fadeInDown`, `@keyframes fadeInUp`, cubic-bezier hover transitions, elevation transforms | `style.css` |
| **CSS3 Shadows & Elevation** | Multi-layer elevation box-shadows (`--shadow-sm`, `--shadow-md`, `--shadow-lg`) | `style.css` |
| **HTML5 Drag-and-Drop Room Allocation** | Native HTML5 Drag and Drop API (`draggable="true"`, `dragstart`, `dragover`, `drop`, `dataTransfer`) | `drag_drop.js` |
| **WAMP/LAMP Configuration** | Setup instructions for Apache web server with PHP request processing | Documented below & `book.php` |

---

## Technical Architecture: HTML5 Drag-and-Drop API

The interactive room allocation board uses the native **HTML5 Drag and Drop specification** without requiring heavy external JavaScript libraries:

```
[Draggable Element]                   [User Event]                  [Drop Target Zone]
        │                                  │                                │
        │  1. dragstart                    │                                │
        ├─────────────────────────────────►│                                │
        │     - Sets 'dragging' class      │                                │
        │     - e.dataTransfer.setData()   │                                │
        │                                  │                                │
        │                                  │  2. dragover                   │
        │                                  ├───────────────────────────────►│
        │                                  │     - e.preventDefault()       │
        │                                  │     - Sets 'drag-over' class   │
        │                                  │                                │
        │                                  │  3. drop                       │
        │                                  ├───────────────────────────────►│
        │                                  │     - e.preventDefault()       │
        │                                  │     - e.dataTransfer.getData() │
        │                                  │     - zone.appendChild(item)   │
        │                                  │     - Display toast feedback   │
```

### Event Lifecycle Implementation in `drag_drop.js`:
1. **`dragstart`**: Attached to `.draggable-item`. Injects the venue identifier into `dataTransfer.setData('text/plain', item.id)` and sets `effectAllowed = 'move'`.
2. **`dragover`**: Attached to `.drop-zone`. Calls `e.preventDefault()`, which is **mandatory** under the W3C spec to signal that a drop is permitted.
3. **`dragenter` & `dragleave`**: Toggles visual styling (`drag-over` class) to indicate an active drop boundary.
4. **`drop`**: Extracts the source node ID using `e.dataTransfer.getData('text/plain')`, appends the child node into the targeted schedule time-slot, hides placeholder messaging, and triggers a confirmation notification toast.
5. **Reset & Bi-directional Drag**: Allows dragged items to be dragged back to the unallocated pool or reset en masse.

---

## Testing & Server Configuration

### 1. Direct Browser Client Preview
Double-click `index.html` to open directly in Google Chrome, Microsoft Edge, or Mozilla Firefox. You can test:
- Interactive Drag and Drop room allocation between slots.
- Real-time form validation constraints (dates, employee IDs, attendees).
- Responsive mobile/desktop transitions and CSS keyframes.

### 2. Local Python Server
```powershell
python -m http.server 8000
# Visit: http://localhost:8000/Question_2_Smart_Campus_Facility_Booking/
```

### 3. WAMP Server Configuration (Windows)
1. Copy the `Question_2_Smart_Campus_Facility_Booking` directory into:
   ```
   C:\wamp64\www\Question_2_Smart_Campus_Facility_Booking
   ```
2. Open your web browser and navigate to:
   ```
   http://localhost/Question_2_Smart_Campus_Facility_Booking/
   ```
3. Submit a facility requisition form to test the Apache PHP handler (`book.php`).

### 4. LAMP Server Configuration (Linux)
```bash
sudo cp -r Question_2_Smart_Campus_Facility_Booking /var/www/html/
sudo systemctl restart apache2
# Visit: http://localhost/Question_2_Smart_Campus_Facility_Booking/
```
