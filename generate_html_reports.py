import pyodbc
import datetime
import os
from collections import defaultdict

# --- Configuration ---
# Update these with your SQL Server details
DB_SERVER = 'tariqhassan2022\SQLEXPRESS'
DB_NAME = 'DTC Box League'
ODBC_DRIVER = 'ODBC Driver 17 for SQL Server'

# Output directory for HTML reports
output_dir = 'docs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Directory for CSS files
css_dir = os.path.join(output_dir, 'css')
if not os.path.exists(css_dir):
    os.makedirs(css_dir)

# Path to logo
IMAGE_PATH = 'assets/TNL_logo_white.png'

# JavaScript for frozen columns and hamburger menu
FROZEN_COLUMNS_JS = """
<script>
window.addEventListener('load', function() {
    function adjustFrozenColumns() {
        document.querySelectorAll('.data-table').forEach(function(table) {
            var firstCol = table.querySelector('th:nth-child(1)');
            if (firstCol) {
                var firstColWidth = firstCol.offsetWidth;
                var secondCols = table.querySelectorAll('th:nth-child(2), td:nth-child(2)');
                secondCols.forEach(function(cell) {
                    cell.style.left = firstColWidth + 'px';
                });
            }
        });
    }
    
    adjustFrozenColumns();
    window.addEventListener('resize', adjustFrozenColumns);
    
    // Hamburger menu toggle - slides in from right
    var menuToggle = document.querySelector('.menu-toggle');
    var navMenu = document.querySelector('nav');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navMenu.classList.toggle('active');
            
            var isExpanded = navMenu.classList.contains('active');
            menuToggle.setAttribute('aria-expanded', isExpanded);
        });
        
        // Close menu when clicking on overlay
        navMenu.addEventListener('click', function(e) {
            if (e.target === navMenu) {
                navMenu.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
        
        // Close menu when clicking on a navigation link
        var navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
            });
        });
    }
});
</script>
"""

def get_nav_items(current_page_name):
    """Generates the navigation items as list items."""
    nav_links = {
        "fixtures": {"text": "Current Round Fixtures", "file": "current_round_fixtures.html"},
        "standings": {"text": "Current Standings", "file": "index.html"},
        "leaderboard": {"text": "Overall Leaderboard", "file": "leaderboard.html"},
        "previous": {"text": "Previous Rounds", "file": "previous_rounds.html"},
        "info": {"text": "Info & Rules", "file": "info_rules.html"}
    }

    nav_items = []
    for key, value in nav_links.items():
        active_class = 'active' if key == current_page_name else ''
        nav_items.append(
            f'<li><a href="{value["file"]}" class="{active_class}">{value["text"]}</a></li>'
        )
    
    return "".join(nav_items)


def get_nav_html(current_page_name):
    """Generates the full HTML for hamburger button and navigation bar."""
    return f'''
    <button class="menu-toggle" aria-label="Toggle navigation menu" aria-expanded="false">
        ☰ Menu
    </button>
    <nav><ul>
        {get_nav_items(current_page_name)}
    </ul></nav>
    '''


def get_footer_html(show_last_updated=True):
    """Generates the HTML for the footer."""
    current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")
    current_year = datetime.datetime.now().year
    
    last_updated = f'<p>Data last updated: <span id="last-updated">{current_time}</span></p>' if show_last_updated else ''
    
    footer_html = f'''
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h4>About</h4>
                    <p>🎾 Community Tennis League</p>
                    <p>📍 Welwyn Garden City & surroundings!</p>
                </div>
                
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="https://docs.google.com/forms/d/e/1FAIpQLSfaBiGWHBvGYVIXNhWPffa0pb-NuMT_CkdPfyxRXj8ZDwWJQQ/viewform?usp=dialog" target="_blank">League Signup</a></li>
                        <li><a href="https://forms.gle/4SxqB9DoL93L6W4Z7" target="_blank">Submit Scores</a></li>
                        <li><a href="https://www.lta.org.uk/advantage-home/my-game/self-submission/" target="_blank">LTA Self-Submission</a></li>
                        <li><a href="social_doubles.html">Social Doubles</a></li> 
                        <li><a href="privacy_policy.html">Privacy Policy</a></li>
                        <li><a href="constitution.html">Constitution</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Social Media</h4>
                    <div class="social-links">
                        <a href="https://www.instagram.com/tennisnerdsuk/" target="_blank" aria-label="Instagram" title="Follow us on Instagram">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                            </svg>
                        </a>
                        <a href="https://chat.whatsapp.com/FASdYjTNTcO2ctSF6zKiwJ" target="_blank" aria-label="WhatsApp" title="League WhatsApp group">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                            </svg>
                        </a>
                    </div>
                </div>
                
                <div class="footer-section">
                    <h4>Partners</h4>
                    <p style="font-weight: bold; margin-bottom: 10px;">Commitment Champion Award</p>
                    <p style="font-size: 0.85em; margin-bottom: 10px;">Generously Sponsored by</p>
                    <a href="https://goode-sport.co.uk/" target="_blank">
                        <img src="assets/volkl-logo.png" alt="Völkl - Goode Sport" class="partner-logo">
                    </a>
                    <div class="partner-info">
                        <a href="https://goode-sport.co.uk/" target="_blank">Goode Sport (Völkl UK)</a>
                    </div>
                </div>
            </div>
            
            <div class="footer-bottom">
                {last_updated}
                <p>&copy; {current_year} Tennis Nerds League. All rights reserved.</p>
            </div>
        </footer>
    '''
    return footer_html
    """Generates the navigation items as list items."""
    nav_links = {
        "fixtures": {"text": "Current Round Fixtures", "file": "current_round_fixtures.html"},
        "standings": {"text": "Current Standings", "file": "index.html"},
        "leaderboard": {"text": "Overall Leaderboard", "file": "leaderboard.html"},
        "previous": {"text": "Previous Rounds", "file": "previous_rounds.html"},
        "info": {"text": "Info & Rules", "file": "info_rules.html"}
    }

    nav_items = []
    for key, value in nav_links.items():
        active_class = 'active' if key == current_page_name else ''
        nav_items.append(
            f'<li><a href="{value["file"]}" class="{active_class}">{value["text"]}</a></li>'
        )
    
    return "".join(nav_items)


def get_nav_html(current_page_name):
    """Generates the full HTML for hamburger button and navigation bar."""
    return f'''
    <button class="menu-toggle" aria-label="Toggle navigation menu" aria-expanded="false">
        ☰ Menu
    </button>
    <nav><ul>
        {get_nav_items(current_page_name)}
    </ul></nav>
    '''


def generate_current_round_fixtures_report():
    conn = None
    cursor = None
    try:
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT TOP 1 [name], [start_date], [end_date]
            FROM dbo.rounds
            WHERE GETDATE() BETWEEN start_date AND end_date
            ORDER BY start_date DESC
        """)
        round_info = cursor.fetchone()

        round_name = "Current Round"
        round_start_date = None
        round_end_date = None

        if round_info:
            round_name = round_info[0]
            start_date_obj = round_info[1]
            end_date_obj = round_info[2]

            if start_date_obj:
                round_start_date = start_date_obj.strftime("%d %b")
            if end_date_obj:
                round_end_date = end_date_obj.strftime("%d %b")

        cursor.execute("SELECT RoundName, BoxName, Player1Name, Player2Name, Score, WinnerName, PlayedOn FROM dbo.vw_CurrentRoundMatches ORDER BY BoxName ASC, CASE WHEN PlayedOn IS NULL THEN 1 ELSE 0 END ASC, PlayedOn ASC, Player1Name ASC")
        matches_data = cursor.fetchall()

        html_sections = ""
        
        current_round_display_name = "Current Round Fixtures"
        if round_name and round_start_date and round_end_date:
            current_round_display_name = f"{round_name} Fixtures <br>({round_start_date} - {round_end_date})"
        elif round_name:
            current_round_display_name = f"{round_name} Fixtures"
        
        if not matches_data:
            print("No active round fixtures found to generate report.")
            html_sections = "<p class='no-data-message'>No matches recorded for the active round yet. Please ensure there is a round with a start date before today and an end date after today, and matches are assigned to it.</p>"
        else:
            grouped_matches = defaultdict(list)
            for row in matches_data:
                box_name = row[1]
                match_details = row[2:]
                grouped_matches[box_name].append(match_details)
            
            for box_name in sorted(grouped_matches.keys()):
                html_sections += f'<h3>{box_name}</h3>\n'
                html_sections += """
                <div class="table-wrapper">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Player 1</th>
                            <th>Player 2</th>
                            <th>Score (P1-P2)</th>
                            <th>Winner</th>
                            <th>Played On</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                for match in grouped_matches[box_name]:
                    player1_name = match[0]
                    player2_name = match[1]
                    score = match[2]
                    winner = match[3]
                    played_on = match[4].strftime("%Y-%m-%d") if match[4] is not None else 'Not Played'

                    html_sections += f"""
                        <tr>
                            <td>{player1_name}</td>
                            <td>{player2_name}</td>
                            <td>{score}</td>
                            <td>{winner}</td>
                            <td>{played_on}</td>
                        </tr>
                    """
                html_sections += """
                    </tbody>
                </table>
                </div>
                """

        current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Nerds League</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/png" href="dtc-favicon.png">
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="header-logo-link">
                <img src="{IMAGE_PATH}" alt="Tennis Nerds League Logo" class="header-logo">
            </a>
            
            <h1 class="league-title">
                <span class="tennis">tennis</span><span class="nerds">nerds</span> <span class="league"> league</span>
            </h1>
            
            {get_nav_html("fixtures")}
        </header>

        <main>
            <h2>{current_round_display_name}</h2>
            {html_sections}
        </main>

        {get_footer_html(current_time)}
    </div>
    {FROZEN_COLUMNS_JS}
</body>
</html>
        """
        output_file_path = os.path.join(output_dir, 'current_round_fixtures.html')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated {output_file_path} successfully!")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error in generate_current_round_fixtures_report: {sqlstate} - {ex}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_current_round_fixtures_report: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def generate_current_round_standings_report():
    conn = None
    cursor = None
    try:
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT TOP 1 [name], [start_date], [end_date]
            FROM dbo.rounds
            WHERE GETDATE() BETWEEN start_date AND end_date
            ORDER BY start_date DESC
        """)
        round_info = cursor.fetchone()

        round_name = "Current Round"
        round_start_date = None
        round_end_date = None

        if round_info:
            round_name = round_info[0]
            start_date_obj = round_info[1]
            end_date_obj = round_info[2]

            if start_date_obj:
                round_start_date = start_date_obj.strftime("%d %b")
            if end_date_obj:
                round_end_date = end_date_obj.strftime("%d %b")

        cursor.execute("""
            SELECT
                RoundName, BoxName, PlayerName, MatchesPlayed, Wins, Losses, Draws, Points, RankInBox
            FROM dbo.vw_CurrentStandings
            ORDER BY RoundName ASC, BoxName ASC, RankInBox ASC
        """)
        standings_data = cursor.fetchall()

        html_sections = ""
        
        report_title = "Current Round Standings"
        if round_name and round_start_date and round_end_date:
            report_title = f"{round_name} Standings <br>({round_start_date} - {round_end_date})"
        elif round_name:
            report_title = f"{round_name} Standings"
        
        if not standings_data:
            print("No current round standings found to generate report.")
            html_sections = "<p class='no-data-message'>No standings available for the current round. Ensure matches have been played and a round is active.</p>"
        else:
            grouped_by_round = defaultdict(lambda: defaultdict(list))
            for row in standings_data:
                round_name_from_db = row[0]
                box_name = row[1]
                player_standings = row[2:]
                grouped_by_round[round_name_from_db][box_name].append(player_standings)

            for r_name in sorted(grouped_by_round.keys()):
                for box_name in sorted(grouped_by_round[r_name].keys()):
                    html_sections += f'<h3>{box_name}</h3>\n'

                    html_sections += """
                    <div class="table-wrapper">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Player</th>
                                <th>Played</th>
                                <th>Wins</th>
                                <th>Losses</th>
                                <th>Draws</th>
                                <th>Points</th>
                            </tr>
                        </thead>
                        <tbody>
                    """
                    for player_stats in grouped_by_round[r_name][box_name]:
                        rank = player_stats[6]
                        player_name = player_stats[0]
                        matches_played = player_stats[1]
                        wins = player_stats[2]
                        losses = player_stats[3]
                        draws = player_stats[4]
                        points = player_stats[5]

                        html_sections += f"""
                            <tr>
                                <td>{rank}</td>
                                <td>{player_name}</td>
                                <td>{matches_played}</td>
                                <td>{wins}</td>
                                <td>{losses}</td>
                                <td>{draws}</td>
                                <td>{points}</td>
                            </tr>
                        """
                    html_sections += """
                        </tbody>
                    </table>
                    </div>
                    """

        current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>tennisnerds.org</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/png" href="dtc-favicon.png">
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="header-logo-link">
                <img src="{IMAGE_PATH}" alt="Tennis Nerds League Logo" class="header-logo">
            </a>
            
            <h1 class="league-title">
                <span class="tennis">tennis</span><span class="nerds">nerds</span><span class="league">league</span>
            </h1>
            
            {get_nav_html("standings")}
        </header>

        <main>
            <h2>{report_title}</h2>
            {html_sections}
        </main>

        {get_footer_html(current_time)}
    </div>
    {FROZEN_COLUMNS_JS}
</body>
</html>
        """
        output_file_path = os.path.join(output_dir, 'index.html')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated {output_file_path} successfully!")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error in generate_current_round_standings_report: {sqlstate} - {ex}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_current_round_standings_report: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def generate_leaderboard_report():
    conn = None
    cursor = None
    try:
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                PlayerName, MatchesPlayed, MatchesWon, GamesWon, SetsWon, MatchesLost, MatchesDraw, TotalPoints, OverallRank
            FROM dbo.vw_OverallLeaderboard
            ORDER BY OverallRank ASC
        """)
        leaderboard_data = cursor.fetchall()

        html_sections = ""

        if not leaderboard_data:
            print("No leaderboard data found to generate report.")
            html_sections = "<p class='no-data-message'>No players have played enough matches to appear on the leaderboard yet.</p>"
        else:
            html_sections += """
            <h2>Overall Leaderboard</h2>
            <div class="table-wrapper">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Played</th>
                        <th>Won</th>
                        <th>Lost</th>
                        <th>Draw</th>
                        <th>Games Won</th>
                        <th>Sets Won</th>
                        <th>Points</th>
                    </tr>
                </thead>
                <tbody>
            """
            for row in leaderboard_data:
                player_name = row[0]
                matches_played = row[1]
                matches_won = row[2]
                games_won = row[3]
                sets_won = row[4]
                matches_lost = row[5]
                matches_draw = row[6]
                total_points = row[7]
                overall_rank = row[8]

                html_sections += f"""
                    <tr>
                        <td>{overall_rank}</td>
                        <td>{player_name}</td>
                        <td>{matches_played}</td>
                        <td>{matches_won}</td>
                        <td>{matches_lost}</td>
                        <td>{matches_draw}</td>
                        <td>{games_won}</td>
                        <td>{sets_won}</td>
                        <td>{total_points}</td>
                    </tr>
                """
            html_sections += """
                </tbody>
            </table>
            </div>
            """

        current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Nerds League - Overall Leaderboard</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/png" href="dtc-favicon.png">
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="header-logo-link">
                <img src="{IMAGE_PATH}" alt="Tennis Nerds League Logo" class="header-logo">
            </a>
            
            <h1 class="league-title">
                <span class="tennis">tennis</span><span class="nerds">nerds</span><span class="league">league</span>
            </h1>
            
            {get_nav_html("leaderboard")}
        </header>

        <main>
            {html_sections}
        </main>

        {get_footer_html(current_time)}
    </div>
    {FROZEN_COLUMNS_JS}
</body>
</html>
        """
        output_file_path = os.path.join(output_dir, 'leaderboard.html')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated {output_file_path} successfully!")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error in generate_leaderboard_report: {sqlstate} - {ex}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_leaderboard_report: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def generate_previous_rounds_report():
    conn = None
    cursor = None
    try:
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                RoundID, RoundName, RoundStartDate, RoundEndDate, BoxName,
                PlayerName, MatchesPlayed, Wins, Losses, Draws, Points, RankInBox
            FROM dbo.vw_PreviousRoundStandings
            ORDER BY RoundEndDate DESC, RoundID DESC, BoxName ASC, RankInBox ASC
        """)
        previous_standings_data = cursor.fetchall()

        cursor.execute("""
            SELECT
                RoundID, RoundName, RoundStartDate, RoundEndDate, BoxName,
                Player1Name, Player2Name, Score, WinnerName, PlayedOn
            FROM dbo.vw_PreviousRoundMatches
            ORDER BY RoundEndDate DESC, RoundID DESC, BoxName ASC, PlayedOn ASC, Player1Name ASC
        """)
        previous_matches_data = cursor.fetchall()

        html_sections = ""

        if not previous_standings_data and not previous_matches_data:
            print("No previous rounds data found to generate report.")
            html_sections = "<p class='no-data-message'>No previous rounds have been completed yet.</p>"
        else:
            grouped_standings = defaultdict(lambda: defaultdict(list))
            for row in previous_standings_data:
                round_id = row[0]
                round_name = row[1]
                round_start_date_str = row[2].strftime("%d %b") if row[2] else 'N/A'
                round_end_date_str = row[3].strftime("%d %b") if row[3] else 'N/A'
                box_name = row[4]
                player_stats = row[5:]
                grouped_standings[(round_id, round_name, round_start_date_str, round_end_date_str)][box_name].append(player_stats)

            grouped_matches = defaultdict(lambda: defaultdict(list))
            for row in previous_matches_data:
                round_id = row[0]
                round_name = row[1]
                round_start_date_str = row[2].strftime("%d %b") if row[2] else 'N/A'
                round_end_date_str = row[3].strftime("%d %b") if row[3] else 'N/A'
                box_name = row[4]
                match_details = row[5:]
                grouped_matches[(round_id, round_name, round_start_date_str, round_end_date_str)][box_name].append(match_details)

            all_round_keys = sorted(list(set(grouped_standings.keys()) | set(grouped_matches.keys())),
                                     key=lambda x: datetime.datetime.strptime(x[3], "%d %b") if x[3] != 'N/A' else datetime.datetime.min,
                                     reverse=True)

            for round_key in all_round_keys:
                round_id, round_name, round_start_date, round_end_date = round_key
                html_sections += f'<h2>{round_name} ({round_start_date} - {round_end_date})</h2>\n'

                boxes_in_round = set(grouped_standings[round_key].keys()) | set(grouped_matches[round_key].keys())

                for box_name in sorted(boxes_in_round):
                    html_sections += f'<h3>{box_name}</h3>\n'

                    if box_name in grouped_standings[round_key]:
                        html_sections += """
                        <h4>Standings</h4>
                        <div class="table-wrapper">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Player</th>
                                    <th>Played</th>
                                    <th>Wins</th>
                                    <th>Losses</th>
                                    <th>Draws</th>
                                    <th>Points</th>
                                </tr>
                            </thead>
                            <tbody>
                        """
                        for player_stats in grouped_standings[round_key][box_name]:
                            rank = player_stats[6]
                            player_name = player_stats[0]
                            matches_played = player_stats[1]
                            wins = player_stats[2]
                            losses = player_stats[3]
                            draws = player_stats[4]
                            points = player_stats[5]

                            html_sections += f"""
                                <tr>
                                    <td>{rank}</td>
                                    <td>{player_name}</td>
                                    <td>{matches_played}</td>
                                    <td>{wins}</td>
                                    <td>{losses}</td>
                                    <td>{draws}</td>
                                    <td>{points}</td>
                                </tr>
                            """
                        html_sections += """
                            </tbody>
                        </table>
                        </div>
                        """
                    else:
                        html_sections += "<p>No standings available for this box in this round.</p>"

                    if box_name in grouped_matches[round_key]:
                        html_sections += """
                        <h4>Matches</h4>
                        <div class="table-wrapper">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Player 1</th>
                                    <th>Player 2</th>
                                    <th>Score (P1-P2)</th>
                                    <th>Winner</th>
                                    <th>Played On</th>
                                </tr>
                            </thead>
                            <tbody>
                        """
                        for match in grouped_matches[round_key][box_name]:
                            player1_name = match[0]
                            player2_name = match[1]
                            score = match[2]
                            winner = match[3]
                            played_on = match[4].strftime("%Y-%m-%d") if match[4] is not None else 'Not Played'

                            html_sections += f"""
                                <tr>
                                    <td>{player1_name}</td>
                                    <td>{player2_name}</td>
                                    <td>{score}</td>
                                    <td>{winner}</td>
                                    <td>{played_on}</td>
                                </tr>
                            """
                        html_sections += """
                            </tbody>
                        </table>
                        </div>
                        """
                    else:
                        html_sections += "<p>No matches available for this box in this round.</p>"

        current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Nerds League - Previous Rounds</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="css/style.css">
    <link rel="icon" type="image/png" href="dtc-favicon.png">
</head>
<body>
    <div class="container">
        <header>
            <a href="/" class="header-logo-link">
                <img src="{IMAGE_PATH}" alt="Tennis Nerds League Logo" class="header-logo">
            </a>
            
            <h1 class="league-title">
                <span class="tennis">tennis</span><span class="nerds">nerds</span><span class="league">league</span>
            </h1>
            
            {get_nav_html("previous")}
        </header>

        <main>
            <h1>Previous Rounds Overview</h1>
            {html_sections}
        </main>

        {get_footer_html(current_time)}
    </div>
    {FROZEN_COLUMNS_JS}
</body>
</html>
        """
        output_file_path = os.path.join(output_dir, 'previous_rounds.html')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated {output_file_path} successfully!")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error in generate_previous_rounds_report: {sqlstate} - {ex}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_previous_rounds_report: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    image_dir = os.path.join(output_dir, 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    print("Starting HTML report generation...")
    generate_current_round_fixtures_report()
    generate_current_round_standings_report()
    generate_leaderboard_report()
    generate_previous_rounds_report()
    print("All HTML reports generated!")