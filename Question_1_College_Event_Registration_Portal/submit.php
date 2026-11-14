<?php
/**
 * TechNova 2026 - Registration Processor
 * WAMP / LAMP Backend POST Request Handler
 * Assignment 1 (CO1) - Question 1
 */

header('Content-Type: text/html; charset=UTF-8');

// Ensure request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo "<h1>405 Method Not Allowed</h1><p>Please submit the form via HTTP POST.</p>";
    exit;
}

// Sanitize inputs
$fullName    = htmlspecialchars(trim($_POST['fullName'] ?? 'N/A'));
$regNumber   = htmlspecialchars(trim($_POST['regNumber'] ?? 'N/A'));
$email       = filter_var(trim($_POST['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$phone       = htmlspecialchars(trim($_POST['phone'] ?? 'N/A'));
$college     = htmlspecialchars(trim($_POST['college'] ?? 'N/A'));
$department  = htmlspecialchars(trim($_POST['department'] ?? 'N/A'));
$year        = htmlspecialchars(trim($_POST['year'] ?? 'N/A'));
$eventDate   = htmlspecialchars(trim($_POST['eventDate'] ?? 'N/A'));
$teamSize    = intval($_POST['teamSize'] ?? 1);
$events      = isset($_POST['events']) && is_array($_POST['events']) ? $_POST['events'] : [];
$specialNotes= htmlspecialchars(trim($_POST['specialNotes'] ?? 'None'));

// Handle optional file upload
$fileName = "No file uploaded";
if (isset($_FILES['idUpload']) && $_FILES['idUpload']['error'] === UPLOAD_ERR_OK) {
    $fileName = htmlspecialchars(basename($_FILES['idUpload']['name']));
}

$registrationId = "TN26-" . strtoupper(substr(md5(uniqid()), 0, 8));
$timestamp = date("Y-m-d H:i:s");
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Registration Confirmation | TechNova 2026</title>
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
    .receipt-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 40px;
      max-width: 650px;
      width: 100%;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
    }
    .badge-success {
      display: inline-block;
      background: #dcfce7;
      color: #166534;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.85rem;
      margin-bottom: 16px;
    }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.8rem;
      color: #0f172a;
      margin: 0 0 8px 0;
    }
    .reg-id {
      color: #4f46e5;
      font-weight: 700;
      font-size: 1.1rem;
      margin-bottom: 24px;
    }
    .receipt-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
    }
    .receipt-table th, .receipt-table td {
      padding: 10px 14px;
      border-bottom: 1px solid #f1f5f9;
      font-size: 0.95rem;
      text-align: left;
    }
    .receipt-table th {
      color: #64748b;
      width: 40%;
    }
    .receipt-table td {
      color: #0f172a;
      font-weight: 600;
    }
    .btn-back {
      display: inline-block;
      background: #4f46e5;
      color: #ffffff;
      text-decoration: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.95rem;
    }
    .btn-back:hover {
      background: #4338ca;
    }
  </style>
</head>
<body>
  <div class="receipt-card">
    <div class="badge-success">✓ HTTP 200 OK — Registration Successful</div>
    <h1>TechNova 2026 Registration Receipt</h1>
    <div class="reg-id">Registration Reference: <?php echo $registrationId; ?></div>

    <table class="receipt-table">
      <tr><th>Full Name</th><td><?php echo $fullName; ?></td></tr>
      <tr><th>Register Number</th><td><?php echo $regNumber; ?></td></tr>
      <tr><th>Institutional Email</th><td><?php echo $email; ?></td></tr>
      <tr><th>Contact Phone</th><td><?php echo $phone; ?></td></tr>
      <tr><th>College / University</th><td><?php echo $college; ?></td></tr>
      <tr><th>Department & Year</th><td><?php echo $department . ' (' . $year . ')'; ?></td></tr>
      <tr><th>Attendance Date</th><td><?php echo $eventDate; ?></td></tr>
      <tr><th>Team Size</th><td><?php echo $teamSize; ?> Member(s)</td></tr>
      <tr>
        <th>Enrolled Events</th>
        <td>
          <?php 
          if (!empty($events)) {
            echo "<ul>";
            foreach ($events as $ev) {
              echo "<li>" . htmlspecialchars($ev) . "</li>";
            }
            echo "</ul>";
          } else {
            echo "None selected";
          }
          ?>
        </td>
      </tr>
      <tr><th>Attached File</th><td><?php echo $fileName; ?></td></tr>
      <tr><th>Submission Timestamp</th><td><?php echo $timestamp; ?></td></tr>
    </table>

    <a href="index.html" class="btn-back">← Back to Portal Home</a>
  </div>
</body>
</html>
