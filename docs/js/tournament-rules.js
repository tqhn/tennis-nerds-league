document.addEventListener("DOMContentLoaded", function() {
    // Combined Tournament Information Content
    const formatHTML = `
        <ol>
            <li>
                <h4>Tournament Format</h4>
                <ol type="a">
                    <li><strong>Eligibility:</strong> Open Singles for adult players (all skill levels), players must have an LTA Advantage account with active WTN rating.</li>
                    <li><strong>Draw Setup:</strong> Depending on number of entries, a group stage (round-robin) may be held followed by a knockout + consolation bracket.</li>
                    <li><strong>Seeding:</strong> Seeds are determined strictly by players' official World Tennis Number (WTN) ratings & rankings at the time of the draw. Top seeds are placed on opposite brackets/groups to ensure a balanced draw. Unseeded spots are placed randomly via draw software.</li>
                    <li><strong>Match Scoring:</strong> Best of 3 standard sets. A 10-point Match Tie-Break can replace the 3rd set if both players agree before or during the match.</li>
                    <li><strong>Scheduling:</strong> Self-arranged matches, players coordinate match dates, times, and venue locations directly with each other within the designated seasonal window.</li>
                </ol>
            </li>

            <li>
                <h4>Venues & Hosting Rules</h4>
                <ol type="a">
                    <li><strong>Location / Venue:</strong> Matches are played across the regional courts/clubs within your dedicated Tennis Nerds circuit. Click to view circuit maps: <a href="https://raw.githubusercontent.com/tqhn/tennis-nerds-league/main/docs/images/Tennis%20Nerds%20Herts%20Circuit%20Map.jpeg" target="_blank">Hertfordshire</a> or <a href="https://raw.githubusercontent.com/tqhn/tennis-nerds-league/main/docs/images/Tennis%20Nerds%20North%20London%20Circuit%20Map.jpeg" target="_blank">North London</a>.</li>
                    <li><strong>Home & Away Setup:</strong> The top/first-named player on the draw fixture is designated as the "Home" player. The Home player is responsible for providing the court and supplying a tin of new or near-new tennis balls.</li>
                    <li>If the Home player cannot provide a court in the local circuit, they concede home advantage. The Away player then takes over as the host, unless agreed otherwise.</li>
                </ol>
            </li>

            <li>
                <h4>Prizes & Recognition</h4>
                <ol type="a">
                    <li><strong>The Champion Trophy:</strong> The ultimate winner of the main draw takes home the engraved Tennis Nerds Champion Trophy. <em>(Note: Trophy cost to be split among all nerds entering the tournament)</em>.</li>
                    <li><strong>WTN Points & Bragging Rights:</strong> All match wins count towards your official World Tennis Number (WTN) rating. Winners of other/consolation brackets earn full nerds circuit recognition and bragging rights.</li>
                </ol>
            </li>

            <li>
                <h4>Results & Disputes</h4>
                <ol type="a">
                    <li><strong>Score Submission:</strong> The winner is responsible for submitting match scores within 24 hours via the google form: <a href="https://forms.gle/PyRd8Swz5D9iQWkt5" target="_blank">https://forms.gle/PyRd8Swz5D9iQWkt5</a></li>
                    <li><strong>On-Court Scoring Disputes:</strong> Follow standard LTA self-officiating principles (e.g., if in doubt, the ball is called 'IN').</li>
                    <li><strong>Administrative Disputes:</strong> For scheduling deadlocks or rule clarifications, the organizer's decision is final.</li>
                    <li><strong>Sanctioning & Conduct:</strong> The competition is sanctioned by the LTA and is governed by <a href="https://www.lta.org.uk/siteassets/lta-officials/my-resources/rules-and-regulations/lta-competition/lta-competition-regulations-2026.pdf" target="_blank">LTA Competition Regulations</a> and the <a href="https://www.lta.org.uk/siteassets/about-lta/file/lta-code-of-conduct-jan-2025.pdf" target="_blank">LTA Code of Conduct</a>.</li>
                    <li><strong>Community Values & Safety:</strong> All players must abide by the <a href="https://www.tennisnerds.org/TNCRulebook.html" target="_blank">TNC Rulebook</a> regarding fair play, venue respect, inclusive behavior, and online conduct.</li>
                </ol>
            </li>
        </ol>
    `;

    // Inject into the single placeholder if it exists on the page
    const formatElement = document.getElementById("tournament-format-box");

    if (formatElement) formatElement.innerHTML = formatHTML;
});
