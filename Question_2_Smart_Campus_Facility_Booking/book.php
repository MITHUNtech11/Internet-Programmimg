<?php
/**
 * Smart Campus Facility Booking - WAMP/LAMP Request Handler
 * Assignment 1 (CO1) - Question 2
 */

header('Content-Type: text/html; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo "<h1>405 Method Not Allowed</h1><p>Please submit via HTTP POST.</p>";
    exit;
}

$facultyName  = htmlspecialchars(trim($_POST['facultyName'] ?? 'N/A'));
$empId        = htmlspecialchars(trim($_POST['empId'] ?? 'N/A'));
$facultyEmail = filter_var(trim($_POST['facultyEmail'] ?? ''), FILTER_SANITIZE_EMAIL);
$department   = htmlspecialchars(trim($_POST['department'] ?? 'N/A'));
$facility     = htmlspecialchars(trim($_POST['facilityChoice'] ?? 'N/A'));
$bookingDate  = htmlspecialchars(trim($_POST['bookingDate'] ?? 'N/A'));
$timeSlot     = htmlspecialchars(trim($_POST['timeSlot'] ?? 'N/A'));
$eventTitle   = htmlspecialchars(trim($_POST['eventTitle'] ?? 'N/A'));
$attendees    = intval($_POST['attendees'] ?? 0);
$equipment    = isset($_POST['equipment']) && is_array($_POST['equipment']) ? $_POST['equipment'] : [];
$specialReq   = htmlspecialchars(trim($_POST['specialReq'] ?? 'None'));

$bookingRef   = "SC-BKG-" . strtoupper(substr(md5(uniqid()), 0, 8));
$timestamp    = date("Y-m-d H:i:s");
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Smart Campus Facility Requisition Receipt</title>
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
    .receipt-box {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 36px;
      max-width: 640px;
      width: 100%;
      box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    }
    .badge {
      display: inline-block;
      background: #eff6ff;
      color: #1d4ed8;
      font-size: 0.85rem;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 9999px;
      margin-bottom: 14px;
    }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.6rem;
      margin-bottom: 6px;
    }
    .ref-code {
      color: #2563eb;
      font-weight: 700;
      font-size: 1.05rem;
      margin-bottom: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
    }
    th, td {
      padding: 9px 12px;
      border-bottom: 1px solid #f1f5f9;
      font-size: 0.92rem;
      text-align: left;
    }
    th { color: #64748b; width: 40%; }
    td { color: #0f172a; font-weight: 600; }
    .btn {
      display: inline-block;
      background: #2563eb;
      color: #ffffff;
      text-decoration: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.92rem;
    }
  </style>
</head>
<body>
  <div class="receipt-box">
    <div class="badge">HTTP 200 OK — Facility Requisition Confirmed</div>
    <h1>Smart Campus Venue Reservation</h1>
    <div class="ref-code">Booking Reference: <?php echo $bookingRef; ?></div>

    <table>
      <tr><th>Faculty Name</th><td><?php echo $facultyName; ?> (<?php echo $empId; ?>)</td></tr>
      <tr><th>Official Email</th><td><?php echo $facultyEmail; ?></td></tr>
      <tr><th>Department</th><td><?php echo $department; ?></td></tr>
      <tr><th>Reserved Facility</th><td><?php echo $facility; ?></td></tr>
      <tr><th>Reservation Date & Slot</th><td><?php echo $bookingDate; ?> &bull; <?php echo $timeSlot; ?></td></tr>
      <tr><th>Event Title / Purpose</th><td><?php echo $eventTitle; ?></td></tr>
      <tr><th>Expected Attendees</th><td><?php echo $attendees; ?> Persons</td></tr>
      <tr>
        <th>Required Equipment</th>
        <td>
          <?php
          if (!empty($equipment)) {
            echo implode(", ", array_map('htmlspecialchars', $equipment));
          } else {
            echo "Standard Venue Setup Only";
          }
          ?>
        </td>
      </tr>
      <tr><th>Special Notes</th><td><?php echo $specialReq; ?></td></tr>
      <tr><th>Recorded At</th><td><?php echo $timestamp; ?></td></tr>
    </table>

    <a href="index.html" class="btn">← Back to Facility Portal</a>
  </div>
</body>
</html>
