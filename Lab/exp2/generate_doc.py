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

sub_info = doc.add_paragraph('Course: Internet Programming | Question 2 | Total Marks: 20 Marks')
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
    'You are tasked with designing a job application form for a company\'s career page. The form '
    'should be user-friendly and visually appealing. The form needs to capture the applicant\'s '
    'personal information, including their name, highest qualified degree, and gender. Additionally, '
    'it should have a "Submit" button to send the application and a "Cancel" button to reset the form '
    'or go back to the previous page.'
)

p_params = doc.add_paragraph()
r_param_h = p_params.add_run('Parameters:\n')
r_param_h.bold = True
p_params.add_run('❖ The job application form should be user-friendly and visually appealing.\n')
p_params.add_run('❖ It must capture the applicant\'s personal information, including their name, highest qualification, and gender.\n')
p_params.add_run('❖ The form must have a "Submit" button to send the application and a "Cancel" button to reset the form.')

p_q = doc.add_paragraph()
r_qh = p_q.add_run('Questions:\n')
r_qh.bold = True
p_q.add_run('a) Design the HTML structure of the job application form\n')
p_q.add_run('b) Add client-side validation to the form using JavaScript to ensure the data is accurate and complete before submission.\n')
p_q.add_run('c) Implement basic validation for fields such as name (required), email (valid format), and gender (required).\n\n')

p_marks = doc.add_paragraph()
r_mh = p_marks.add_run('Marks Distribution (20 Marks):\n')
r_mh.bold = True
p_marks.add_run('• HTML form structure: 3 marks\n')
p_marks.add_run('• JavaScript client-side validation: 7 marks\n')
p_marks.add_run('• CSS Styling for Visual Appeal: 5 marks\n')
p_marks.add_run('• Submit and Cancel Button Functionality: 5 marks')

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
doc.add_heading('Question (a): Design the HTML Structure of the Job Application Form (3 Marks)', level=2)
doc.add_paragraph(
    'The HTML structure of the job application form is engineered using semantic HTML5 elements. '
    'The structure organizes information into two logically distinct fieldsets: "Applicant Personal Details" '
    'and "Role Preference & Professional Summary". Each field is wrapped in a dedicated form-row container '
    'featuring an explicit <label>, standard input controls (<input>, <select>, <textarea>), and a dedicated '
    '<span> container for real-time validation error messaging.'
)

diagram_text = (
    "+-------------------------------------------------------------------------+\n"
    "|                       CAREER PAGE: HEADER BANNER                        |\n"
    "|         Company Badge: NexGen Careers | Title & Application Scope        |\n"
    "+-------------------------------------------------------------------------+\n"
    "|                        FORM CARD CONTAINER                              |\n"
    "|  +-------------------------------------------------------------------+  |\n"
    "|  | FIELDSET 1: Applicant Personal Details                            |  |\n"
    "|  |  * Full Name           : <input type=\"text\" id=\"applicantName\">       |  |\n"
    "|  |  * Email Address       : <input type=\"email\" id=\"applicantEmail\">     |  |\n"
    "|  |  * Contact Phone       : <input type=\"tel\" id=\"applicantPhone\">       |  |\n"
    "|  |  * Highest Degree      : <select id=\"highestDegree\"> (Options)       |  |\n"
    "|  |  * Gender Selection    : Radio buttons (Male / Female / Other / etc.)  |  |\n"
    "|  +-------------------------------------------------------------------+  |\n"
    "|  | FIELDSET 2: Role Preference & Summary                             |  |\n"
    "|  |  * Position Applied    : <select id=\"targetPosition\"> (Roles)         |  |\n"
    "|  |  * Brief Statement     : <textarea id=\"coverNote\"> + Char Counter     |  |\n"
    "|  +-------------------------------------------------------------------+  |\n"
    "|  | FORM ACTIONS:                                                     |  |\n"
    "|  |  [ ✓ Submit Application (btn-primary) ]                           |  |\n"
    "|  |  [ ✕ Cancel / Reset Form (btn-secondary) ]                        |  |\n"
    "|  +-------------------------------------------------------------------+  |\n"
    "+-------------------------------------------------------------------------+"
)
add_callout(doc, diagram_text, 'Visual Form Layout & Semantic Hierarchy')

# Read HTML code from index.html
with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r', encoding='utf-8') as f:
    html_code = f.read()

add_callout(doc, html_code, 'Complete HTML5 Markup: index.html')

# Question (b)
doc.add_heading('Question (b): Client-Side Validation Using JavaScript (7 Marks)', level=2)
doc.add_paragraph(
    'Client-side validation is implemented in JavaScript (script.js) to enforce rigorous data validation '
    'before form dispatch. This avoids redundant roundtrips to the server, protects server resources, '
    'and provides immediate visual guidance to the applicant.'
)

doc.add_paragraph(
    'Core Validation Architecture:\n'
    '1. Event Interception: The form\'s "submit" event is intercepted using event.preventDefault() to '
    'inhibit unvalidated browser submission.\n'
    '2. Multi-Stage Lifecycle: Validations execute both on input events (real-time feedback as the user types) '
    'and on blur events (when focus leaves an input field), plus a master sweep on form submission.\n'
    '3. Dynamic DOM Feedback: Invalid controls receive the CSS class "is-invalid" (red outline and light red fill) '
    'and display an error string in the corresponding error <span>. Valid controls receive "is-valid" (green border).\n'
    '4. Accessibility & Viewport Focus: If validation fails, the UI renders a top banner alert and automatically '
    'scrolls the viewport to the first offending input element.'
)

# Read JavaScript code from script.js
with open(os.path.join(os.path.dirname(__file__), 'script.js'), 'r', encoding='utf-8') as f:
    js_code = f.read()

add_callout(doc, js_code, 'Complete Client-Side JavaScript Logic: script.js')

# Question (c)
doc.add_heading('Question (c): Specific Validation Rules: Name, Email, Gender & Degree', level=2)
doc.add_paragraph(
    'The implementation enforces exact field-level validation rules as requested by the parameters:'
)

rules = [
    ("1. Applicant Name (Required)",
     "Enforced via regex /^[A-Za-z\\s.'-]{3,60}$/. The name field cannot be empty, must contain at least 3 alphabetic characters, and rejects malicious script tags, numbers, or unsupported special symbols."),
    ("2. Email Address (Valid Format)",
     "Enforced via RFC 5322 compliant regex /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/. Ensures presence of an alphanumeric user prefix, the '@' separator, a domain name, and a recognized top-level domain (TLD) of at least two letters."),
    ("3. Highest Qualified Degree (Required)",
     "Enforced by checking degreeSelect.value !== ''. The dropdown offers comprehensive degree levels (B.E./B.Tech, B.Sc/BCA, M.Tech/M.Sc, MBA, Ph.D.). An unselected default prompt triggers a validation error."),
    ("4. Gender Selection (Required)",
     "Enforced by evaluating document.querySelector('input[name=\"gender\"]:checked'). If null, genderError indicates mandatory selection. Supports inclusive identity options (Male, Female, Non-Binary, Prefer Not to Say)."),
    ("5. Phone Number & Role Preference",
     "Contact number requires minimum 7 numeric digits using phone regex; position selection verifies applicant career alignment.")
]

for title, desc in rules:
    p = doc.add_paragraph()
    p.add_run(f'• {title}: ').bold = True
    p.add_run(desc)

# CSS Styling for Visual Appeal (5 Marks)
doc.add_heading('CSS Styling for Visual Appeal (5 Marks)', level=2)
doc.add_paragraph(
    'The design adheres to clean, modern SaaS corporate aesthetics using custom CSS3 properties (CSS Variables, '
    'Flexbox, multi-level box shadows, subtle borders, and smooth transitions). '
    'The form is fully responsive across mobile screens and desktop monitors.'
)

# Read CSS code from style.css
with open(os.path.join(os.path.dirname(__file__), 'style.css'), 'r', encoding='utf-8') as f:
    css_code = f.read()

add_callout(doc, css_code, 'Complete CSS3 Stylesheet: style.css')

# Submit and Cancel Button Functionality (5 Marks)
doc.add_heading('Submit and Cancel Button Functionality (5 Marks)', level=2)
doc.add_paragraph(
    'The form provides two prominent action buttons with distinct visual hierarchies and behavioral handlers:\n\n'
    '1. Submit Application Button (.btn-primary):\n'
    '   - Triggers the comprehensive validation pipeline across all input fields.\n'
    '   - If valid, opens an animated confirmation modal dialog displaying the sanitized candidate submission summary.\n'
    '   - Prevents duplicate dispatches and displays error banners if criteria are not satisfied.\n\n'
    '2. Cancel / Reset Form Button (.btn-secondary):\n'
    '   - Bound to an explicit JavaScript confirmation prompt: confirm("Are you sure you want to cancel and reset the job application form?").\n'
    '   - Upon user confirmation, resets all input fields (form.reset()), clears all CSS validation states (.is-valid and .is-invalid), '
    'clears all error text spans, resets character counters, and restores the form to its initial pristine state.'
)

# Output Document Path
doc_path = os.path.join(os.path.dirname(__file__), 'Job_Application_Form_Assignment_Submission.docx')
doc.save(doc_path)
print('SUCCESS: Created', doc_path)
