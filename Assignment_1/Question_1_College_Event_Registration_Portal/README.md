# Question 1: College Event Registration Portal (TechNova 2026)

## Overview & Scenario
A responsive, modern web portal designed for an annual National Technical Symposium (**TechNova 2026**). The portal facilitates online registrations, displays multi-track event schedules, showcases technical guidelines, and implements form validation following HTML5 and CSS3 specifications.

---

## Key Features & Requirements Matrix

| Requirement | Implementation Details | File / Location |
|---|---|---|
| **HTML5 Semantic Elements** | `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, `<figure>` | `index.html` |
| **HTML5 Input Types & Forms** | `text`, `email`, `tel`, `date`, `number`, `file`, `radio`, `checkbox`, `select`, `textarea`, `min`, `max`, `pattern`, `required` | Form in `index.html` |
| **Event Schedules** | Multi-day schedule table (`<table>`) with `<caption>`, `<thead>`, `<tbody>`, `<tfoot>`, and `rowspan`/`colspan` cells | Schedule Section in `index.html` |
| **Lists** | Unordered (`<ul>`) and ordered (`<ol>`) category and track hierarchies | Event Tracks in `index.html` |
| **Inline CSS** | Styled global notification bar at the top of the body | `<aside style="...">` in `index.html` |
| **Embedded CSS** | Hero live badge animation (`@keyframes pulseGlow`) and heading utility styles | `<style>` tag in `<head>` |
| **External CSS** | Complete responsive stylesheet utilizing custom properties, Flexbox, CSS Grid, borders, and shadows | `style.css` |
| **CSS Aesthetics** | Colors (HSL/Hex variables), subtle radial background pattern, soft box-shadows, rounded borders | `style.css` |
| **HTTP Process Explanation** | Theoretical and architectural model of the HTTP request/response transaction | Documented below & in `index.html` |
| **WAMP/LAMP Configuration** | Step-by-step instructions for Apache deployment and client-server testing | Documented below |

---

## In-Depth: HTTP Request and Response Process During Registration

When a student fills out the registration form and clicks **Submit Registration**, a complete HTTP client-server transaction takes place:

```
[Web Browser Client]                                 [Apache Web Server (WAMP/LAMP)]
         │                                                            │
         │  1. TCP Handshake (SYN, SYN-ACK, ACK)                      │
         ├───────────────────────────────────────────────────────────►│
         │                                                            │
         │  2. HTTP POST Request (Form Data, Headers, Payload)        │
         ├───────────────────────────────────────────────────────────►│
         │     POST /submit.php HTTP/1.1                              │
         │     Host: localhost                                        │
         │     Content-Type: multipart/form-data; boundary=----xyz    │
         │     Content-Length: 1420                                   │
         │     [Binary/Text Form Payload]                             │
         │                                                            │
         │                                              3. Execution: │
         │                                                 - Parse $_POST
         │                                                 - Save $_FILES
         │                                                 - Database/Receipt
         │                                                            │
         │  4. HTTP Response (Status 200 OK + HTML Receipt)           │
         │◄───────────────────────────────────────────────────────────┤
         │     HTTP/1.1 200 OK                                        │
         │     Content-Type: text/html; charset=UTF-8                 │
         │     Content-Length: 2840                                   │
         │     [Rendered HTML Receipt Body]                           │
         │                                                            │
```

### 1. Request Phase (Client to Server)
- **Method**: `POST` is used rather than `GET` because registration contains sensitive data (email, phone, student ID) and file attachments (`idUpload`), which must be sent in the request body, not appended to the URL query string.
- **Request Headers Sent**:
  - `Host: localhost`
  - `User-Agent: Mozilla/5.0 ...`
  - `Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...`
  - `Content-Length: <byte_count>`
- **Request Body**: Contains boundary-separated key-value pairs (`fullName`, `regNumber`, `email`, `department`, etc.) and multipart binary data for the uploaded ID/abstract file.

### 2. Processing Phase (Server-Side)
- Apache receives the request on port 80 (or 443 for HTTPS) and delegates the script execution to the PHP engine via `mod_php` or `php-fpm`.
- PHP populates superglobals `$_POST` and `$_FILES`.
- Input validation, data sanitization, and registration ID generation occur.

### 3. Response Phase (Server to Client)
- Apache transmits the response header:
  - `HTTP/1.1 200 OK` (Indicating successful processing)
  - `Content-Type: text/html; charset=UTF-8`
  - `Date: ...`
- The response body contains the dynamically generated confirmation receipt (`submit.php`).
- The browser parses the HTML DOM, downloads fonts/CSS, and displays the receipt.

---

## Deployment & Testing Instructions

### Option A: Local Browser Preview (Instant Client-Side Testing)
1. Navigate to the `Question_1_College_Event_Registration_Portal/` directory.
2. Double-click `index.html` to open it directly in any modern browser (Chrome, Edge, Firefox).
3. The page includes an automatic client-side fallback: submitting the form while viewing on `file://` simulates a real-time HTTP POST receipt banner without requiring a server.

### Option B: Python Local Server Testing
Open PowerShell in this directory:
```powershell
python -m http.server 8000
```
Visit: `http://localhost:8000/Question_1_College_Event_Registration_Portal/`

### Option C: WAMP Configuration (Windows)
1. Start WAMP Server (ensure the icon is green).
2. Copy the `Question_1_College_Event_Registration_Portal` folder to `C:\wamp64\www\`.
3. Open your browser and navigate to:
   ```
   http://localhost/Question_1_College_Event_Registration_Portal/
   ```
4. Fill out the form and submit. Apache will execute `submit.php` and return the formatted confirmation receipt.

### Option D: LAMP Configuration (Linux)
1. Start Apache: `sudo systemctl start apache2`
2. Copy folder to web root:
   ```bash
   sudo cp -r Question_1_College_Event_Registration_Portal /var/www/html/
   sudo chown -R www-data:www-data /var/www/html/Question_1_College_Event_Registration_Portal/
   ```
3. Visit: `http://localhost/Question_1_College_Event_Registration_Portal/`
