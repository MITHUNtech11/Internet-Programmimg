# Question 3: Online Sports Tournament Management Website (Olympus Cup 2026)

## Overview & Scenario
An inter-collegiate sports tournament management portal designed for athletic departments, team managers, and student competitors. The system showcases competition schedules, match results with live score indicators, hierarchical sports categories, 3D interactive team contender cards with custom team insignia, and an official squad registration form.

---

## Requirements & Implementation Matrix

| Requirement | Implementation Details | File / Location |
|---|---|---|
| **Tournament Schedules in Tables** | Filterable schedule table (`<table>`) with Match ID, sport tags, matchup, venue, and live status badges | Schedules Section in `index.html` |
| **Sports Categories in Lists** | Semantic unordered (`<ul>`) and ordered (`<ol>`) lists detailing Outdoor Athletics and Indoor Racquet sports | Categories in `index.html` |
| **Team Registration Form** | Comprehensive team entry form with discipline, division, captain contacts, jersey color picker, and roster input | Form in `index.html` |
| **Team Logos & Sports Images** | High-definition inline SVG vector logos (Royal Lions, Titan Strikers, Cyber Hawks, Thunderbolts) and sports hero graphics | `index.html` |
| **CSS3 Transformations & 3D** | `perspective: 1200px`, `transform-style: preserve-3d`, `rotateY(12deg) rotateX(4deg)` 3D card tilt effects | `style.css` |
| **Transitions & Animations** | Cubic-bezier transition curves, `@keyframes pulseLive` for live score badges, hover elevations | `style.css` |
| **Semantic HTML5 Elements** | `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>` | `index.html` |
| **Client-Server Process Explanation** | End-to-end walkthrough of DNS, TCP handshake, HTTP request/response, and DOM rendering | Documented below & in `index.html` |

---

## Deep-Dive: Client-Server Communication Process in Web Applications

The interaction between the user's web browser (client) and the tournament hosting server (Apache/PHP) follows a structured six-stage communication lifecycle:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CLIENT-SERVER ARCHITECTURE                      │
└────────────────────────────────────────────────────────────────────────┘

  [1. USER ACTION] ──► User enters URL: http://localhost/register.php
          │
          ▼
  [2. DNS RESOLUTION] ──► Browser checks:
          │                  - Browser DNS Cache
          │                  - OS Hosts File (127.0.0.1 localhost)
          │                  - Recursive DNS Server
          │
          ▼
  [3. TCP 3-WAY HANDSHAKE] (Transport Layer)
          │     Client ──────── SYN (Seq=X) ────────► Server
          │     Client ◄── SYN-ACK (Seq=Y, Ack=X+1) ─ Server
          │     Client ──────── ACK (Ack=Y+1) ──────► Server
          │
          ▼
  [4. HTTP POST REQUEST TRANSMISSION] (Application Layer)
          │     POST /register.php HTTP/1.1
          │     Host: localhost
          │     Content-Type: application/x-www-form-urlencoded
          │     teamName=Royal+Lions&captain=Rohit...
          │
          ▼
  [5. SERVER-SIDE PROCESSING (WAMP/LAMP)]
          │     - Apache accepts TCP socket on Port 80
          │     - mod_php processes script execution
          │     - Sanitizes input, issues entry pass
          │
          ▼
  [6. HTTP RESPONSE & BROWSER RENDERING]
          │     Server ── HTTP/1.1 200 OK (Content-Type: text/html) ──► Client
          │     Browser: HTML Parsing ➔ DOM Tree ➔ CSSOM ➔ Render Tree ➔ Paint
```

### Stage 1: URL Parsing and DNS Resolution
When the client initiates a request (e.g., navigating to the sports portal or submitting a form), the browser extracts the protocol (`http`), host (`localhost`), and resource path (`/register.php`). The hostname is resolved to an IP address (`127.0.0.1` locally) via DNS lookups.

### Stage 2: TCP Handshake Establishment
Before HTTP data can travel, a reliable Transmission Control Protocol (TCP) stream must be opened:
1. **SYN**: Client sends Synchronize packet with initial sequence number $X$.
2. **SYN-ACK**: Server acknowledges with $Ack = X + 1$ and sends its own sequence number $Y$.
3. **ACK**: Client acknowledges with $Ack = Y + 1$. Connection is now established.

### Stage 3: HTTP Request Formulation
The browser serializes the team registration form fields into standard HTTP format:
- **Request Line**: `POST /register.php HTTP/1.1`
- **Request Headers**: `Host`, `User-Agent`, `Accept`, `Content-Type`, `Content-Length`.
- **Message Body**: URL-encoded key-value pairs representing team name, sport category, captain details, and roster.

### Stage 4: Apache Web Server Execution
The web server (Apache in WAMP or LAMP) identifies the requested file as a `.php` script, directs it to the Zend Engine interpreter, initializes the `$_POST` array, and dynamically builds an HTML response document.

### Stage 5: HTTP Response Delivery
The server responds with an HTTP status code:
- `HTTP/1.1 200 OK`: Successful submission and confirmation.
- `Content-Type: text/html; charset=UTF-8`: Instructs the client on how to decode the incoming binary stream.

### Stage 6: Client DOM Construction & Paint
Upon receiving the response packets, the browser:
1. Parses HTML into a **Document Object Model (DOM)** tree.
2. Parses external/embedded CSS into a **CSS Object Model (CSSOM)** tree.
3. Combines both into a **Render Tree**, executes layout calculations, and paints pixels to the screen.

---

## Deployment & Testing Instructions

### 1. Browser Direct Run
Open `index.html` directly in any web browser to test:
- 3D perspective tilt transformations on the participating team cards.
- Live category filtering on the match fixtures table.
- Client-side form validation.

### 2. Local Python Server
```powershell
python -m http.server 8000
# Visit: http://localhost:8000/Question_3_Online_Sports_Tournament/
```

### 3. WAMP Deployment (Windows)
1. Copy the `Question_3_Online_Sports_Tournament` folder to:
   ```
   C:\wamp64\www\Question_3_Online_Sports_Tournament
   ```
2. Navigate to: `http://localhost/Question_3_Online_Sports_Tournament/`
3. Fill out the team registration form and submit to execute `register.php`.

### 4. LAMP Deployment (Linux)
```bash
sudo cp -r Question_3_Online_Sports_Tournament /var/www/html/
# Visit: http://localhost/Question_3_Online_Sports_Tournament/
```
