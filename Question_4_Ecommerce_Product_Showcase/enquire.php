<?php
/**
 * NexTech Electronics - Customer Purchase Enquiry Handler
 * WAMP/LAMP HTTP POST Processor
 * Assignment 1 (CO1) - Question 4
 */

header('Content-Type: text/html; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo "<h1>405 Method Not Allowed</h1><p>Please submit via HTTP POST.</p>";
    exit;
}

$clientName      = htmlspecialchars(trim($_POST['clientName'] ?? 'N/A'));
$clientEmail     = filter_var(trim($_POST['clientEmail'] ?? ''), FILTER_SANITIZE_EMAIL);
$clientPhone     = htmlspecialchars(trim($_POST['clientPhone'] ?? 'N/A'));
$productSelect   = htmlspecialchars(trim($_POST['productSelect'] ?? 'N/A'));
$orderQuantity   = intval($_POST['orderQuantity'] ?? 1);
$buyerType       = htmlspecialchars(trim($_POST['buyerType'] ?? 'Individual Consumer'));
$contactChannel  = htmlspecialchars(trim($_POST['contactChannel'] ?? 'Official Email'));
$enquiryMessage  = htmlspecialchars(trim($_POST['enquiryMessage'] ?? 'Standard enquiry without extra notes'));

$enquiryRef      = "NEXTECH-ENQ-" . strtoupper(substr(md5(uniqid()), 0, 8));
$timestamp       = date("Y-m-d H:i:s");
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Customer Purchase Enquiry Voucher | NexTech</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: #f8fafc;
      color: #0f172a;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      padding: 20px;
    }
    .voucher-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 36px;
      max-width: 640px;
      width: 100%;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    }
    .badge {
      display: inline-block;
      background: #e0e7ff;
      color: #4338ca;
      font-size: 0.85rem;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 9999px;
      margin-bottom: 12px;
    }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.6rem;
      color: #0f172a;
      margin: 0 0 6px 0;
    }
    .ref-code {
      color: #6366f1;
      font-weight: 700;
      margin-bottom: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
    }
    th, td {
      padding: 10px 12px;
      border-bottom: 1px solid #f1f5f9;
      font-size: 0.92rem;
      text-align: left;
    }
    th { color: #64748b; width: 40%; }
    td { color: #0f172a; font-weight: 600; }
    .btn {
      display: inline-block;
      background: #6366f1;
      color: #ffffff;
      font-weight: 700;
      text-decoration: none;
      padding: 10px 22px;
      border-radius: 8px;
    }
    .btn:hover { background: #4f46e5; }
  </style>
</head>
<body>
  <div class="voucher-card">
    <div class="badge">HTTP 200 OK — Purchase Requisition Received</div>
    <h1>NexTech Electronics Quotation Requisition</h1>
    <div class="ref-code">Enquiry Tracking ID: <?php echo $enquiryRef; ?></div>

    <table>
      <tr><th>Customer / Entity</th><td><?php echo $clientName; ?></td></tr>
      <tr><th>Email Address</th><td><?php echo $clientEmail; ?></td></tr>
      <tr><th>Contact Phone</th><td><?php echo $clientPhone; ?></td></tr>
      <tr><th>Target Hardware</th><td><?php echo $productSelect; ?></td></tr>
      <tr><th>Requested Quantity</th><td><?php echo $orderQuantity; ?> Unit(s)</td></tr>
      <tr><th>Procurement Category</th><td><?php echo $buyerType; ?></td></tr>
      <tr><th>Preferred Follow-Up</th><td><?php echo $contactChannel; ?></td></tr>
      <tr><th>Custom Notes</th><td><?php echo $enquiryMessage; ?></td></tr>
      <tr><th>Recorded Timestamp</th><td><?php echo $timestamp; ?></td></tr>
    </table>

    <a href="index.html" class="btn">← Back to Showcase Store</a>
  </div>
</body>
</html>
