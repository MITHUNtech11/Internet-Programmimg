<?php
/**
 * WanderLust Global Journeys - Travel Booking Processor
 * WAMP/LAMP HTTP POST Handler
 * Assignment 1 (CO1) - Question 5
 */

header('Content-Type: text/html; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo "<h1>405 Method Not Allowed</h1><p>Please submit booking requests via HTTP POST.</p>";
    exit;
}

$travelerName    = htmlspecialchars(trim($_POST['travelerName'] ?? 'N/A'));
$travelerEmail   = filter_var(trim($_POST['travelerEmail'] ?? ''), FILTER_SANITIZE_EMAIL);
$phone           = htmlspecialchars(trim($_POST['phone'] ?? 'N/A'));
$destination     = htmlspecialchars(trim($_POST['destination'] ?? 'N/A'));
$packageTier     = htmlspecialchars(trim($_POST['packageTier'] ?? 'Explorer Premium Tier'));
$depDate         = htmlspecialchars(trim($_POST['depDate'] ?? 'N/A'));
$returnDate      = htmlspecialchars(trim($_POST['returnDate'] ?? 'N/A'));
$adults          = intval($_POST['adults'] ?? 1);
$children        = intval($_POST['children'] ?? 0);
$preferences     = isset($_POST['preferences']) && is_array($_POST['preferences']) ? $_POST['preferences'] : [];
$specialRequests = htmlspecialchars(trim($_POST['specialRequests'] ?? 'None'));

$bookingCode     = "WL-EXP-" . strtoupper(substr(md5(uniqid()), 0, 8));
$timestamp       = date("Y-m-d H:i:s");
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Travel Itinerary Reservation Confirmation | WanderLust</title>
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
    .booking-voucher {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 36px;
      max-width: 650px;
      width: 100%;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    }
    .badge-confirm {
      display: inline-block;
      background: #e0f2fe;
      color: #0369a1;
      font-size: 0.85rem;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 9999px;
      margin-bottom: 12px;
    }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.6rem;
      margin: 0 0 6px 0;
    }
    .code {
      color: #0284c7;
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
      background: #0284c7;
      color: #ffffff;
      font-weight: 700;
      text-decoration: none;
      padding: 10px 22px;
      border-radius: 8px;
    }
    .btn:hover { background: #0369a1; }
  </style>
</head>
<body>
  <div class="booking-voucher">
    <div class="badge-confirm">HTTP 200 OK — Itinerary Reservation Confirmed</div>
    <h1>WanderLust Expeditions Tour Voucher</h1>
    <div class="code">Voucher Reference: <?php echo $bookingCode; ?></div>

    <table>
      <tr><th>Lead Traveler</th><td><?php echo $travelerName; ?></td></tr>
      <tr><th>Contact Email</th><td><?php echo $travelerEmail; ?></td></tr>
      <tr><th>Phone / WhatsApp</th><td><?php echo $phone; ?></td></tr>
      <tr><th>Target Destination</th><td><?php echo $destination; ?></td></tr>
      <tr><th>Chosen Package</th><td><?php echo $packageTier; ?></td></tr>
      <tr><th>Travel Window</th><td><?php echo $depDate; ?> to <?php echo $returnDate; ?></td></tr>
      <tr><th>Travel Party</th><td><?php echo $adults; ?> Adult(s), <?php echo $children; ?> Child(ren)</td></tr>
      <tr>
        <th>Selected Inclusions</th>
        <td>
          <?php
          if (!empty($preferences)) {
            echo implode(", ", array_map('htmlspecialchars', $preferences));
          } else {
            echo "Standard Inclusions Only";
          }
          ?>
        </td>
      </tr>
      <tr><th>Special Requests</th><td><?php echo $specialRequests; ?></td></tr>
      <tr><th>Issued Timestamp</th><td><?php echo $timestamp; ?></td></tr>
    </table>

    <a href="index.html" class="btn">← Back to WanderLust Destinations</a>
  </div>
</body>
</html>
