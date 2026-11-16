# Question 5: Online Travel and Tourism Website (WanderLust Global Journeys)

## Overview & Scenario
A premier online tourism application developed for international travel agencies (WanderLust Global Journeys). The platform showcases scenic destinations (Swiss Alps, Bali, Kyoto, Santorini) with high-fidelity vector imagery, compares multi-tiered vacation packages via comparative tabular grids, categorizes world heritage attractions and guest amenities via semantic lists, provides an interactive travel reservation form, and delivers an architectural explanation of HTTP client-server communication.

---

## Requirements & Implementation Matrix

| Requirement | Implementation Details | File / Location |
|---|---|---|
| **Display Destinations Using Images** | Responsive destination cards with inline SVG landscapes and luxury hotel tags | Destinations Section in `index.html` |
| **Tables to Compare Packages** | Comparative table (`<table>`) with `<caption>`, `<thead>`, `<tbody>`, `<tfoot>`, comparing 3 package tiers across 7 parameters | Packages Section in `index.html` |
| **Lists of Attractions & Facilities** | Unordered (`<ul>`) list of UNESCO heritage attractions and ordered (`<ol>`) list of guest amenities | Attractions Section in `index.html` |
| **HTML5 Booking Controls** | Inputs: `text`, `email`, `tel`, `date` (with `min`), `number` (with `min`/`max`), `select`, `checkbox`, `textarea` | Booking Form in `index.html` |
| **CSS3 Background Images & Gradients** | Layered radial ambient glows and linear gradient background overlays | `style.css` |
| **CSS3 Border Image & Text Shadows** | Two-tone linear gradient border-image (`border-image: linear-gradient(...) 1`) and glowing text shadows (`text-shadow`) | `style.css` |
| **Hover Effects & CSS Animations** | Smooth image zoom (`scale(1.08)`), card elevation (`translateY(-8px)`), and floating badge animation (`@keyframes floatSun`) | `style.css` |
| **HTTP Communication Explanation** | Comprehensive breakdown of HTTP request methods, headers, status code taxonomy, and statelessness | Documented below & in `index.html` |
| **WAMP/LAMP Configuration** | Step-by-step Apache server deployment and testing guide | Documented below & `booking.php` |

---

## Technical Deep-Dive: How Web Clients Communicate With Web Servers Using HTTP

Hypertext Transfer Protocol (HTTP) is the foundational application-layer protocol powering the World Wide Web. Communication operates via a **request-response model** over a reliable TCP/IP connection.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      HTTP CLIENT-SERVER TRANSACTION                    │
└────────────────────────────────────────────────────────────────────────┘

  [Web Client / Browser]                               [Apache Web Server (WAMP/LAMP)]
           │                                                         │
           │  1. HTTP Request (Method, URI, Protocol Version)        │
           ├────────────────────────────────────────────────────────►│
           │     POST /booking.php HTTP/1.1                          │
           │     Host: localhost                                     │
           │     User-Agent: Chrome/120.0                            │
           │     Accept: text/html,application/xhtml+xml             │
           │     Content-Type: application/x-www-form-urlencoded     │
           │     Content-Length: 184                                 │
           │                                                         │
           │     [Message Body: traveler=Mithun&dest=Swiss+Alps...]  │
           │                                                         │
           │                                            2. Server    │
           │                                               Logic:    │
           │                                               - Read Body
           │                                               - Parse URI
           │                                               - Run PHP 
           │                                                         │
           │  3. HTTP Response (Status Line, Headers, Entity Body)   │
           │◄────────────────────────────────────────────────────────┤
           │     HTTP/1.1 200 OK                                     │
           │     Date: Sat, 14 Nov 2026 13:00:00 GMT                 │
           │     Server: Apache/2.4.58 (Win64) PHP/8.2               │
           │     Content-Type: text/html; charset=UTF-8              │
           │     Content-Length: 2150                                │
           │     Connection: keep-alive                              │
           │                                                         │
           │     [HTML Entity Body / Travel Voucher]                 │
```

### 1. HTTP Request Methods
The method indicates the desired action to be performed on the identified resource:
- **`GET`**: Requests data from a specified resource (e.g. loading `index.html` or fetching images). Should never alter server state.
- **`POST`**: Submits an entity to the specified resource, commonly resulting in a change in state or side effect on the server (e.g., submitting tour booking requests). Data is transmitted securely inside the message payload.
- **`PUT`**: Replaces all current representations of the target resource with the uploaded payload.
- **`DELETE`**: Deletes the specified resource.
- **`HEAD`**: Asks for an identical response to a GET request, but without the response body (useful for caching validation and checking content length).

### 2. Request and Response Headers
Headers provide essential metadata governing content negotiation, security, and connection persistence:
- **Request Headers**:
  - `Host`: Domain name of the server (mandatory in HTTP/1.1).
  - `User-Agent`: String identifying client browser engine and OS.
  - `Accept`: MIME types acceptable by the client (`text/html`, `image/webp`).
  - `Content-Type`: Format of the data in the request body (`application/x-www-form-urlencoded`).
- **Response Headers**:
  - `Content-Type`: Tells the browser how to interpret the payload (`text/html; charset=UTF-8`).
  - `Server`: Software handling the request (`Apache/2.4.58`).
  - `Connection: keep-alive`: Allows multiple requests over the same TCP socket, mitigating latency.

### 3. HTTP Status Code Taxonomy
Status codes are grouped into five standard families:
1. **1xx (Informational)**: Request received, continuing process (e.g., `100 Continue`, `101 Switching Protocols`).
2. **2xx (Success)**: Action successfully received, understood, and accepted (e.g., `200 OK`, `201 Created`, `204 No Content`).
3. **3xx (Redirection)**: Further action must be taken to complete request (e.g., `301 Moved Permanently`, `302 Found`, `304 Not Modified`).
4. **4xx (Client Error)**: Request contains bad syntax or cannot be fulfilled (e.g., `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `405 Method Not Allowed`).
5. **5xx (Server Error)**: Server failed to fulfill an apparently valid request (e.g., `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`).

### 4. Protocol Statelessness & Cookie Sessions
HTTP is inherently **stateless** — each request is executed independently without inherent memory of preceding requests. Web applications bridge this by issuing `Set-Cookie: session_id=...` headers upon login or form booking, which the browser stores and automatically re-transmits in subsequent requests, enabling persistent user carts and booking sessions.

---

## Deployment & Testing Instructions

### 1. Direct Browser Client Preview
Double-click `index.html` to open in Chrome, Edge, or Firefox:
- Explore the interactive destination cards with hover zoom transitions.
- Review the package comparison matrix with gradient border styling.
- Submit the tour reservation form to test client-side validation and fallback preview.

### 2. Local Python Server
```powershell
python -m http.server 8000
# Visit: http://localhost:8000/Question_5_Online_Travel_Tourism/
```

### 3. WAMP Deployment (Windows)
1. Copy the `Question_5_Online_Travel_Tourism` folder to:
   ```
   C:\wamp64\www\Question_5_Online_Travel_Tourism
   ```
2. Navigate in browser to:
   ```
   http://localhost/Question_5_Online_Travel_Tourism/
   ```
3. Submit a travel reservation to execute `booking.php` and generate an official WanderLust confirmation voucher.

### 4. LAMP Deployment (Linux)
```bash
sudo cp -r Question_5_Online_Travel_Tourism /var/www/html/
# Visit: http://localhost/Question_5_Online_Travel_Tourism/
```
