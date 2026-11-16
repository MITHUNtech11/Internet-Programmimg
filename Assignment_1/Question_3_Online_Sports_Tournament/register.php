<?php
/**
 * Olympus Sports Tournament - Team Registration Processor
 * WAMP/LAMP HTTP POST Handler
 * Assignment 1 (CO1) - Question 3
 */

header('Content-Type: text/html; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo "<h1>405 Method Not Allowed</h1><p>Please submit via HTTP POST.</p>";
    exit;
}

$teamName       = htmlspecialchars(trim($_POST['teamName'] ?? 'N/A'));
$college        = htmlspecialchars(trim($_POST['college'] ?? 'N/A'));
$sportCategory  = htmlspecialchars(trim($_POST['sportCategory'] ?? 'N/A'));
$genderDivision = htmlspecialchars(trim($_POST['genderDivision'] ?? 'N/A'));
$squadCount     = intval($_POST['squadCount'] ?? 0);
$captainName    = htmlspecialchars(trim($_POST['captainName'] ?? 'N/A'));
$captainPhone   = htmlspecialchars(trim($_POST['captainPhone'] ?? 'N/A'));
$captainEmail   = filter_var(trim($_POST['captainEmail'] ?? ''), FILTER_SANITIZE_EMAIL);
$jerseyColor    = htmlspecialchars(trim($_POST['jerseyColor'] ?? '#f59e0b'));
$roster         = nl2br(htmlspecialchars(trim($_POST['roster'] ?? 'N/A')));

$entryCode      = "OLY-TEAM-" . strtoupper(substr(md5(uniqid()), 0, 8));
$timestamp      = date("Y-m-d H:i:s");
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Olympus Cup 2026 - Team Entry Confirmation</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: #0f172a;
      color: #f8fafc;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      padding: 20px;
    }
    .pass-card {
      background: #1e293b;
      border: 2px solid #f59e0b;
      border-radius: 16px;
      padding: 36px;
      max-width: 650px;
      width: 100%;
      box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    .badge-live {
      background: #f59e0b;
      color: #0f172a;
      font-weight: 800;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.8rem;
      display: inline-block;
      margin-bottom: 12px;
    }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.6rem;
      color: #ffffff;
      margin: 0 0 6px 0;
    }
    .code {
      color: #f59e0b;
      font-weight: 700;
      margin-bottom: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 24px;
    }
    th, td {
      padding: 9px 12px;
      border-bottom: 1px solid #334155;
      font-size: 0.92rem;
      text-align: left;
    }
    th { color: #94a3b8; width: 40%; }
    td { color: #f8fafc; font-weight: 600; }
    .color-swatch {
      display: inline-block;
      width: 16px;
      height: 16px;
      border-radius: 4px;
      vertical-align: middle;
      border: 1px solid #ffffff;
    }
    .btn {
      display: inline-block;
      background: #f59e0b;
      color: #0f172a;
      font-weight: 700;
      text-decoration: none;
      padding: 10px 22px;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="pass-card">
    <div class="badge-live">HTTP 200 OK — Official Team Entry Confirmed</div>
    <h1>Olympus Championship 2026 Entry Pass</h1>
    <div class="code">Team Pass Reference: <?php echo $entryCode; ?></div>

    <table>
      <tr><th>Team Name</th><td><?php echo $teamName; ?></td></tr>
      <tr><th>Representing College</th><td><?php echo $college; ?></td></tr>
      <tr><th>Sport Discipline</th><td><?php echo $sportCategory . ' (' . $genderDivision . ')'; ?></td></tr>
      <tr><th>Squad Size</th><td><?php echo $squadCount; ?> Players</td></tr>
      <tr><th>Team Captain</th><td><?php echo $captainName; ?> (<?php echo $captainPhone; ?>)</td></tr>
      <tr><th>Captain Email</th><td><?php echo $captainEmail; ?></td></tr>
      <tr>
        <th>Jersey Color</th>
        <td>
          <span class="color-swatch" style="background-color: <?php echo $jerseyColor; ?>;"></span>
          <?php echo $jerseyColor; ?>
        </td>
      </tr>
      <tr><th>Roster Summary</th><td><?php echo $roster; ?></td></tr>
      <tr><th>Registered At</th><td><?php echo $timestamp; ?></td></tr>
    </table>

    <a href="index.html" class="btn">← Back to Tournament Hub</a>
  </div>
</body>
</html>
