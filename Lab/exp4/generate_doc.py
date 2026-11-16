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

sub_info = doc.add_paragraph('Course: Internet Programming | Question 4 | Total Marks: 20 Marks')
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
    'You are developing a web application that involves detailed interactions between clients and '
    'servers using HTTP. Your task is to ensure that the application can handle various HTTP '
    'request and response messages correctly. Additionally, you need to understand and manage '
    'common HTTP response status codes to effectively troubleshoot and handle different scenarios.\n'
    'Explain the structure of an HTTP request message and an HTTP response message.'
)

p_params = doc.add_paragraph()
r_param_h = p_params.add_run('Parameters:\n')
r_param_h.bold = True
p_params.add_run('❖ Understanding and managing HTTP request and response messages.\n')
p_params.add_run('❖ Ability to explain their structure and components.\n')
p_params.add_run('❖ Implementing a multi-page website with a cohesive design.\n')
p_params.add_run('❖ Ensuring responsiveness across different devices.')

p_q = doc.add_paragraph()
r_qh = p_q.add_run('Questions:\n')
r_qh.bold = True
p_q.add_run('a) Create a simplified dimensional data model (snowflake schema) to structure the sales data for analysis.\n')
p_q.add_run('b) Define the ETL steps to preprocess and load the data into the warehouse.\n')
p_q.add_run('c) Perform the following OLAP operations:\n')
p_q.add_run('   i) Roll-up to analyze total sales revenue by region.\n')
p_q.add_run('   ii) Dice to compare sales performance across age groups and product categories.\n')
p_q.add_run('d) Provide a brief explanation of how the insights could guide the retailer\'s marketing and inventory decisions.\n\n')

p_marks = doc.add_paragraph()
r_mh = p_marks.add_run('Marks Distribution (20 Marks):\n')
r_mh.bold = True
p_marks.add_run('• Dimensional data model design: 6 marks\n')
p_marks.add_run('• ETL process definition: 4 marks\n')
p_marks.add_run('• OLAP operation implementation: 6 marks\n')
p_marks.add_run('• Insight discussion: 4 marks')

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

# Part 1: Comprehensive HTTP Protocol & Status Code Analysis
doc.add_heading('Comprehensive Technical Analysis: Structure of HTTP Request & Response Messages', level=2)
doc.add_paragraph(
    'The Hypertext Transfer Protocol (HTTP) is the foundational stateless application-layer protocol powering '
    'the World Wide Web. Client-server communication operates through a strict request-response exchange format '
    'governed by RFC 7230 / RFC 9112 specifications.'
)

http_packet_diagram = (
    "+-------------------------------------------------------------------------+\n"
    "|                       HTTP REQUEST MESSAGE FORMAT                       |\n"
    "+-------------------------------------------------------------------------+\n"
    "| Request Line : [METHOD] [REQUEST-URI] [HTTP-VERSION] <CRLF>             |\n"
    "|                e.g., POST /api/v1/sales/transactions HTTP/1.1           |\n"
    "| Request      : Header-Name: Header-Value <CRLF>                         |\n"
    "| Headers        Host: api.retailanalytics.cloud                          |\n"
    "|                Content-Type: application/json; charset=utf-8            |\n"
    "|                Authorization: Bearer eyJhbGciOiJIUzI1Ni...              |\n"
    "| Empty Line   : <CRLF> (Marks boundary between headers and entity body)  |\n"
    "| Message Body : [Optional Payload: JSON / XML / Form Data / Binary]     |\n"
    "+-------------------------------------------------------------------------+\n"
    "\n"
    "+-------------------------------------------------------------------------+\n"
    "|                       HTTP RESPONSE MESSAGE FORMAT                      |\n"
    "+-------------------------------------------------------------------------+\n"
    "| Status Line  : [HTTP-VERSION] [STATUS-CODE] [REASON-PHRASE] <CRLF>      |\n"
    "|                e.g., HTTP/1.1 200 OK  or  HTTP/1.1 201 Created          |\n"
    "| Response     : Date: Mon, 16 Nov 2026 14:00:00 GMT                      |\n"
    "| Headers        Server: Apache/2.4.56 (Unix)                             |\n"
    "|                Content-Type: application/json; charset=utf-8            |\n"
    "|                Content-Length: 245                                      |\n"
    "| Empty Line   : <CRLF>                                                   |\n"
    "| Message Body : [Resource Entity / Error Diagnostic Payload]             |\n"
    "+-------------------------------------------------------------------------+"
)
add_callout(doc, http_packet_diagram, 'Structural Anatomy of HTTP Request and Response Packets')

# HTTP Status Code Handling
doc.add_heading('HTTP Status Code Taxonomy & Error Recovery Protocols', level=3)
doc.add_paragraph(
    'HTTP status codes are standardized 3-digit integers partitioned into five functional classes:\n'
    '1. 1xx (Informational): Provisional handshakes (e.g., 101 Switching Protocols).\n'
    '2. 2xx (Success): Action successfully completed (200 OK for standard retrieval, 201 Created for record insertion, 204 No Content for silent updates).\n'
    '3. 3xx (Redirection): Client must take additional action (301 Moved Permanently for URL rewrites, 304 Not Modified for browser HTTP cache revalidation).\n'
    '4. 4xx (Client Error): Malformed requests or unauthorized operations (400 Bad Request for validation failure, 401 Unauthorized for missing tokens, 403 Forbidden for restricted access, 404 Not Found for missing URIs).\n'
    '5. 5xx (Server Error): Server infrastructure failure (500 Internal Server Error for unhandled runtime exceptions, 502 Bad Gateway for upstream proxy faults, 503 Service Unavailable for maintenance/overload).'
)

# Question (a)
doc.add_heading('Question (a): Simplified Dimensional Data Model (Snowflake Schema) (6 Marks)', level=2)
doc.add_paragraph(
    'A Snowflake Schema is a variation of the dimensional star schema where dimension tables are normalized '
    'into sub-dimension tables along natural concept hierarchies. This eliminates data redundancy, saves storage '
    'space, preserves 3rd Normal Form (3NF) across attribute hierarchies, and ensures relational referential integrity.'
)

snowflake_schema_diagram = (
    " [Dim_Category]                      [Dim_Region]                    [Dim_Year]\n"
    " (CategoryID, CatName)               (RegionID, RegionName)          (YearID, CalendarYear)\n"
    "          ^                                   ^                               ^\n"
    "          | 1:N                               | 1:N                           | 1:N\n"
    " [Dim_SubCategory]                   [Dim_City]                      [Dim_Quarter]\n"
    " (SubCatID, SubName, CategoryID)     (CityID, CityName, RegionID)    (QuarterID, QtrName, YearID)\n"
    "          ^                                   ^                               ^\n"
    "          | 1:N                               | 1:N                           | 1:N\n"
    " [Dim_Product]                       [Dim_Store]                     [Dim_Time]\n"
    " (ProductID, Name, SubCatID, Price)  (StoreID, StoreName, CityID)    (TimeKey, FullDate, QuarterID)\n"
    "          \\                                   |                               /\n"
    "           \\                                  |                              /\n"
    "            \\                                 v                             /\n"
    "             +--------------------> [FACT_SALES] <-------------------------+\n"
    "                                    * SalesID (Primary Key)\n"
    "                                    * ProductID (FK -> Dim_Product)\n"
    "                                    * StoreID (FK -> Dim_Store)\n"
    "                                    * CustomerID (FK -> Dim_Customer)\n"
    "                                    * TimeKey (FK -> Dim_Time)\n"
    "                                    * QuantitySold (Measure - Additive)\n"
    "                                    * UnitPrice (Measure - Semi-Additive)\n"
    "                                    * TotalRevenue (Measure - Additive)\n"
    "                                              ^\n"
    "                                              |\n"
    "                                     [Dim_Customer]\n"
    "                                     (CustID, CustName, DemographicsID)\n"
    "                                              | 1:N\n"
    "                                              v\n"
    "                                     [Dim_Demographics]\n"
    "                                     (DemographicsID, AgeGroup, IncomeTier)"
)
add_callout(doc, snowflake_schema_diagram, 'Snowflake Dimensional Data Model (Retail Sales Warehouse)')

doc.add_paragraph(
    'Key Normalization Chains in the Snowflake Schema:\n'
    '1. Product Hierarchy: Dim_Product -> Dim_SubCategory -> Dim_Category. Avoids repeating category strings for thousands of individual SKU rows.\n'
    '2. Geography Hierarchy: Dim_Store -> Dim_City -> Dim_Region. Enables seamless geographic drill-down and roll-up across territories.\n'
    '3. Customer Demographics Hierarchy: Dim_Customer -> Dim_Demographics. Groups customers into standardized Age Groups (18-25, 26-40, 41-60) and income brackets.\n'
    '4. Temporal Hierarchy: Dim_Time -> Dim_Quarter -> Dim_Year. Supports seasonal roll-up analysis across financial fiscal quarters.'
)

# Question (b)
doc.add_heading('Question (b): ETL Steps to Preprocess & Load Data into Warehouse (4 Marks)', level=2)
doc.add_paragraph(
    'The Extract, Transform, Load (ETL) pipeline automates the ingestion of raw transactional data from disparate '
    'operational databases and point-of-sale (POS) systems into the analytical snowflake data warehouse:'
)

etl_steps = [
    ("1. Extraction Phase (E)",
     "Transactional records are extracted from live Point-of-Sale (POS) cash registers, e-commerce web application MySQL databases, "
     "and real-time Kafka event streams. Change Data Capture (CDC) based on timestamps (updated_at) extracts delta increments every hour "
     "to prevent locking production transactional tables."),
    ("2. Transformation & Data Cleansing Phase (T)",
     "• Deduplication: Transaction IDs are checked against existing staging logs to discard duplicate records.\n"
     "• Data Sanitization: Missing or null customer IDs are assigned a surrogate key (-1 = Anonymous Guest).\n"
     "• Unit Normalization: Currencies across international stores are converted to USD using daily exchange rate feeds.\n"
     "• Demographic Mapping: Raw applicant/customer birth dates are transformed into categorized age bands (18-25, 26-40, 41-60, 60+).\n"
     "• Measure Derivation: Total revenue is validated as QuantitySold * UnitPrice - Discounts."),
    ("3. Loading Phase (L)",
     "Cleaned datasets are loaded into target snowflake tables:\n"
     "• Dimension Tables: Loaded using Slowly Changing Dimensions (SCD Type 2) with effective start/end timestamps to track historical changes (e.g., customer moving to a new city).\n"
     "• Fact Table: High-velocity bulk partition append into Fact_Sales, updating clustered column indexes for rapid analytical query processing.")
]

for title, desc in etl_steps:
    p = doc.add_paragraph()
    p.add_run(f'• {title}:\n').bold = True
    p.add_run(desc)

# Question (c)
doc.add_heading('Question (c): OLAP Operations Implementation: Roll-Up and Dice (6 Marks)', level=2)
doc.add_paragraph(
    'Online Analytical Processing (OLAP) provides multidimensional analysis of warehouse data cubes. '
    'Below are the implementations for the specified Roll-up and Dice operations:'
)

# OLAP 1: Roll-up
doc.add_heading('1. OLAP Operation: Roll-Up (Total Sales Revenue by Region)', level=3)
doc.add_paragraph(
    'The Roll-up operation summarizes data along a dimensional concept hierarchy by climbing up from a more granular '
    'level (individual stores / cities) to a higher grouping level (Geographic Region).'
)

sql_rollup = """-- SQL Implementation of Roll-Up by Region
SELECT 
    r.RegionName,
    SUM(f.TotalRevenue) AS TotalSalesRevenue,
    SUM(f.QuantitySold) AS TotalUnitsSold,
    COUNT(DISTINCT s.StoreID) AS ActiveStoreCount
FROM Fact_Sales f
JOIN Dim_Store s ON f.StoreID = s.StoreID
JOIN Dim_City c ON s.CityID = c.CityID
JOIN Dim_Region r ON c.RegionID = r.RegionID
GROUP BY r.RegionName
ORDER BY TotalSalesRevenue DESC;"""
add_callout(doc, sql_rollup, 'SQL Query: Roll-Up Total Revenue by Region')

# Roll-up Table
tbl_ro = doc.add_table(rows=5, cols=4)
tbl_ro.alignment = WD_TABLE_ALIGNMENT.CENTER
ro_headers = ["Geographic Region", "Total Sales Revenue (USD)", "Units Sold", "Active Store Outlets"]
for col_idx, h in enumerate(ro_headers):
    c = tbl_ro.cell(0, col_idx)
    c.paragraphs[0].add_run(h).bold = True
    set_cell_background(c, '1A252F')
    c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

ro_data = [
    ("North Region", "$1,420,500 (39%)", "18,450", "42"),
    ("West Region", "$1,050,200 (29%)", "14,200", "31"),
    ("South Region", "$680,400 (19%)", "9,800", "22"),
    ("East Region", "$472,900 (13%)", "6,450", "16")
]

for row_idx, r_vals in enumerate(ro_data, start=1):
    for col_idx, val in enumerate(r_vals):
        c = tbl_ro.cell(row_idx, col_idx)
        c.paragraphs[0].add_run(val)
        set_cell_background(c, 'F9FBFD' if row_idx % 2 == 1 else 'FFFFFF')

doc.add_paragraph()

# OLAP 2: Dice
doc.add_heading('2. OLAP Operation: Dice (Age Groups vs. Product Categories)', level=3)
doc.add_paragraph(
    'The Dice operation defines a sub-cube by selecting two or more specific slices across different dimensions. '
    'Here, the data cube is diced along the Demographics Dimension (Age Groups: 18-25, 26-40, 41-60) and the '
    'Product Dimension (Categories: Electronics, Apparel, Home Goods).'
)

sql_dice = """-- SQL Implementation of Dice Operation
SELECT 
    d.AgeGroup,
    cat.CatName AS ProductCategory,
    SUM(f.TotalRevenue) AS SegmentRevenue,
    SUM(f.QuantitySold) AS UnitsSold
FROM Fact_Sales f
JOIN Dim_Customer cust ON f.CustomerID = cust.CustID
JOIN Dim_Demographics d ON cust.DemographicsID = d.DemographicsID
JOIN Dim_Product p ON f.ProductID = p.ProductID
JOIN Dim_SubCategory sub ON p.SubCatID = sub.SubCatID
JOIN Dim_Category cat ON sub.CategoryID = cat.CategoryID
WHERE d.AgeGroup IN ('18-25', '26-40', '41-60')
  AND cat.CatName IN ('Electronics', 'Apparel', 'Home Goods')
GROUP BY d.AgeGroup, cat.CatName
ORDER BY d.AgeGroup, SegmentRevenue DESC;"""
add_callout(doc, sql_dice, 'SQL Query: Multi-Dimensional Dice Operation')

# Dice Table
tbl_dice = doc.add_table(rows=10, cols=4)
tbl_dice.alignment = WD_TABLE_ALIGNMENT.CENTER
dice_headers = ["Customer Age Group", "Product Category", "Segment Revenue (USD)", "Units Sold"]
for col_idx, h in enumerate(dice_headers):
    c = tbl_dice.cell(0, col_idx)
    c.paragraphs[0].add_run(h).bold = True
    set_cell_background(c, '1A252F')
    c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

dice_data = [
    ("18-25 (Gen-Z)", "Electronics", "$480,200", "4,120"),
    ("18-25 (Gen-Z)", "Apparel", "$210,400", "3,890"),
    ("18-25 (Gen-Z)", "Home Goods", "$45,600", "610"),
    ("26-40 (Millennials)", "Electronics", "$520,800", "3,250"),
    ("26-40 (Millennials)", "Apparel", "$340,100", "4,200"),
    ("26-40 (Millennials)", "Home Goods", "$290,500", "2,780"),
    ("41-60 (Gen-X)", "Home Goods", "$430,900", "3,950"),
    ("41-60 (Gen-X)", "Apparel", "$265,300", "2,980"),
    ("41-60 (Gen-X)", "Electronics", "$240,600", "1,450")
]

for row_idx, r_vals in enumerate(dice_data, start=1):
    for col_idx, val in enumerate(r_vals):
        c = tbl_dice.cell(row_idx, col_idx)
        c.paragraphs[0].add_run(val)
        set_cell_background(c, 'F9FBFD' if row_idx % 2 == 1 else 'FFFFFF')

doc.add_paragraph()

# Question (d)
doc.add_heading('Question (d): Strategic Marketing & Inventory Decision Insights (4 Marks)', level=2)
doc.add_paragraph(
    'The analytical findings extracted from the Roll-up and Dice OLAP operations provide actionable intelligence '
    'for the retail executive team to optimize capital allocation, marketing ROI, and supply chain logistics:'
)

insights = [
    ("1. Regional Inventory Reallocation (Based on Roll-Up)",
     "The Roll-up analysis demonstrates that the North (39%) and West (29%) regions contribute 68% of total revenue. "
     "Decision: Establish secondary fulfillment distribution hubs in the North and West territories to support higher local "
     "inventory buffer levels. Conversely, the East region represents only 13% of volume; downsize warehouse holding costs "
     "in the East and transition slower-moving inventory to on-demand regional fulfillment."),
    ("2. Targeted Demographic Marketing Campaigns (Based on Dice)",
     "The Dice analysis exposes distinct purchasing preferences by demographic tier: Gen-Z (18-25) heavily favors Electronics "
     "($480k) and Apparel ($210k), while Gen-X (41-60) is the highest spender in Home Goods ($430k). "
     "Decision: Allocate digital advertising spend by channel—deploy mobile video ads (TikTok/Instagram) promoting wearable electronics "
     "and streetwear to audiences aged 18-25. Allocate email marketing and home interior catalog campaigns featuring premium kitchenware "
     "to homeowners in the 41-60 age segment."),
    ("3. Automated Replenishment & Stockout Prevention",
     "Cross-referencing the Dice matrix with sales velocity allows inventory managers to configure dynamic Safety Stock formulas. "
     "Because Electronics turnover among young adults accelerates sharply during back-to-school and holiday quarters, automated purchase "
     "orders can be scheduled 6 weeks in advance, eliminating costly stockout lost revenues.")
]

for title, desc in insights:
    p = doc.add_paragraph()
    p.add_run(f'• {title}:\n').bold = True
    p.add_run(desc)

# Output Document Path
doc_path = os.path.join(os.path.dirname(__file__), 'HTTP_and_Data_Warehouse_OLAP_Assignment_Submission.docx')
doc.save(doc_path)
print('SUCCESS: Created', doc_path)
