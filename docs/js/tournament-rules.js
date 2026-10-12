document.addEventListener("DOMContentLoaded", function() {
    // Tournament Format Content
    const formatHTML = `
        <h4>Tournament Format</h4>
        <ul>
            <li><strong>Eligibility:</strong> Open Singles for adult players (all skill levels), players must have an LTA Advantage account with active WTN rating.</li>
            <li><strong>Draw:</strong> Depending on number of entries, a group stage (round-robin) may be held followed by a knockout + consolation bracket.</li>
            <li><strong>Seeding:</strong> Seeds are determined strictly by players' official World Tennis Number (WTN) ratings & rankings at the time of the draw. Top seeds are placed on opposite brackets/groups to ensure a balanced draw. Unseeded spots are placed randomly via draw software.</li>
            <li><strong>Match Scoring:</strong> Best of 3 standard sets (A Match tie-break can be played at 1 set all if both players agreed).</li>
            <li><strong>Scheduling:</strong> Self-arranged matches, players coordinate match dates, times, and venue locations directly with each other within the designated seasonal window.</li>
        </ul>

        <h4>Venues & Hosting Rules</h4>
        <ul>
            <li><strong>Location / Venue:</strong> Matches are played across local tennis courts/clubs in the county.</li>
            <li><strong>Home & Away Setup:</strong> The top/first-named player on the draw fixture is designated as the "Home" player. The Home player is responsible for providing the court and supplying a tin of new or near-new tennis balls.</li>
            <li>If the Home player cannot provide a court in the county, they concede home advantage. The Away player then takes over as the host.</li>
        </ul>

    `;

    // Result Entry & WTN Content
    const resultHTML = `
        <h4>Prizes & Recognition</h4>
        <ol>
            <li><strong>The Champion Trophy:</strong> The ultimate winner of the main draw takes home the engraved Tennis Nerds Champion Trophy. <em>(Note: Trophy cost to be split among all nerds entering the draw)</em>.</li>
            <li><strong>WTN Points & Bragging Rights:</strong> All matches count towards your official World Tennis Number (WTN) rating. Winners of other/consolation brackets earn full 'nerds circuit' recognition and bragging rights.</li>
        </ol>
    
        <h4>Results & Disputes</h4>
        <ul>
            <li><strong>Score Submission:</strong> Winners are required to submit match results using this <a href="https://forms.gle/PyRd8Swz5D9iQWkt5" target="_blank">form</a> within 24 hours.</li>
            <li><strong>On-Court Scoring Disputes:</strong> Follow standard LTA self-officiating principles (e.g., if in doubt, the ball is called 'IN').</li>
            <li><strong>Administrative Disputes:</strong> For scheduling deadlocks or rule clarifications, the organizer's decision is final.</li>
            <li><strong>Sanctioning & Conduct:</strong> The competition is sanctioned by the LTA and is governed by <a href="https://www.lta.org.uk/siteassets/lta-officials/my-resources/rules-and-regulations/lta-competition/lta-competition-regulations-2026.pdf" target="_blank">LTA Competition Regulations</a> and the <a href="https://www.lta.org.uk/siteassets/about-lta/file/lta-code-of-conduct-jan-2025.pdf" target="_blank">LTA Code of Conduct</a> .</li>
            <li><strong>Community Values & Safety:</strong> All players must abide by the <a href="https://www.tennisnerds.org/TNCRulebook.html" target="_blank">TNC Rulebook</a> regarding fair play, venue respect, inclusive behavior, and online conduct.</li>
        </ul>    
    `;

    // Inject into placeholders if they exist on the page
    const formatElement = document.getElementById("tournament-format-box");
    const resultElement = document.getElementById("result-entry-box");

    if (formatElement) formatElement.innerHTML = formatHTML;
    if (resultElement) resultElement.innerHTML = resultHTML;
});
