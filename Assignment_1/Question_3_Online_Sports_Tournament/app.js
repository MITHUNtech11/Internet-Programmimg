/**
 * Olympus Sports Tournament - Interactive Client App
 * Provides: dynamic table filtering by sport category,
 * and client-side simulation for standalone browser testing.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Sports category table filtering
  const filterButtons = document.querySelectorAll('.filter-btn');
  const tableRows = document.querySelectorAll('#fixturesTable tbody tr');

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active class
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const selectedSport = btn.dataset.sport;

      tableRows.forEach(row => {
        const rowSport = row.dataset.sport;
        if (selectedSport === 'all' || rowSport === selectedSport) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  });

  // Client-side fallback for form submission
  const form = document.getElementById('tournamentForm');
  const feedback = document.getElementById('sportsFeedback');

  form.addEventListener('submit', (e) => {
    if (window.location.protocol === 'file:') {
      e.preventDefault();
      const team = document.getElementById('teamName').value;
      const college = document.getElementById('college').value;
      const sport = document.getElementById('sportCategory').value;
      const captain = document.getElementById('captainName').value;

      feedback.style.display = 'block';
      feedback.innerHTML = `
        <h4>✓ Team Registration Received (Client Simulation)</h4>
        <p><strong>Team:</strong> ${team} | <strong>Institution:</strong> ${college}</p>
        <p><strong>Sport Discipline:</strong> ${sport} | <strong>Captain:</strong> ${captain}</p>
        <p style="color: #059669; font-size: 0.9rem;">HTTP POST payload validated. In WAMP/LAMP environment, this routes to <code>register.php</code>.</p>
      `;
      feedback.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
