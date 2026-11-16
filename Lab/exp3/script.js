/**
 * Interactivity & Diagnostics Simulator: LAMP vs WAMP Stack (exp3)
 */

document.addEventListener('DOMContentLoaded', () => {
    // Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    // Simulator State
    let isApacheRunning = false;
    let isMysqlRunning = false;

    const indApache = document.getElementById('indApache');
    const indMysql = document.getElementById('indMysql');
    const indPhp = document.getElementById('indPhp');
    const termOutput = document.getElementById('termOutput');

    const btnStartApache = document.getElementById('btnStartApache');
    const btnStartMysql = document.getElementById('btnStartMysql');
    const btnTestPhp = document.getElementById('btnTestPhp');
    const btnResetStack = document.getElementById('btnResetStack');

    function logTerminal(message, type = 'info') {
        const time = new Date().toLocaleTimeString();
        const line = document.createElement('div');
        line.className = `term-line ${type}`;
        line.innerHTML = `[${time}] ${message}`;
        termOutput.appendChild(line);
        termOutput.scrollTop = termOutput.scrollHeight;
    }

    // Toggle Apache
    btnStartApache.addEventListener('click', () => {
        if (!isApacheRunning) {
            isApacheRunning = true;
            btnStartApache.textContent = 'Stop Apache Server';
            indApache.querySelector('.status-light').className = 'status-light green';
            indApache.querySelector('.state-text').textContent = 'Online / Listening';
            logTerminal('Apache/2.4.56 HTTP Service started. Bound to TCP 0.0.0.0:80 and 0.0.0.0:443.', 'success');
            logTerminal('Loaded modules: core_module, mod_rewrite, mod_ssl, mod_headers, mod_php.', 'info');
        } else {
            isApacheRunning = false;
            btnStartApache.textContent = 'Start Apache Server';
            indApache.querySelector('.status-light').className = 'status-light red';
            indApache.querySelector('.state-text').textContent = 'Offline';
            logTerminal('Apache HTTP Server process terminated gracefully (SIGTERM). Ports released.', 'warning');
        }
    });

    // Toggle MySQL
    btnStartMysql.addEventListener('click', () => {
        if (!isMysqlRunning) {
            isMysqlRunning = true;
            btnStartMysql.textContent = 'Stop MySQL Service';
            indMysql.querySelector('.status-light').className = 'status-light green';
            indMysql.querySelector('.state-text').textContent = 'Online / Active';
            logTerminal('MySQL Community Server 8.0 initialized. Ready for client connections on socket 127.0.0.1:3306.', 'success');
            logTerminal('InnoDB engine active. Buffer pool initialized with 128MB memory allocation.', 'info');
        } else {
            isMysqlRunning = false;
            btnStartMysql.textContent = 'Start MySQL Service';
            indMysql.querySelector('.status-light').className = 'status-light red';
            indMysql.querySelector('.state-text').textContent = 'Offline';
            logTerminal('MySQL daemon stopped. Active connection pools closed.', 'warning');
        }
    });

    // Run PHP Script Simulation
    btnTestPhp.addEventListener('click', () => {
        logTerminal('Dispatching HTTP GET request: http://localhost/test_db_connect.php ...', 'info');

        if (!isApacheRunning) {
            logTerminal('ERR_CONNECTION_REFUSED: Could not establish TCP connection to port 80. Apache is NOT running!', 'error');
            return;
        }

        indPhp.querySelector('.status-light').className = 'status-light amber';
        indPhp.querySelector('.state-text').textContent = 'Executing...';

        setTimeout(() => {
            if (isMysqlRunning) {
                indPhp.querySelector('.status-light').className = 'status-light green';
                indPhp.querySelector('.state-text').textContent = 'Idle (Executed OK)';
                logTerminal('PHP Engine invoked via mod_php / PHP-FPM handler.', 'info');
                logTerminal('PDO::__construct("mysql:host=localhost;dbname=test_db", "root", "secret") -> SUCCESS (Latency: 1.8ms)', 'success');
                logTerminal('SQL: "SELECT * FROM users LIMIT 5" -> Returned 5 rows.', 'success');
                logTerminal('HTTP/1.1 200 OK | Content-Type: text/html; charset=UTF-8 | Bytes: 4120', 'success');
            } else {
                indPhp.querySelector('.status-light').className = 'status-light red';
                indPhp.querySelector('.state-text').textContent = 'Script Error';
                logTerminal('PHP Engine invoked via mod_php handler.', 'info');
                logTerminal('PHP Fatal Error: Uncaught PDOException: SQLSTATE[HY000] [2002] Connection refused. MySQL service is not active on port 3306!', 'error');
                logTerminal('HTTP/1.1 500 Internal Server Error delivered to client browser.', 'error');
            }
        }, 500);
    });

    // Stop All
    btnResetStack.addEventListener('click', () => {
        isApacheRunning = false;
        isMysqlRunning = false;
        btnStartApache.textContent = 'Start Apache Server';
        btnStartMysql.textContent = 'Start MySQL Service';

        indApache.querySelector('.status-light').className = 'status-light red';
        indApache.querySelector('.state-text').textContent = 'Offline';

        indMysql.querySelector('.status-light').className = 'status-light red';
        indMysql.querySelector('.state-text').textContent = 'Offline';

        indPhp.querySelector('.status-light').className = 'status-light gray';
        indPhp.querySelector('.state-text').textContent = 'Idle';

        logTerminal('Stack Reset: All daemon services stopped. Environment set to offline state.', 'warning');
    });
});
