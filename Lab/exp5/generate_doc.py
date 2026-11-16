import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Page Margins
sections = doc.sections
for s in sections:
    s.top_margin = Inches(0.8)
    s.bottom_margin = Inches(0.8)
    s.left_margin = Inches(0.8)
    s.right_margin = Inches(0.8)

# Styling Helpers
def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def add_callout(doc, text, title=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    set_cell_background(c, 'F0F4F8')
    p = c.paragraphs[0]
    p.paragraph_format.left_indent = Inches(0.1)
    p.paragraph_format.right_indent = Inches(0.1)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    if title:
        run_t = p.add_run(f'{title}\n')
        run_t.bold = True
        run_t.font.name = 'Consolas'
        run_t.font.size = Pt(10)
        run_t.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    doc.add_paragraph()

# ----------------- SECTION 1: ORIGINAL QUESTION PAGES FIRST -----------------
q_title = doc.add_heading('ASSIGNMENT QUESTION PAPER', level=1)
q_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
q_title.runs[0].font.name = 'Arial'
q_title.runs[0].font.size = Pt(18)
q_title.runs[0].font.bold = True
q_title.runs[0].font.color.rgb = RGBColor(0x1A, 0x25, 0x2F)

sub_info = doc.add_paragraph('Course: Internet Programming | Question 5 | Total Marks: 20 Marks')
sub_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
sub_info.runs[0].font.name = 'Arial'
sub_info.runs[0].font.size = Pt(11)
sub_info.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)

doc.add_paragraph('------------------------------------------------------------------------------------------------------------------------')

p_intro = doc.add_paragraph()
r_intro = p_intro.add_run('Problem Statement:\n')
r_intro.bold = True
r_intro.font.size = Pt(11)
p_intro.add_run(
    'You are tasked with creating a simple multi-page website for a small business that includes a '
    'homepage, an about page, and a contact page. The client wants the site to have a cohesive '
    'design with appealing visual elements. You need to apply various CSS styling techniques, '
    'including color schemes, typography, and layout adjustments, to enhance the overall look and '
    'feel of the site.'
)

p_params = doc.add_paragraph()
r_param_h = p_params.add_run('Parameters:\n')
r_param_h.bold = True
p_params.add_run('❖ The website must include a homepage, an about page, and a contact page.\n')
p_params.add_run('❖ The design must be cohesive with appealing visual elements using CSS styling techniques such as color schemes, typography, and layout adjustments.\n')
p_params.add_run('❖ Focus on creating a visually engaging experience while ensuring proper functionality across all pages.')

p_q = doc.add_paragraph()
r_qh = p_q.add_run('Questions:\n')
r_qh.bold = True
p_q.add_run('1. Explain the structure and content of the homepage, about page, and contact page, highlighting their purpose.\n')
p_q.add_run('2. Describe the CSS techniques applied to ensure a cohesive design, focusing on color schemes, typography, and layout.\n')
p_q.add_run('3. Outline the HTML structure and how the pages are linked to create navigation across the site.\n\n')

p_marks = doc.add_paragraph()
r_mh = p_marks.add_run('Marks Distribution (20 Marks):\n')
r_mh.bold = True
p_marks.add_run('• Explanation of website structure and content: 7 marks\n')
p_marks.add_run('• Explanation of CSS styling techniques: 7 marks\n')
p_marks.add_run('• Description of HTML structure and navigation: 6 marks')

# ----------------- SECTION SEPARATION / PAGE BREAK -----------------
doc.add_page_break()

# ----------------- SECTION 2: GENERATED ANSWERS -----------------
ans_h = doc.add_heading('SOLUTIONS & GENERATED ANSWERS', level=1)
ans_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
ans_h.runs[0].font.name = 'Arial'
ans_h.runs[0].font.size = Pt(18)
ans_h.runs[0].font.bold = True
ans_h.runs[0].font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)

doc.add_paragraph('------------------------------------------------------------------------------------------------------------------------')

# Question 1: Structure and Content (7 Marks)
doc.add_heading('1. Structure and Content of Homepage, About Page, and Contact Page (7 Marks)', level=2)
doc.add_paragraph(
    'The small business website is architected for "Roast & Brew Coffee Roasters", an artisanal specialty coffee '
    'company. The website comprises three interconnected pages, each engineered with a dedicated structural purpose, '
    'clear information hierarchy, and user-centric conversion funnels.'
)

site_map_diagram = (
    "+-------------------------------------------------------------------------+\n"
    "|                  ROAST & BREW COFFEE ROASTERS SITE MAP                  |\n"
    "+-------------------------------------------------------------------------+\n"
    "|                                                                         |\n"
    "|            +-----------------------------------------------+            |\n"
    "|            |            SHARED NAVIGATION HEADER           |            |\n"
    "|            | [Logo]  [Home]   [About Us]   [Contact] [CTA] |            |\n"
    "|            +-----------------------------------------------+            |\n"
    "|                    |                   |                   |            |\n"
    "|         +----------+         +---------+---------+         +--------+   |\n"
    "|         v                    v                   v                  v   |\n"
    "|  +---------------+   +---------------+   +----------------+             |\n"
    "|  | HOMEPAGE      |   | ABOUT PAGE    |   | CONTACT PAGE   |             |\n"
    "|  | (index.html)  |   | (about.html)  |   | (contact.html) |             |\n"
    "|  |---------------|   |---------------|   |----------------|             |\n"
    "|  | * Hero Banner |   | * Page Banner |   | * Page Banner  |             |\n"
    "|  | * Value Props |   | * Origin Story|   | * Roastery Info|             |\n"
    "|  | * Best Sellers|   | * 3-Stage Proc|   | * Interactive  |             |\n"
    "|  | * Store Info  |   | * Impact Stats|   |   Contact Form |             |\n"
    "|  +---------------+   +---------------+   +----------------+             |\n"
    "|                    |                   |                   |            |\n"
    "|            +-----------------------------------------------+            |\n"
    "|            |            SHARED RECIPROCAL FOOTER           |            |\n"
    "|            | Brand Summary | Quick Links | Hours | Rights  |            |\n"
    "|            +-----------------------------------------------+            |\n"
    "+-------------------------------------------------------------------------+"
)
add_callout(doc, site_map_diagram, 'Site Architecture & Page Hierarchy Diagram')

pages_breakdown = [
    ("1. Homepage (index.html) - Brand Immersion & Conversion",
     "Purpose: Establishes brand identity, introduces value propositions, and directs visitors to product offerings.\n"
     "• Hero Section: Dynamic high-contrast banner featuring the brand headline, sub-headline, and dual CTA buttons ('Discover Our Story' and 'Find Our Roastery').\n"
     "• Value Pillars: Three-column card grid highlighting '100% Direct Trade', 'Master Drum Roasting', and 'Freshness Guaranteed'.\n"
     "• Featured Products Showcase: Displays signature seasonal beans (Highland Yirgacheffe, Andean Velvet, Midnight Espresso) with tasting notes, roast levels, and pricing.\n"
     "• Roastery Info Strip: Concise physical location and business hours banner providing instant store details."),
    ("2. About Page (about.html) - Trust Building & Craftsmanship Heritage",
     "Purpose: Builds credibility, communicates ethical sourcing philosophy, and details roasting craftsmanship.\n"
     "• Page Banner: Minimalist header establishing the 'Heritage & Craft' narrative.\n"
     "• Origin Story & Philosophy: Compelling background story explaining why the business was founded, featuring an authentic quote callout from the Head Roaster.\n"
     "• Quantitative Impact Grid: 4-stat metric dashboard showcasing '100% Specialty Arabica', '14 Farm Partners', '250+ Weekly Batches', and '0 Additives'.\n"
     "• 3-Stage Process Pipeline: Step-by-step breakdown (Stage 01: Ethical Sourcing, Stage 02: Thermodynamic Roasting, Stage 03: Cupping & Packaging).\n"
     "• Call to Action Strip: Encourages wholesale partnerships and cafe visits."),
    ("3. Contact Page (contact.html) - Customer Inquiry & Location Discovery",
     "Purpose: Facilitates direct customer communication, wholesale inquiries, and tasting room visitation.\n"
     "• Split 2-Column Responsive Layout:\n"
     "  - Left Column (Store Details): Full physical address, phone numbers, departmental email routing, weekly operating hours, and stylized location map container.\n"
     "  - Right Column (Interactive Inquiry Form): Captures applicant/customer name, email address, inquiry category (Retail, Subscription, Wholesale, Tours), and message body.\n"
     "  - Dynamic Feedback: Integrated JavaScript validation with a celebratory confirmation toast notification upon submission.")
]

for title, desc in pages_breakdown:
    p = doc.add_paragraph()
    p.add_run(f'• {title}:\n').bold = True
    p.add_run(desc)

# Question 2: CSS Styling Techniques (7 Marks)
doc.add_heading('2. CSS Techniques Applied for Cohesive Design: Color, Typography & Layout (7 Marks)', level=2)
doc.add_paragraph(
    'To achieve a cohesive aesthetic across all three pages, the styling relies on a centralized stylesheet (style.css) '
    'built upon modern CSS3 principles and the 60-30-10 color balance rule:'
)

css_techniques = [
    ("1. Unified Color Palette & CSS Custom Properties (--variables)",
     "A centralized :root block defines semantic color variables reflecting the artisan coffee theme:\n"
     "• Dominant Base (60%): Warm Cream Light (#fdfbf7) and Sand (#f5eedf) for comfortable, inviting backgrounds.\n"
     "• Secondary Structure (30%): Deep Espresso (#221510) and Dark Roast (#2d1e17) for navigation bars, footers, and text hierarchy.\n"
     "• Accent Pop (10%): Roasted Amber Gold (#c26a1b) for hover states, buttons, active link indicators, and badges.\n"
     "This strict palette maintains immediate visual brand recognition across every viewport."),
    ("2. Typography System & Modular Font Hierarchy",
     "• Heading Font: 'Playfair Display' / Georgia serif typeface evokes artisanal elegance, warmth, and culinary heritage.\n"
     "• Body Font: Apple System / Roboto / Segoe UI sans-serif provides crisp readability for paragraphs and tables.\n"
     "• Modular Scale: Consistent line heights (1.65), letter-spacing on sub-badges (1.5px uppercase), and proportional font sizes (46px hero down to 12px tags)."),
    ("3. Advanced Layout Adjustments: CSS Grid & Flexbox",
     "• Sticky Navigation: The <header class=\"site-header\"> utilizes position: sticky; top: 0; z-index: 1000; with box-shadow to anchor navigation throughout scrolling.\n"
     "• 3-Column Card Grids: .cards-grid and .product-grid leverage display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; for symmetrical alignment.\n"
     "• Split Asymmetric Layouts: .story-grid and .contact-split-grid employ proportional ratios (1.2fr to 0.8fr) to balance informational text with visual widgets.\n"
     "• Card Elevations & Micro-Interactions: Cards incorporate subtle border styling (1px solid var(--color-border)) and elevate on hover via transform: translateY(-5px); and deep box-shadow."),
    ("4. Responsive Breakpoints & Mobile Adaptability",
     "• @media (max-width: 900px): Grids gracefully fold from 3 columns into 2 columns, and split panels collapse into stacked blocks.\n"
     "• @media (max-width: 680px): Triggers mobile hamburger navigation (.menu-toggle), turning horizontal navigation links into an animated absolute dropdown drawer.")
]

for title, desc in css_techniques:
    p = doc.add_paragraph()
    p.add_run(f'• {title}:\n').bold = True
    p.add_run(desc)

# Question 3: HTML Structure & Navigation (6 Marks)
doc.add_heading('3. HTML Structure & Navigation Linking Architecture (6 Marks)', level=2)
doc.add_paragraph(
    'Navigation across the site is built on semantic HTML5 elements (<header>, <nav>, <main>, <section>, <footer>) '
    'and reciprocal relative hyperlinking:'
)

doc.add_paragraph(
    'Navigation Principles:\n'
    '1. Identical Header Structure: Each page (index.html, about.html, contact.html) incorporates the same top navigation markup, '
    'preventing disorientation as users transition between URLs.\n'
    '2. Visual State Awareness (.nav-link.active): The current page is marked with class="nav-link active", which activates an amber underline '
    'and colored font so users always know their location in the site hierarchy.\n'
    '3. Reciprocal Relative Linking: All anchors use clean relative URLs (href="index.html", href="about.html", href="contact.html"), '
    'ensuring seamless local execution without requiring a web server or internet connection.\n'
    '4. Double Navigation Redundancy: Navigation links are mirrored in both the primary sticky header and the multi-column footer, '
    'allowing visitors at the bottom of long pages to navigate without scrolling to the top.'
)

# Source Code Appendices
doc.add_heading('Complete Source Code Listings for Small Business Website', level=2)

# Read and attach index.html
with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r', encoding='utf-8') as f:
    html_home = f.read()
add_callout(doc, html_home, '1. Homepage HTML: index.html')

# Read and attach about.html
with open(os.path.join(os.path.dirname(__file__), 'about.html'), 'r', encoding='utf-8') as f:
    html_about = f.read()
add_callout(doc, html_about, '2. About Page HTML: about.html')

# Read and attach contact.html
with open(os.path.join(os.path.dirname(__file__), 'contact.html'), 'r', encoding='utf-8') as f:
    html_contact = f.read()
add_callout(doc, html_contact, '3. Contact Page HTML: contact.html')

# Read and attach style.css
with open(os.path.join(os.path.dirname(__file__), 'style.css'), 'r', encoding='utf-8') as f:
    css_code = f.read()
add_callout(doc, css_code, '4. Central Cohesive Stylesheet: style.css')

# Read and attach script.js
with open(os.path.join(os.path.dirname(__file__), 'script.js'), 'r', encoding='utf-8') as f:
    js_code = f.read()
add_callout(doc, js_code, '5. Client-Side Interactivity Script: script.js')

# Output Document Path
doc_path = os.path.join(os.path.dirname(__file__), 'Small_Business_MultiPage_Website_Assignment_Submission.docx')
doc.save(doc_path)
print('SUCCESS: Created', doc_path)
