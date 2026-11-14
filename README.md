# Internet Programming - Assignment 1 (CO1)

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)
![WAMP / LAMP](https://img.shields.io/badge/Server-WAMP%20%2F%20LAMP-00758F?style=for-the-badge&logo=apache&logoColor=white)

Comprehensive, production-ready solutions for **Assignment 1 (Course Outcome 1)** of the **Internet Programming** laboratory curriculum based on the official assignment prompt: [`Assignment1_CO1.pdf`](Assignment1_CO1.pdf).

---

## Course Outcome 1 (CO1) Competencies Mastered

- **Semantic HTML5 & Form Architecture**: Use of semantic elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`), custom tables (`<thead>`, `<tbody>`, `rowspan`, `colspan`), structured lists (`<ul>`, `<ol>`), and modern HTML5 form validation controls.
- **Modern CSS3 Engineering**: Handcrafted Vanilla CSS3 without bulky frameworks, implementing CSS Variables, Flexbox, CSS Grid, keyframe animations, cubic-bezier transitions, 3D perspective transforms, gradient border-images, text glow effects, and deep elevation shadows.
- **CSS Cascading & Inheritance**: Rigorous demonstration of inheritance rules, the `inherit` keyword, and specificity weight calculations ($(a, b, c, d)$ tuple resolution).
- **Native Browser APIs**: HTML5 Drag and Drop API implementation with custom `dataTransfer` payload management and drop target state tracking.
- **Client-Server Communication & HTTP Protocol**: In-depth theoretical models covering DNS lookups, TCP 3-way handshakes, HTTP request methods (`GET`, `POST`, `PUT`, `DELETE`), header mechanics, status code families (1xx through 5xx), and WAMP/LAMP server configuration.

---

## Repository Project Directory & Solutions Index

Each question is maintained as an independent, fully self-contained web application with its own dedicated markup, styling, client scripts, optional PHP backend handlers, and architectural technical documentation:

| Folder / Project | Theme & Scenario | Key Technical Highlights |
|---|---|---|
| 📂 [**Question 1: College Event Registration Portal**](Question_1_College_Event_Registration_Portal/) | Technical Symposium (**TechNova 2026**) | Form controls, event schedule tables, inline/embedded/external CSS demonstration, HTTP request/response cycle breakdown, `submit.php`. |
| 📂 [**Question 2: Smart Campus Facility Booking**](Question_2_Smart_Campus_Facility_Booking/) | Venue Reservation (**SmartCampus**) | Real-time availability table, vector facility art, CSS3 animations, **native HTML5 Drag and Drop** room scheduling allocator, `book.php`. |
| 📂 [**Question 3: Online Sports Tournament Management**](Question_3_Online_Sports_Tournament/) | Athletic Championship (**Olympus Cup 2026**) | Fixture schedules with live score indicators, team insignia, **CSS3 3D perspective tilt transforms**, client-server communication analysis, `register.php`. |
| 📂 [**Question 4: E-Commerce Product Showcase**](Question_4_Ecommerce_Product_Showcase/) | Consumer Electronics Retail (**NexTech**) | Product cards with hover lift animations, specification comparison matrix, **demonstration of CSS cascading & inheritance**, `enquire.php`. |
| 📂 [**Question 5: Online Travel and Tourism Website**](Question_5_Online_Travel_Tourism/) | Curated International Tours (**WanderLust**) | Destination showcase, multi-tier package comparison table with gradient border-image, **comprehensive HTTP architecture guide**, `booking.php`. |

---

## Technical Comparison Matrix Across All 5 Projects

| Feature / Standard | Question 1 | Question 2 | Question 3 | Question 4 | Question 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| **Semantic HTML5 Layout** | Yes | Yes | Yes | Yes | Yes |
| **HTML5 Form Validation** | Yes | Yes | Yes | Yes | Yes |
| **Data Tables with Semantics** | Schedule Matrix | Availability Grid | Fixture Table | Specs Matrix | Package Comparison |
| **Structured Lists (`<ul>`, `<ol>`)** | Tracks & Events | Amenities | Categories | Categories | Inclusions |
| **Vector Graphics (Inline SVG)** | Yes | Yes | Yes | Yes | Yes |
| **CSS3 Animations / Keyframes** | Yes (`pulseGlow`) | Yes (`fadeInUp`) | Yes (`pulseLive`) | Yes (`cardHover`) | Yes (`floatSun`) |
| **Specialized CSS3 Feature** | Inline/Embedded/Ext | Elevation Shadows | 3D Perspective Tilt | Border-Image & Cascade | Gradient Overlays |
| **Interactive JavaScript** | Validation Fallback | HTML5 Drag & Drop | Fixture Category Filter | Spec Preselect | Booking Intercept |
| **WAMP / LAMP PHP Handler** | `submit.php` | `book.php` | `register.php` | `enquire.php` | `booking.php` |
| **Client-Server / HTTP Theory** | Request/Response Flow | Drag-Drop & Server | 6-Stage TCP/HTTP | Cascade Specificity | HTTP Methods & Codes |

---

## Quickstart & Local Execution Guide

### Option 1: Standalone Browser Preview (Zero Installation)
All projects are built to execute directly in any modern web browser without needing any server or internet connection:
1. Navigate into any project directory (e.g. `Question_1_College_Event_Registration_Portal/`).
2. Double-click `index.html`.
3. Test responsive views, form interactions, and animations directly.

### Option 2: Local Python Server Testing
To serve all projects over HTTP locally:
```powershell
# Open terminal in the root repository directory
python -m http.server 8000
```
Open your browser and navigate to:
- `http://localhost:8000/Question_1_College_Event_Registration_Portal/`
- `http://localhost:8000/Question_2_Smart_Campus_Facility_Booking/`
- `http://localhost:8000/Question_3_Online_Sports_Tournament/`
- `http://localhost:8000/Question_4_Ecommerce_Product_Showcase/`
- `http://localhost:8000/Question_5_Online_Travel_Tourism/`

### Option 3: Deploying on WAMP Server (Windows)
1. Ensure WAMP Server is running (Apache service active).
2. Copy the entire repository folder into your WAMP web root:
   ```powershell
   Copy-Item -Recurse -Path . -Destination "C:\wamp64\www\Internet_Programming_Assignment1"
   ```
3. Open your browser and navigate to:
   ```
   http://localhost/Internet_Programming_Assignment1/Question_1_College_Event_Registration_Portal/
   ```
4. Submitting any form will now dispatch HTTP POST requests to the live PHP handlers (`submit.php`, `book.php`, `register.php`, `enquire.php`, `booking.php`).

### Option 4: Deploying on LAMP Server (Linux / Ubuntu)
```bash
# Clone or copy repository into Apache web directory
sudo cp -r . /var/www/html/Internet_Programming_Assignment1
sudo chown -R www-data:www-data /var/www/html/Internet_Programming_Assignment1
sudo systemctl restart apache2
```
Visit: `http://localhost/Internet_Programming_Assignment1/`

---

## Academic Integrity & Standards
- Handcrafted vanilla code written specifically for the Internet Programming curriculum.
- No bulky third-party frontend frameworks (React, Vue, Tailwind, Bootstrap) required; proves foundational command of HTML5, CSS3, and core client-server principles.
- 100% self-contained inline SVG illustrations ensure all visual assets render cleanly offline and on GitHub Pages.
