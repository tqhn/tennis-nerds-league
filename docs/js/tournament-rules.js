document.addEventListener("DOMContentLoaded", function() {
    // Tournament Format Content
    const formatHTML = `
        <h4>Tournament Format</h4>
        <ul>
            <li><strong>Eligibility:</strong> Open singles tournament for adult players.</li>
            <li><strong>Draw:</strong> Depending on the number of entries, a group stage (round-robin format) may be held followed by a knockout + consolation bracket.</li>
            <li><strong>Match Scoring:</strong> Best of 3 standard sets (A Match tie-break can be played at 1 set all if both players agreed).</li>
            <li><strong>Scheduling:</strong> Self-arranged matches coordinated directly between competitors.</li>
            <li><strong>Safeguarding:</strong> Further on-court conduct & safeguarding, see the <a href="TNCRulebook.html" target="_blank">TNC Rulebook</a></li>           
        </ul>
    `;

    // Result Entry & WTN Content
    const resultHTML = `
        <h4>Results & WTN</h4>
        <ul>
            <li><strong>LTA Verified:</strong> Official LTA grade match contributes towards your WTN rating.</li>
            <li><strong>Score Reporting:</strong> Winners are required to submit match results using this <a href="https://forms.gle/PyRd8Swz5D9iQWkt5" target="_blank">form</a> within 24 hours.</li>
            <li><strong>Dispute Resolution:</strong> In the event of a scoring dispute during a match, players should follow LTA self-officiating principles (e.g., if in doubt, the ball is 'in'). For administrative disputes, the decision of the Tennis Nerds committee is final.</li>
        </ul>
    `;

    // Inject into placeholders if they exist on the page
    const formatElement = document.getElementById("tournament-format-box");
    const resultElement = document.getElementById("result-entry-box");

    if (formatElement) formatElement.innerHTML = formatHTML;
    if (resultElement) resultElement.innerHTML = resultHTML;
});
