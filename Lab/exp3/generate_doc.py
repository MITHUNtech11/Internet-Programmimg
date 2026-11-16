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

sub_info = doc.add_paragraph('Course: Internet Programming | Question 3 | Total Marks: 20 Marks')
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
    'You have been assigned the task of establishing a development environment for a new web '
    'application project. The team is considering whether to utilize the LAMP stack or the '
    'WAMP stack. They need a clear understanding of the essential components of these stacks, '
    'their functions, and the installation procedures on both Linux and Windows systems. '
    'Additionally, they seek to grasp the role of the Apache web server within the stack and how '
    'it integrates with the other components.'
)

p_params = doc.add_paragraph()
r_param_h = p_params.add_run('Parameters:\n')
r_param_h.bold = True
p_params.add_run('❖ The team is considering whether to use the LAMP stack (Linux, Apache, MySQL, PHP) or WAMP stack (Windows, Apache, MySQL, PHP) for the web application development environment.\n')
p_params.add_run('❖ The team needs to understand the components of each stack, their functions, installation procedures on Linux and Windows systems, and the role of Apache in both environments.')

p_q = doc.add_paragraph()
r_qh = p_q.add_run('Questions:\n')
r_qh.bold = True
p_q.add_run('(1) Explain the key components of the LAMP stack and their roles in web development.\n')
p_q.add_run('(2) Explain the key components of the WAMP stack and how it compares to the LAMP stack.\n')
p_q.add_run('(3) Describe the role of Apache web server within both stacks and how it integrates with other components.\n\n')

p_marks = doc.add_paragraph()
r_mh = p_marks.add_run('Marks Distribution (20 Marks):\n')
r_mh.bold = True
p_marks.add_run('• Explanation of LAMP stack components: 7 marks\n')
p_marks.add_run('• Explanation of WAMP stack components: 7 marks\n')
p_marks.add_run('• Role of Apache web server: 6 marks')

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

# Question (1)
doc.add_heading('Question (1): Key Components of the LAMP Stack & Their Roles in Web Development (7 Marks)', level=2)
doc.add_paragraph(
    'The LAMP stack is an industry-standard open-source web platform architecture designed for deploying '
    'high-performance dynamic web applications. The acronym stands for Linux, Apache, MySQL, and PHP/Perl/Python. '
    'Each layer fulfills a specialized role in the multi-tiered web architecture:'
)

lamp_components = [
    ("1. Linux (Operating System Layer)",
     "Linux serves as the foundational operating system. It provides kernel-level process isolation, efficient memory paging, "
     "high-speed TCP/IP networking, and strict POSIX file permissions (chmod/chown). As an open-source, non-proprietary OS, "
     "Linux delivers rock-solid reliability, low CPU overhead, and native daemon process orchestration via systemd."),
    ("2. Apache (Web Server Layer)",
     "Apache HTTP Server acts as the HTTP daemon (httpd/apache2) listening on ports 80 and 443. It intercepts incoming client requests, "
     "terminates SSL/TLS certificates, evaluates routing rules (.htaccess, mod_rewrite), serves static content (HTML, CSS, JS, media) "
     "with zero CPU processing overhead, and delegates dynamic script requests to PHP."),
    ("3. MySQL (Relational Database Management System Layer)",
     "MySQL provides the persistent data tier. It organizes application information into structured tables with strict relational integrity, "
     "foreign key constraints, and ACID transactions through the InnoDB engine. It executes SQL queries dispatched by the backend application, "
     "supporting indices, connection pooling, and replication."),
    ("4. PHP (Server-Side Scripting / Application Logic Layer)",
     "PHP is the server-side programming language that executes backend business logic. It reads incoming HTTP payloads ($_GET, $_POST, $_COOKIE), "
     "authenticates user sessions, queries MySQL databases using object-oriented drivers (PDO / MySQLi), compiles dynamic HTML markup, and sends "
     "it back to Apache for delivery to the client.")
]

for title, desc in lamp_components:
    p = doc.add_paragraph()
    p.add_run(f'• {title}:\n').bold = True
    p.add_run(desc)

lamp_flow = (
    "+-------------------------------------------------------------------------+\n"
    "|                       LAMP ARCHITECTURE WORKFLOW                        |\n"
    "+-------------------------------------------------------------------------+\n"
    "|  User Browser  --->  [Port 80/443]  --->  Apache Web Server (Linux)     |\n"
    "|                                                    |                    |\n"
    "|                                  Delegates .php to | (mod_php / FPM)    |\n"
    "|                                                    v                    |\n"
    "|                                           PHP Engine (Business Logic)   |\n"
    "|                                                    |                    |\n"
    "|                                 SQL Queries via PDO| (Socket/Port 3306) |\n"
    "|                                                    v                    |\n"
    "|                                            MySQL Database Storage       |\n"
    "+-------------------------------------------------------------------------+"
)
add_callout(doc, lamp_flow, 'LAMP Stack Architectural Flow')

# Linux Installation Procedure
doc.add_heading('Linux (Ubuntu/Debian) LAMP Installation Procedure', level=3)
linux_commands = """# Step 1: Update Linux Package Repository
sudo apt update && sudo apt upgrade -y

# Step 2: Install Apache HTTP Server
sudo apt install apache2 -y
sudo systemctl enable apache2
sudo systemctl start apache2

# Step 3: Install MySQL Server & Secure Installation
sudo apt install mysql-server -y
sudo mysql_secure_installation

# Step 4: Install PHP and Essential Extensions
sudo apt install php libapache2-mod-php php-mysql php-curl php-gd php-mbstring php-xml -y

# Step 5: Restart Apache to Register PHP Module
sudo systemctl restart apache2

# Step 6: Test Installation with info.php
echo "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php"""
add_callout(doc, linux_commands, 'Bash Commands: Linux LAMP Setup')

# Question (2)
doc.add_heading('Question (2): Key Components of the WAMP Stack & Comparison to LAMP (7 Marks)', level=2)
doc.add_paragraph(
    'The WAMP stack substitutes the Linux operating system with Microsoft Windows (Windows, Apache, MySQL, PHP). '
    'It is commonly distributed as unified bundled software packages such as WampServer or XAMPP, providing a graphical '
    'dashboard, system tray controllers, and automated configuration of all services for Windows environments.'
)

wamp_components = [
    ("1. Windows (Operating System Layer)",
     "Microsoft Windows (Windows 10/11 or Windows Server) provides the OS environment. Developers enjoy an intuitive GUI, "
     "broad hardware compatibility, and seamless integration with Windows IDEs (VS Code, PhpStorm). However, Windows uses "
     "the Windows NT kernel, NTFS file system, and different thread/process management than Linux."),
    ("2. Apache for Windows (Win32 / Win64)",
     "Apache is compiled as a native Windows service (Apache2.4.exe). Rather than using POSIX process forks, it utilizes "
     "the multithreaded mpm_winnt module, where a single control process spawns multiple worker threads."),
    ("3. MySQL for Windows",
     "Runs as a Windows Background Service (mysqld.exe). It comes pre-packaged with phpMyAdmin, an intuitive browser-based "
     "database administration panel accessible at http://localhost/phpmyadmin."),
    ("4. PHP for Windows",
     "Uses Windows thread-safe (TS) binary builds of the PHP interpreter, configured through php.ini to dynamically load "
     "extension dynamic-link libraries (.dll files, e.g. php_mysqli.dll, php_pdo_mysql.dll).")
]

for title, desc in wamp_components:
    p = doc.add_paragraph()
    p.add_run(f'• {title}:\n').bold = True
    p.add_run(desc)

# Comparison Table
doc.add_heading('Comprehensive Technical Comparison: LAMP vs. WAMP', level=3)

tbl = doc.add_table(rows=7, cols=3)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Evaluation Criteria", "LAMP Stack (Linux)", "WAMP Stack (Windows)"]
for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.paragraphs[0].add_run(h).bold = True
    cell.paragraphs[0].runs[0].font.name = 'Arial'
    cell.paragraphs[0].runs[0].font.size = Pt(10)
    set_cell_background(cell, '1A252F')
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

comparison_data = [
    ("Operating System", "Linux (Ubuntu, Debian, CentOS, RHEL)", "Microsoft Windows (10/11/Server)"),
    ("Primary Use Case", "Production cloud servers, CI/CD, live hosting", "Local developer desktops, rapid prototyping"),
    ("File Name Case Sensitivity", "Case-sensitive (script.php != Script.php)", "Case-insensitive (script.php == Script.php)"),
    ("Path Separation", "Forward slash (/var/www/html/)", "Backslash (C:\\wamp64\\www\\)"),
    ("Process Architecture", "Process-forking MPM (prefork/worker/event)", "Multithreaded Windows MPM (mpm_winnt)"),
    ("Cost & Licensing", "100% Free and Open Source (FOSS)", "FOSS stack, but Windows OS requires license")
]

for row_idx, row_vals in enumerate(comparison_data, start=1):
    for col_idx, val in enumerate(row_vals):
        c = tbl.cell(row_idx, col_idx)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = 'Arial'
        r.font.size = Pt(9)
        if col_idx == 0:
            r.bold = True
        set_cell_background(c, 'F9FBFD' if row_idx % 2 == 1 else 'FFFFFF')

doc.add_paragraph()

# Windows Installation Procedure
doc.add_heading('Windows WAMP Installation Procedure', level=3)
windows_steps = """Step 1: Install Visual C++ Redistributable Prerequisites
Download and install Microsoft Visual C++ Redistributable 2012-2022 (both x86 and x64).
These C++ runtimes are strictly required by Apache and PHP binaries on Windows.

Step 2: Download WampServer Installer
Visit official website: https://www.wampserver.com/en/
Download WampServer 3.x (64-bit). Run installer as Administrator.

Step 3: Specify Installation Directory
Set destination path to C:\\wamp64 (root directory for web projects is C:\\wamp64\\www\\).

Step 4: Configure Default Browser & Text Editor
Select preferred browser (e.g. Chrome) and text editor (e.g. VS Code or Notepad++).

Step 5: Launch WampServer & Check Status
Launch WampServer from desktop shortcut. Look at system tray icon:
- Red: Both services offline.
- Orange: One service running, one failed (often port conflict).
- Green: All services (Apache, MySQL) operating perfectly.

Step 6: Verify Deployment
Open web browser and navigate to:
- Dashboard:  http://localhost
- phpMyAdmin: http://localhost/phpmyadmin"""
add_callout(doc, windows_steps, 'Windows WAMP Setup Walkthrough')

# Question (3)
doc.add_heading('Question (3): Role of Apache Web Server & Component Integration (6 Marks)', level=2)
doc.add_paragraph(
    'The Apache HTTP Web Server functions as the core traffic controller, security perimeter, and orchestrator '
    'of the entire stack. Without Apache, web browsers cannot establish HTTP connections, route URLs, or invoke '
    'server-side PHP scripts.'
)

apache_roles = [
    ("1. Network Port Binding & Request Listening",
     "Apache binds to standard TCP port 80 (HTTP) and port 443 (HTTPS). It manages incoming socket connections, performs "
     "TCP 3-way handshakes, and maintains persistent Keep-Alive connections to optimize client-server latency."),
    ("2. Static Content Routing vs Dynamic Script Execution",
     "When an HTTP GET request requests a static resource (.html, .css, .js, .png), Apache directly streams the raw binary/text "
     "from the file system to the network socket using the operating system's zero-copy kernel routines (sendfile). "
     "When the requested URI ends in .php, Apache delegates execution to the PHP engine."),
    ("3. PHP Module Integration (mod_php vs PHP-FPM)",
     "In traditional LAMP/WAMP deployments, Apache embeds the PHP runtime directly into its worker threads via mod_php (libapache2-mod-php). "
     "Apache passes HTTP request headers, environment parameters, and query payloads into PHP's global arrays ($_SERVER, $_GET, $_POST). "
     "In modern high-concurrency setups, Apache forwards requests via FastCGI (mod_proxy_fcgi) to a detached PHP-FPM pool."),
    ("4. Database Security Gateway & MySQL Insulation",
     "Apache shields the MySQL database from direct internet exposure. Remote users can never connect to MySQL port 3306 directly; "
     "instead, the PHP script executed inside Apache acts as the trusted broker. PHP establishes an internal loopback socket connection "
     "to MySQL (localhost:3306), executes parameterized SQL statements, and prevents unauthorized external access."),
    ("5. Virtual Host Configuration & URL Rewriting",
     "Apache enables hosting multiple independent domains/projects on a single physical machine via Name-Based Virtual Hosts "
     "(<VirtualHost *:80>). It also leverages mod_rewrite and .htaccess files to translate human-friendly URLs (e.g., /careers/apply) "
     "into server script parameters (/index.php?route=apply).")
]

for title, desc in apache_roles:
    p = doc.add_paragraph()
    p.add_run(f'• {title}:\n').bold = True
    p.add_run(desc)

# Apache Configuration Callout
apache_conf = """# Sample Apache VirtualHost Configuration (apache2.conf / httpd.conf)
<VirtualHost *:80>
    ServerAdmin webmaster@company.com
    ServerName myapp.local
    DocumentRoot "/var/www/html/myapp"

    # Directory Permissions and .htaccess overrides
    <Directory "/var/www/html/myapp">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # PHP Handler Delegation
    <FilesMatch \\.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>

    # Custom Logging
    ErrorLog ${APACHE_LOG_DIR}/myapp_error.log
    CustomLog ${APACHE_LOG_DIR}/myapp_access.log combined
</VirtualHost>"""
add_callout(doc, apache_conf, 'Apache VirtualHost Configuration Directive')

# Output Document Path
doc_path = os.path.join(os.path.dirname(__file__), 'LAMP_vs_WAMP_Stack_Assignment_Submission.docx')
doc.save(doc_path)
print('SUCCESS: Created', doc_path)
