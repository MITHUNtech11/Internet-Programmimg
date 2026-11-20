document.addEventListener('DOMContentLoaded', () => {
    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanels.forEach(p => p.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // HTTP Simulator
    const btnRun = document.getElementById('btnRunHttp');
    const btnStep = document.getElementById('btnStepHttp');
    const btnReset = document.getElementById('btnResetHttp');
    const items = document.querySelectorAll('.waterfall-item');
    const headerCode = document.getElementById('headerCode');

    let currentStep = 0;
    const stepPackets = [
        `DNS LOOKUP:
QUERY: api.techflow.io IN A
ANSWER: api.techflow.io -> 104.21.42.12 (TTL 300)
STATUS: NOERROR`,
        `TCP 3-WAY HANDSHAKE:
[Client] -> SYN Seq=0 -> [Server:443]
[Server] -> SYN-ACK Seq=0 Ack=1 -> [Client]
[Client] -> ACK Seq=1 Ack=1 -> [Server]
SOCKET ESTABLISHED.`,
        `TLS 1.3 NEGOTIATION:
ClientHello: TLS_AES_128_GCM_SHA256, SNI=api.techflow.io
ServerHello: KeyExchange=X25519, Certificate Validated
Handshake Complete. Session Encrypted.`,
        `HTTP GET REQUEST DISPATCH:
GET /products/hypercore-x1 HTTP/1.1
Host: api.techflow.io
User-Agent: Mozilla/5.0 Chrome/130.0
Accept: text/html,application/xhtml+xml
Connection: keep-alive

HTTP RESPONSE RECEIVED:
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 14280`,
        `FETCHING DEPENDENT ASSETS:
-> GET /style.css (200 OK - 8KB)
-> GET /app.js (200 OK - 12KB)
-> GET /device.svg (304 Not Modified - 4KB)
DOM Complete. Event 'load' fired.`
    ];

    function renderStep(idx) {
        items.forEach((item, i) => {
            const bar = item.querySelector('.w-bar');
            if (i < idx) {
                item.className = 'waterfall-item done';
                bar.style.width = '100%';
            } else if (i === idx) {
                item.className = 'waterfall-item active';
                bar.style.width = '80%';
            } else {
                item.className = 'waterfall-item';
                bar.style.width = '0%';
            }
        });
        if (idx < stepPackets.length) {
            headerCode.textContent = stepPackets[idx];
        }
    }

    btnStep.addEventListener('click', () => {
        if (currentStep < items.length) {
            renderStep(currentStep);
            currentStep++;
        }
    });

    btnRun.addEventListener('click', () => {
        currentStep = 0;
        let timer = setInterval(() => {
            if (currentStep < items.length) {
                renderStep(currentStep);
                currentStep++;
            } else {
                clearInterval(timer);
            }
        }, 600);
    });

    btnReset.addEventListener('click', () => {
        currentStep = 0;
        items.forEach(item => {
            item.className = 'waterfall-item';
            item.querySelector('.w-bar').style.width = '0%';
        });
        headerCode.textContent = `Awaiting network simulation... Click "Simulate Full HTTP Sequence".`;
    });
});
