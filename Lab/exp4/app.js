/**
 * Interactive Logic: HTTP Protocol Inspector & Snowflake OLAP Console (exp4)
 */

document.addEventListener('DOMContentLoaded', () => {
    // Mode Switcher
    const btnShowHttp = document.getElementById('btnShowHttp');
    const btnShowOlap = document.getElementById('btnShowOlap');
    const httpModule = document.getElementById('httpModule');
    const olapModule = document.getElementById('olapModule');

    btnShowHttp.addEventListener('click', () => {
        btnShowHttp.classList.add('active');
        btnShowOlap.classList.remove('active');
        httpModule.classList.add('active');
        olapModule.classList.remove('active');
    });

    btnShowOlap.addEventListener('click', () => {
        btnShowOlap.classList.add('active');
        btnShowHttp.classList.remove('active');
        olapModule.classList.add('active');
        httpModule.classList.remove('active');
    });

    // HTTP Inspector Logic
    const httpMethod = document.getElementById('httpMethod');
    const httpEndpoint = document.getElementById('httpEndpoint');
    const simulateScenario = document.getElementById('simulateScenario');
    const btnSendHttp = document.getElementById('btnSendHttp');
    const rawRequestOutput = document.getElementById('rawRequestOutput');
    const rawResponseOutput = document.getElementById('rawResponseOutput');
    const statusTag = document.getElementById('statusTag');

    function updateHttpInspector() {
        const method = httpMethod.value;
        const endpoint = httpEndpoint.value;
        const scenario = simulateScenario.value;
        const dateStr = new Date().toUTCString();

        // Sample Request Payload if POST/PUT
        let bodyPayload = '';
        if (method === 'POST' || method === 'PUT') {
            bodyPayload = JSON.stringify({
                transactionId: "TXN-984210",
                storeId: "STR-NORTH-04",
                productId: "PRD-ELEC-550",
                quantity: 2,
                unitPrice: 199.99,
                customerId: "CUST-8831"
            }, null, 2);
        }

        // Construct Raw Request
        let reqText = `${method} ${endpoint} HTTP/1.1\r\n`;
        reqText += `Host: api.retailanalytics.cloud\r\n`;
        reqText += `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n`;
        reqText += `Accept: application/json, text/plain, */*\r\n`;
        reqText += `Accept-Language: en-US,en;q=0.9\r\n`;
        reqText += `Connection: keep-alive\r\n`;
        if (scenario === '401') {
            reqText += `Authorization: (Missing or Invalid Token)\r\n`;
        } else {
            reqText += `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\r\n`;
        }
        if (bodyPayload) {
            reqText += `Content-Type: application/json; charset=utf-8\r\n`;
            reqText += `Content-Length: ${new TextEncoder().encode(bodyPayload).length}\r\n\r\n`;
            reqText += bodyPayload;
        } else {
            reqText += `\r\n(No message body for ${method} request)`;
        }

        rawRequestOutput.textContent = reqText;

        // Construct Raw Response based on Scenario
        let resCode = "200 OK";
        let resData = {};

        switch (scenario) {
            case "200":
                resCode = "200 OK";
                statusTag.textContent = "200 OK (Success)";
                statusTag.style.color = "#34d399";
                resData = {
                    status: "success",
                    timestamp: dateStr,
                    data: {
                        reportType: "Regional Sales Summary",
                        currency: "USD",
                        activeRegions: 4,
                        recordsProcessed: 142050
                    }
                };
                break;
            case "201":
                resCode = "201 Created";
                statusTag.textContent = "201 Created";
                statusTag.style.color = "#34d399";
                resData = {
                    status: "created",
                    recordId: "REC-2026-9921",
                    message: "Sales transactional record committed into staging partition successfully."
                };
                break;
            case "400":
                resCode = "400 Bad Request";
                statusTag.textContent = "400 Bad Request";
                statusTag.style.color = "#fbbf24";
                resData = {
                    status: "error",
                    error: "Bad Request",
                    message: "Invalid query parameter 'quarter'. Expected one of ['Q1', 'Q2', 'Q3', 'Q4']."
                };
                break;
            case "401":
                resCode = "401 Unauthorized";
                statusTag.textContent = "401 Unauthorized";
                statusTag.style.color = "#f87171";
                resData = {
                    status: "error",
                    error: "Unauthorized",
                    message: "Authentication credentials were not provided or JWT bearer token has expired."
                };
                break;
            case "404":
                resCode = "404 Not Found";
                statusTag.textContent = "404 Not Found";
                statusTag.style.color = "#f87171";
                resData = {
                    status: "error",
                    error: "Not Found",
                    message: `Endpoint resource '${endpoint}' does not exist on this cluster.`
                };
                break;
            case "500":
                resCode = "500 Internal Server Error";
                statusTag.textContent = "500 Internal Server Error";
                statusTag.style.color = "#f87171";
                resData = {
                    status: "error",
                    error: "Internal Server Error",
                    message: "Connection pool timeout: MySQL database replica cluster unreachable on port 3306."
                };
                break;
        }

        const resBody = JSON.stringify(resData, null, 2);
        let resText = `HTTP/1.1 ${resCode}\r\n`;
        resText += `Date: ${dateStr}\r\n`;
        resText += `Server: Apache/2.4.56 (Unix) OpenSSL/1.1.1t\r\n`;
        resText += `Content-Type: application/json; charset=utf-8\r\n`;
        resText += `Content-Length: ${new TextEncoder().encode(resBody).length}\r\n`;
        resText += `Access-Control-Allow-Origin: *\r\n`;
        resText += `X-Content-Type-Options: nosniff\r\n\r\n`;
        resText += resBody;

        rawResponseOutput.textContent = resText;
    }

    btnSendHttp.addEventListener('click', updateHttpInspector);
    httpMethod.addEventListener('change', () => {
        if (httpMethod.value === 'POST') {
            httpEndpoint.value = '/api/v1/sales/transactions';
            simulateScenario.value = '201';
        } else if (httpMethod.value === 'GET') {
            httpEndpoint.value = '/api/v1/sales/reports/regional?quarter=Q3';
            simulateScenario.value = '200';
        } else if (httpMethod.value === 'PUT') {
            httpEndpoint.value = '/api/v1/sales/transactions/TXN-984210';
            simulateScenario.value = '200';
        } else if (httpMethod.value === 'DELETE') {
            httpEndpoint.value = '/api/v1/sales/transactions/TXN-984210';
            simulateScenario.value = '200';
        }
        updateHttpInspector();
    });
    simulateScenario.addEventListener('change', updateHttpInspector);

    // Initial render of HTTP inspector
    updateHttpInspector();

    // ==================== OLAP RENDERING ====================
    // Data: Roll-up by Region
    const rollupData = [
        { region: "North Region", revenue: 1420500, units: 18450, stores: 42, pct: 39 },
        { region: "West Region",  revenue: 1050200, units: 14200, stores: 31, pct: 29 },
        { region: "South Region", revenue: 680400,  units: 9800,  stores: 22, pct: 19 },
        { region: "East Region",  revenue: 472900,  units: 6450,  stores: 16, pct: 13 }
    ];

    const rollupContainer = document.getElementById('rollupContainer');
    let rollupHtml = `
        <table class="olap-table">
            <thead>
                <tr>
                    <th>Geographic Region</th>
                    <th>Total Sales Revenue (USD)</th>
                    <th>Share of Total</th>
                    <th>Units Sold</th>
                    <th>Active Store Outlets</th>
                </tr>
            </thead>
            <tbody>
    `;

    rollupData.forEach(row => {
        rollupHtml += `
            <tr>
                <td><strong>${row.region}</strong></td>
                <td>$${row.revenue.toLocaleString()}</td>
                <td>
                    <div class="bar-cell">
                        <div class="rev-bar" style="width: ${row.pct * 2.2}px;"></div>
                        <span>${row.pct}%</span>
                    </div>
                </td>
                <td>${row.units.toLocaleString()}</td>
                <td>${row.stores}</td>
            </tr>
        `;
    });
    rollupHtml += `</tbody></table>`;
    rollupContainer.innerHTML = rollupHtml;

    // Data: Dice (Age Group vs Product Category)
    const diceData = [
        { age: "18-25 (Gen-Z)",       cat: "Electronics", rev: "$480,200", units: "4,120", dominant: "Audio & Wearables" },
        { age: "18-25 (Gen-Z)",       cat: "Apparel",     rev: "$210,400", units: "3,890", dominant: "Streetwear & Sneakers" },
        { age: "18-25 (Gen-Z)",       cat: "Home Goods",  rev: "$45,600",  units: "610",   dominant: "Desk Accessories" },
        { age: "26-40 (Millennials)", cat: "Electronics", rev: "$520,800", units: "3,250", dominant: "Smart Home & Laptops" },
        { age: "26-40 (Millennials)", cat: "Apparel",     rev: "$340,100", units: "4,200", dominant: "Athleisure & Formal" },
        { age: "26-40 (Millennials)", cat: "Home Goods",  rev: "$290,500", units: "2,780", dominant: "Kitchen & Furniture" },
        { age: "41-60 (Gen-X)",       cat: "Electronics", rev: "$240,600", units: "1,450", dominant: "Appliances & TVs" },
        { age: "41-60 (Gen-X)",       cat: "Apparel",     rev: "$265,300", units: "2,980", dominant: "Outdoor & Casual" },
        { age: "41-60 (Gen-X)",       cat: "Home Goods",  rev: "$430,900", units: "3,950", dominant: "Home Decor & Dining" }
    ];

    const diceContainer = document.getElementById('diceContainer');
    let diceHtml = `
        <table class="olap-table">
            <thead>
                <tr>
                    <th>Customer Age Group</th>
                    <th>Product Category</th>
                    <th>Segment Revenue</th>
                    <th>Units Sold</th>
                    <th>Dominant Product Segment</th>
                </tr>
            </thead>
            <tbody>
    `;

    diceData.forEach(row => {
        diceHtml += `
            <tr>
                <td><strong>${row.age}</strong></td>
                <td>${row.cat}</td>
                <td><strong>${row.rev}</strong></td>
                <td>${row.units}</td>
                <td><em>${row.dominant}</em></td>
            </tr>
        `;
    });
    diceHtml += `</tbody></table>`;
    diceContainer.innerHTML = diceHtml;
});
