# Question 4: E-Commerce Product Showcase Website (NexTech Electronics)

## Overview & Scenario
A retail showcase web application for consumer electronics (NexTech Retail). The platform exhibits flagship hardware (ultrabooks, noise-canceling headphones, AMOLED tablets, biometric smartwatches), displays cross-device specification comparisons in tabular matrices, organizes departmental taxonomies via lists, collects purchase enquiries through validated HTML5 forms, and provides an academic demonstration of CSS3 styling, animations, border images, cascading, and property inheritance.

---

## Requirements & Implementation Matrix

| Requirement | Implementation Details | File / Location |
|---|---|---|
| **HTML5 Product Cards** | Product cards with inline SVG device art, badges, star ratings, prices, and CTAs | Showcase Section in `index.html` |
| **Specifications Tables** | Comparison table (`<table>`) with `<caption>`, `<thead>`, `<tbody>`, `<tfoot>`, comparing 8 hardware parameters | Specs Section in `index.html` |
| **Product Categories in Lists** | Categorical nested unordered (`<ul>`) and ordered (`<ol>`) lists | Categories in `index.html` |
| **Customer Enquiry Form** | Validated HTML5 inputs (`text`, `email`, `tel`, `number`, `radio`, `select`, `textarea`) | Enquiry Section in `index.html` |
| **CSS3 Border Image** | Linear gradient border image (`border-image: linear-gradient(to right, ...) 1`) | Cascade Section in `style.css` |
| **CSS3 Backgrounds & Colors** | Radial gradient glows, subtle surface color hierarchy, custom variables | `style.css` |
| **Shadows & Text Effects** | Multi-level elevation shadows, `text-shadow` glow effect, hover transforms | `style.css` |
| **Card Transitions & Animations** | `cubic-bezier(0.165, 0.84, 0.44, 1)` hover lift and SVG scale zoom | `style.css` |
| **CSS Cascading & Inheritance** | Dedicated academic demo and explanation of specificity scores and inheritance | `index.html`, `style.css`, and below |
| **WAMP/LAMP Configuration** | Step-by-step Apache server deployment and testing guide | Documented below & `enquire.php` |

---

## Technical Deep-Dive: CSS Cascading and Inheritance

### 1. The Principle of Cascading & Specificity
When multiple CSS declarations target the same DOM element, the browser resolves conflicts using the **CSS Cascade**, governed by:
1. **Origin and Importance**: `!important` declarations override normal declarations.
2. **Specificity Weight Hierarchy**: Represented as a 4-part tuple $(a, b, c, d)$:

| Level | Selector Type | Weight Contribution | Example |
|---|---|---|---|
| $a$ | **Inline Styles** | $1, 0, 0, 0$ | `<p style="color: green;">` |
| $b$ | **ID Selectors** | $0, 1, 0, 0$ | `#uniqueSpecificityId` |
| $c$ | **Classes, Attributes, Pseudo-classes** | $0, 0, 1, 0$ | `.general-class-specificity`, `[type="text"]`, `:hover` |
| $d$ | **Elements & Pseudo-elements** | $0, 0, 0, 1$ | `p`, `div`, `::before` |

*Order of Appearance*: If two rules have identical specificity, the **last declared rule** in the stylesheet wins.

### 2. CSS Property Inheritance
Not all CSS properties inherit from parent to child by default:
- **Naturally Inherited Properties**: Typography and color properties flow down the DOM tree (`color`, `font-family`, `font-size`, `line-height`, `letter-spacing`, `text-align`).
- **Non-Inherited Properties (Box Model)**: Layout and geometry properties default to `initial` (`border`, `margin`, `padding`, `background`, `width`, `height`, `position`).
- **The `inherit` Keyword**: Forces a child element to explicitly inherit a non-inherited property from its parent container (demonstrated in our `.child-inherit-border` class: `border: inherit;`).

---

## Deployment & Testing Instructions

### 1. Standalone Browser Preview
Open `index.html` directly in Chrome, Edge, or Firefox:
- Inspect smooth product card hover animations and SVG zoom transitions.
- Test "Enquire Now" shortcuts that auto-select the chosen device in the enquiry form.
- Verify the CSS Cascading & Inheritance demonstration box.

### 2. Local Python Server
```powershell
python -m http.server 8000
# Visit: http://localhost:8000/Question_4_Ecommerce_Product_Showcase/
```

### 3. WAMP Deployment (Windows)
1. Copy the `Question_4_Ecommerce_Product_Showcase` folder to:
   ```
   C:\wamp64\www\Question_4_Ecommerce_Product_Showcase
   ```
2. Navigate in browser to:
   ```
   http://localhost/Question_4_Ecommerce_Product_Showcase/
   ```
3. Submit a customer purchase enquiry to execute `enquire.php` and receive an official quotation voucher.

### 4. LAMP Deployment (Linux)
```bash
sudo cp -r Question_4_Ecommerce_Product_Showcase /var/www/html/
# Visit: http://localhost/Question_4_Ecommerce_Product_Showcase/
```
