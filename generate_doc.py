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

# Styling Helper
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

sub_info = doc.add_paragraph('Course: Internet Programming | Total Marks: 20 Marks')
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
    'You are tasked with creating a web page for a bike showroom. The showroom wants a clean '
    'and interactive design where customers can easily navigate through different bike brands '
    'and view the specific models and their specifications. The page should be divided into three '
    'frames using a frameset: a top row for displaying the showroom name, a left column for '
    'listing bike brands with hyperlinks, and a right column for showing the corresponding bike '
    'models and specifications when a brand is selected.'
)

p_params = doc.add_paragraph()
r_param_h = p_params.add_run('Parameters:\n')
r_param_h.bold = True
p_params.add_run('• The bike showroom offers multiple bike brands.\n')
p_params.add_run('• Each brand has a selection of bike models with detailed specifications.\n')
p_params.add_run("• The showroom's goal is to provide an interactive and easy-to-navigate page.\n\n")
p_params.add_run('The page must be divided into three frames:\n')
p_params.add_run('1. Top row for displaying the showroom name.\n')
p_params.add_run('2. Left column for listing bike brands with hyperlinks.\n')
p_params.add_run('3. Right column for displaying corresponding bike models and specifications based on brand selection.')

p_q = doc.add_paragraph()
r_qh = p_q.add_run('Questions:\n')
r_qh.bold = True
p_q.add_run('a) Design the layout of the bike showroom webpage using HTML frameset\n')
p_q.add_run('b) Provide HTML and CSS code to implement the design, ensuring a clean and interactive user experience.\n')
p_q.add_run('c) Write the HTML code for the frameset and the structure for the left and right columns.\n')
p_q.add_run('d) Discuss potential challenges in handling semi-structured data during the ETL process and propose solutions.\n\n')

p_marks = doc.add_paragraph()
r_mh = p_marks.add_run('Marks Distribution (20 Marks):\n')
r_mh.bold = True
p_marks.add_run('• Frameset layout design: 4 marks\n')
p_marks.add_run('• HTML and CSS code for the page: 4 marks\n')
p_marks.add_run('• HTML code : 12 marks\n')
p_marks.add_run('Requirement Note: Website design should be very simple and basic.')

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

# Question (a)
doc.add_heading('Question (a): Layout Design of Bike Showroom Webpage Using HTML Frameset (4 Marks)', level=2)
doc.add_paragraph(
    'The webpage layout is architected using standard HTML framesets. In an HTML frameset architecture, '
    'the browser window is divided into independent rectangular regions (frames), where each frame loads an '
    'autonomous HTML document. For the bike showroom, the layout requires a three-frame arrangement:\n'
    '1. Top Row (Header Frame): Allocated 20% of vertical height to display the showroom brand name and banner.\n'
    '2. Left Column (Navigation Frame): Allocated 25% of horizontal width inside the lower section for brand hyperlinks.\n'
    '3. Right Column (Content Display Frame): Allocated 75% of horizontal width inside the lower section for bike models and specifications.'
)

diagram_text = (
    "+-------------------------------------------------------------------------+\n"
    "|                       TOP ROW: HEADER FRAME (20%)                       |\n"
    "|                 Name: \"headerFrame\" | Source: header.html                |\n"
    "|                 Content: SpeedWheels Bike Showroom Title                |\n"
    "+------------------------------------+------------------------------------+\n"
    "|     LEFT COLUMN (25%)              |        RIGHT COLUMN (75%)          |\n"
    "|     Name: \"navFrame\"               |        Name: \"mainFrame\"           |\n"
    "|     Source: nav.html               |        Source: home.html (Default) |\n"
    "|                                    |                                    |\n"
    "|     Hyperlinks to Brands:          |     Loads when brand clicked:      |\n"
    "|     - Yamaha (target=\"mainFrame\")  |     - Yamaha Models & Specs        |\n"
    "|     - Honda (target=\"mainFrame\")   |     - Honda Models & Specs         |\n"
    "|     - Royal Enfield                |     - Royal Enfield Models & Specs |\n"
    "|     - Kawasaki                     |     - Kawasaki Models & Specs      |\n"
    "+------------------------------------+------------------------------------+"
)
add_callout(doc, diagram_text, 'Visual Architecture Diagram (Frameset Layout)')

p_explain = doc.add_paragraph()
p_explain.add_run('Key Architectural Principles:\n').bold = True
p_explain.add_run(
    '1. Frame Nesting: The outer <frameset rows="20%, 80%"> partitions the screen vertically. '
    'The bottom 80% row contains a nested <frameset cols="25%, 75%"> to create the left and right columns.\n'
    '2. Target Redirection: In nav.html, each hyperlink uses the attribute target="mainFrame". '
    'This informs the browser to retain the top header and left menu static while refreshing only the right content frame.\n'
    '3. Seamless User Experience: Customers can switch between brands without the page re-downloading the header or navigation bar, '
    'ensuring smooth and rapid browsing.'
)

# Question (b)
doc.add_heading('Question (b): HTML and CSS Code for Clean and Interactive User Experience (4 Marks)', level=2)
doc.add_paragraph(
    'To fulfill the requirement of keeping the design simple, basic, and interactive, a centralized stylesheet (style.css) '
    'is applied across all frames. It features clear typography, card layouts, distinct hover effects on navigation buttons, '
    'and well-structured tabular presentation for technical specifications.'
)

css_code = """/* Shared CSS Stylesheet: style.css */
body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    padding: 15px;
    background-color: #f7f9fa;
    color: #333333;
}

/* Header Frame Styles */
.header-container {
    background-color: #1a252f;
    color: #ffffff;
    text-align: center;
    padding: 15px 10px;
    border-radius: 6px;
}
.header-container h1 {
    margin: 0 0 5px 0;
    font-size: 26px;
    letter-spacing: 1px;
    color: #e74c3c;
}
.header-container p {
    margin: 0;
    font-size: 14px;
    color: #bdc3c7;
}

/* Navigation Frame Styles */
.nav-container {
    background-color: #ffffff;
    padding: 15px;
    border: 1px solid #dcdcdc;
    border-radius: 6px;
}
.nav-container h3 {
    margin-top: 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #e74c3c;
    color: #2c3e50;
    font-size: 18px;
}
.nav-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}
.nav-list li {
    margin-bottom: 10px;
}
.nav-list a {
    display: block;
    text-decoration: none;
    color: #2c3e50;
    background-color: #ecf0f1;
    padding: 10px 12px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 15px;
    border-left: 4px solid #3498db;
    transition: 0.2s ease;
}
.nav-list a:hover {
    background-color: #3498db;
    color: #ffffff;
    border-left: 4px solid #e74c3c;
}

/* Specifications Table */
table.spec-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    margin-bottom: 20px;
    font-size: 14px;
}
table.spec-table th, table.spec-table td {
    border: 1px solid #dddddd;
    padding: 9px 12px;
    text-align: left;
}
table.spec-table th {
    background-color: #2c3e50;
    color: #ffffff;
    width: 35%;
}
table.spec-table tr:nth-child(even) {
    background-color: #f9f9f9;
}"""
add_callout(doc, css_code, 'CSS Code: style.css')

# Question (c)
doc.add_heading('Question (c): Complete HTML Code for Frameset, Left, and Right Columns (12 Marks)', level=2)
doc.add_paragraph(
    'The website comprises modular HTML documents working together. Below is the full code for the master frameset, '
    'the header frame, the navigation sidebar, and the model/specification content pages.'
)

# index.html
html_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SpeedWheels Bike Showroom</title>
</head>
<!-- Outer frameset: 20% Top Row, 80% Bottom Area -->
<frameset rows="20%, 80%" border="2" frameborder="1" framespacing="2">
    <!-- Frame 1: Top Row for Showroom Header -->
    <frame src="header.html" name="headerFrame" scrolling="no" noresize>

    <!-- Inner nested frameset: 25% Left Column, 75% Right Column -->
    <frameset cols="25%, 75%" border="2" frameborder="1" framespacing="2">
        <!-- Frame 2: Left Navigation Column -->
        <frame src="nav.html" name="navFrame" scrolling="auto">
        <!-- Frame 3: Right Model & Specifications Display Column -->
        <frame src="home.html" name="mainFrame" scrolling="auto">
    </frameset>

    <!-- Fallback for non-supporting browsers -->
    <noframes>
        <body>
            <h2>Browser Not Supported</h2>
            <p>Your browser does not support HTML frames. Please use a modern browser.</p>
        </body>
    </noframes>
</frameset>
</html>"""
add_callout(doc, html_index, '1. Master Frameset HTML: index.html')

# header.html
html_header = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Showroom Header</title>
    <link rel="stylesheet" href="style.css">
</head>
<body style="background-color: #1a252f; padding: 10px;">
    <div class="header-container">
        <h1>SPEEDWHEELS BIKE SHOWROOM</h1>
        <p>Your Premier Destination for Top Motorcycle Brands & Performance Rides</p>
    </div>
</body>
</html>"""
add_callout(doc, html_header, '2. Top Row Header Frame HTML: header.html')

# nav.html
html_nav = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bike Brands Navigation</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="nav-container">
        <h3>Bike Brands</h3>
        <ul class="nav-list">
            <li><a href="home.html" target="mainFrame">Home / Overview</a></li>
            <li><a href="yamaha.html" target="mainFrame">Yamaha</a></li>
            <li><a href="honda.html" target="mainFrame">Honda</a></li>
            <li><a href="royalenfield.html" target="mainFrame">Royal Enfield</a></li>
            <li><a href="kawasaki.html" target="mainFrame">Kawasaki</a></li>
        </ul>
    </div>
</body>
</html>"""
add_callout(doc, html_nav, '3. Left Column Navigation Frame HTML: nav.html')

# home.html
html_home = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome to SpeedWheels</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="content-card welcome-box">
        <h2>Welcome to SpeedWheels Bike Showroom!</h2>
        <p>
            Explore our wide range of premium two-wheelers from world-class motorcycle manufacturers.
            Click on any bike brand from the <strong>left navigation menu</strong> to view available models,
            engine details, mileage, braking systems, and price specifications.
        </p>
        <p style="margin-top: 25px; color: #7f8c8d; font-size: 13px;">
            Select a brand (Yamaha, Honda, Royal Enfield, Kawasaki) to begin exploring.
        </p>
    </div>
</body>
</html>"""
add_callout(doc, html_home, '4. Right Column Initial Display Frame HTML: home.html')

# yamaha.html
html_yamaha = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Yamaha Motorcycles</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="content-card">
        <h2 class="brand-title">Yamaha Motorcycles</h2>
        <p class="model-desc">Yamaha is renowned for racing heritage, sharp aerodynamics, and high-revving performance.</p>

        <!-- Model 1 -->
        <h3 class="model-title">1. Yamaha YZF-R15 V4</h3>
        <p class="model-desc">Track-focused supersport bike equipped with variable valve actuation (VVA).</p>
        <table class="spec-table">
            <tr><th>Specification</th><td>Details</td></tr>
            <tr><th>Engine Displacement</th><td>155 cc (Liquid-cooled, 4-stroke, SOHC, 4-valve)</td></tr>
            <tr><th>Max Power</th><td>18.4 PS @ 10,000 rpm</td></tr>
            <tr><th>Max Torque</th><td>14.2 Nm @ 7,500 rpm</td></tr>
            <tr><th>Fuel Mileage</th><td>Approx. 45 - 50 km/l</td></tr>
            <tr><th>Braking & Safety</th><td>Dual Channel ABS with Traction Control System</td></tr>
            <tr><th>Ex-Showroom Price</th><td>$2,300 (approx.)</td></tr>
        </table>

        <!-- Model 2 -->
        <h3 class="model-title">2. Yamaha MT-15 V2</h3>
        <p class="model-desc">Hyper-naked streetfighter offering agile handling and punchy acceleration.</p>
        <table class="spec-table">
            <tr><th>Specification</th><td>Details</td></tr>
            <tr><th>Engine Displacement</th><td>155 cc (Liquid-cooled, 4-stroke, FI)</td></tr>
            <tr><th>Max Power</th><td>18.4 PS @ 10,000 rpm</td></tr>
            <tr><th>Max Torque</th><td>14.1 Nm @ 7,500 rpm</td></tr>
            <tr><th>Fuel Mileage</th><td>Approx. 48 - 52 km/l</td></tr>
            <tr><th>Braking & Safety</th><td>Dual Channel ABS</td></tr>
            <tr><th>Ex-Showroom Price</th><td>$2,100 (approx.)</td></tr>
        </table>
    </div>
</body>
</html>"""
add_callout(doc, html_yamaha, '5. Right Column Brand Page Sample: yamaha.html')

# Question (d)
doc.add_heading('Question (d): Potential Challenges in Handling Semi-Structured Data During ETL & Proposed Solutions', level=2)
doc.add_paragraph(
    'In modern enterprise architectures such as digital automotive dealerships and multi-brand bike showrooms, '
    'technical specifications, telematics feeds, dealer inventories, and customer interactions arrive as semi-structured data '
    '(JSON, XML, or NoSQL document dumps). While semi-structured data offers flexibility, it introduces significant '
    'complications during the Extract, Transform, Load (ETL) pipeline when moving data into structured warehouses or analytical data marts.'
)

doc.add_heading('1. Potential Challenges in Handling Semi-Structured Data During ETL', level=3)

challenges = [
    ("Schema Drift and Dynamic Variability",
     "Unlike relational tables where columns are fixed, semi-structured data does not enforce rigid schemas. Manufacturers frequently introduce new nested attributes (e.g., adding 'ridingModes' or 'batteryPackKW' for newer electric models) or rename keys without advance notice. Traditional rigid ETL pipelines fail or drop unmapped attributes when encountering unexpected keys."),
    ("Data Type Inconsistencies and Heterogeneity",
     "Values across different JSON feeds frequently lack uniform data types. For instance, engine displacement might appear as an integer (350), a float (348.36), or a text string ('350 cc'). Similarly, power ratings can be recorded across incompatible units (e.g., PS, bhp, kW). Merging these into a unified data warehouse results in type casting exceptions and corrupted analytical aggregations."),
    ("Complex Hierarchical Nesting and Arrays",
     "Bike specifications often contain nested child arrays and deep objects (e.g., multiple available color options, package tiers, financing plans). Flattening these arrays into flat relational structures requires unnesting/exploding operations, which can lead to Cartesian explosion, exponential row multiplication, and massive compute overhead."),
    ("High Data Sparsity and Null Value Proliferation",
     "Different vehicle categories possess vastly different attributes (e.g., an electric scooter has 'chargingTime' and 'regenerativeBraking', whereas a superbike has 'cylinderArrangement' and 'exhaustValve'). Ingesting all variants into a single tabular schema creates wide, sparse tables with thousands of NULL entries, degrading columnar compression and query performance."),
    ("Parsing Latency and Performance Bottlenecks",
     "Parsing complex, multi-megabyte JSON or XML files is computationally intensive. CPU-bound serial string parsers can choke high-throughput ingestion pipelines, creating significant ETL latency and delays in updating live showroom inventory.")
]

for title, desc in challenges:
    p = doc.add_paragraph()
    p.add_run(f'• {title}: ').bold = True
    p.add_run(desc)

doc.add_heading('2. Proposed Solutions and Best Practices', level=3)

solutions = [
    ("Schema-on-Read and Hybrid Columnar Architectures",
     "Adopt modern lakehouse and warehouse storage patterns (e.g., Google BigQuery, Snowflake, Databricks Delta Lake) that natively support semi-structured types (such as JSON, VARIANT, or STRUCT). By storing raw semi-structured payloads in raw ingestion tables, new attributes are never lost. Downstream transformations can extract specific fields on-read without requiring immediate schema alterations."),
    ("Automated Cleaning and Unit Normalization Pipelines",
     "Implement automated transformation routines using regex parsers and look-up tables in tools like dbt or PySpark. These clean string values, extract numeric scalars, and convert divergent units to standard SI units (e.g., normalizing all engine power values to Kilowatts and all displacements to numeric cc)."),
    ("Dead-Letter Queues (DLQ) and Quarantine Patterns",
     "Build fault-tolerant pipelines where records containing schema violations, syntax errors, or corrupted payloads are routed to a Dead-Letter Queue (DLQ) or quarantine bucket rather than terminating the whole batch. Data engineers can inspect and reprocess quarantined records asynchronously."),
    ("Automated Data Quality & Contract Testing",
     "Enforce schema contracts using modern validation frameworks such as Great Expectations, Pydantic, or Apache Deequ. Essential fields (e.g., vin, brandName, modelId) are verified before data enters analytics layers, preventing broken downstream reports."),
    ("Distributed Processing and Incremental CDC",
     "Utilize distributed streaming and batch engines (e.g., Apache Spark, Kafka with Schema Registry, or cloud-native Dataflow) to parallelize JSON parsing across worker nodes, paired with Change Data Capture (CDC) to process only modified inventory items incrementally.")
]

for title, desc in solutions:
    p = doc.add_paragraph()
    p.add_run(f'• {title}: ').bold = True
    p.add_run(desc)

doc_path = r'C:\Users\mithu\OneDrive\Desktop\Internet Programmimg\Bike_Showroom_Assignment_Submission.docx'
doc.save(doc_path)
print('SUCCESS: Created', doc_path)
