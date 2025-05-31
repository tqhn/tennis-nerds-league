import pyodbc
import datetime
import os
from collections import defaultdict

# --- Configuration ---
DB_SERVER = 'tariqhassan2022\SQLEXPRESS' # Or your SQL Server instance name/IP
DB_NAME = 'DTC Box League'
ODBC_DRIVER = 'ODBC Driver 17 for SQL Server' # Or the exact ODBC driver name you have installed

# Output directory for HTML reports
# This will create an 'reports' folder in the same directory as your script
output_dir = 'reports'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- Common HTML Structure & Styling ---
# This CSS will be embedded in each HTML file
COMMON_CSS = """
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f7f6;
    color: #333;
    line-height: 1.6;
}
.container {
    max-width: 1200px;
    margin: 20px auto;
    background-color: #fff;
    padding: 30px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border-radius: 8px;
}
header {
    background-color: #004d40; /* Dark Teal */
    color: #ffffff;
    padding: 25px 0;
    text-align: center;
    border-radius: 8px 8px 0 0;
    margin-bottom: 30px;
}
header h1 {
    margin: 0;
    font-size: 2.8em;
    letter-spacing: 1.5px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}
nav ul {
    list-style: none;
    padding: 0;
    margin: 20px 0 0;
    display: flex;
    justify-content: center;
    background-color: #00695c; /* Slightly lighter teal */
    border-radius: 0 0 8px 8px;
}
nav li {
    margin: 0 15px;
}
nav a {
    color: #ffffff;
    text-decoration: none;
    padding: 12px 20px;
    display: block;
    font-weight: bold;
    transition: background-color 0.3s ease, color 0.3s ease;
}
nav a:hover, nav a.active {
    background-color: #00897b; /* Even lighter teal */
    border-radius: 5px;
    color: #e0f2f1;
}
main {
    padding: 20px 0;
}
h2 {
    color: #004d40;
    font-size: 2.2em;
    border-bottom: 2px solid #e0f2f1;
    padding-bottom: 10px;
    margin-top: 30px;
    text-align: center;
}
h3 {
    color: #00695c;
    font-size: 1.6em;
    margin-top: 25px;
    margin-bottom: 15px;
}
.data-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.data-table th, .data-table td {
    border: 1px solid #ddd;
    padding: 12px 15px;
    text-align: left;
}
.data-table th {
    background-color: #e0f2f1; /* Lightest teal */
    color: #004d40;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 0.9em;
}
.data-table tbody tr:nth-child(even) {
    background-color: #f9fdfc;
}
.data-table tbody tr:hover {
    background-color: #e6f7f6;
    cursor: pointer;
}
footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    border-top: 1px solid #e0f2f1;
    color: #666;
    font-size: 0.9em;
}
footer p {
    margin: 5px 0;
}
.no-data-message {
    text-align: center;
    font-size: 1.2em;
    color: #777;
    padding: 50px 0;
}
"""

# --- Report Generation Functions ---

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

        # Query the vw_CurrentRoundMatches view
        cursor.execute("SELECT RoundName, BoxName, Player1Name, Player2Name, Score, WinnerName, PlayedOn FROM dbo.vw_CurrentRoundMatches ORDER BY BoxName ASC, PlayedOn ASC, Player1Name ASC")
        matches_data = cursor.fetchall()

        html_sections = ""
        current_round_display_name = "Current Round Fixtures" # Default if no data

        if not matches_data:
            print("No active round fixtures found to generate report.")
            html_sections = "<p class='no-data-message'>No matches recorded for the active round yet. Please ensure there is a round with a start date before today and an end date after today, and matches are assigned to it.</p>"
        else:
            grouped_matches = defaultdict(list)
            first_row_round_name = None

            for row in matches_data:
                round_name_from_db = row[0]
                box_name = row[1]
                match_details = row[2:] # Player1Name, Player2Name, Score, WinnerName, PlayedOn

                if first_row_round_name is None:
                    first_row_round_name = round_name_from_db # Capture the round name from the first row

                grouped_matches[box_name].append(match_details)

            current_round_display_name = f"{first_row_round_name} Fixtures" if first_row_round_name else "Current Round Fixtures"

            for box_name in sorted(grouped_matches.keys()):
                html_sections += f'<h3>Box {box_name}</h3>\n'

                html_sections += """
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
                """

        current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTC Box League - Current Round Fixtures</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>DTC Box League</h1>
            <nav>
                <ul>
                    <li><a href="current_round_fixtures.html" class="active">Current Round Fixtures</a></li>
                    <li><a href="current_round_standings.html">Current Standings</a></li>
                    <li><a href="leaderboard.html">Overall Leaderboard</a></li>
                    <li><a href="previous_rounds.html">Previous Rounds</a></li>
                    <li><a href="info_rules.html">Info & Rules</a></li> </ul>
            </nav>
        </header>

        <main>
            <h2>{current_round_display_name}</h2>
            {html_sections}
        </main>

        <footer>
            <p>Data last updated: <span id="last-updated">{current_time}</span></p>
            <p>&copy; {datetime.datetime.now().year} Digswell Tennis Club Box League</p>
        </footer>
    </div>
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
        print(f"Please check your DB_SERVER, DB_NAME, ODBC_DRIVER settings, and that SQL Server is running.")
        print(f"Also ensure your view 'dbo.vw_CurrentRoundMatches' exists and returns data.")
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

        # Query the vw_CurrentStandings view
        cursor.execute("""
            SELECT
                RoundName, BoxName, PlayerName, MatchesPlayed, Wins, Losses, Draws, Points, RankInBox
            FROM dbo.vw_CurrentStandings
            ORDER BY RoundName ASC, BoxName ASC, RankInBox ASC
        """)
        standings_data = cursor.fetchall()

        html_sections = ""
        report_title = "Current Round Standings"

        if not standings_data:
            print("No current round standings found to generate report.")
            html_sections = "<p class='no-data-message'>No standings available for the current round. Ensure matches have been played and a round is active.</p>"
        else:
            grouped_by_round = defaultdict(lambda: defaultdict(list))
            # Group data: Round -> Box -> Player Standings
            for row in standings_data:
                round_name = row[0]
                box_name = row[1]
                player_standings = row[2:] # PlayerName, MatchesPlayed, Wins, Losses, Draws, Points, RankInBox

                grouped_by_round[round_name][box_name].append(player_standings)

            # Assuming there's only one "current" round, but iterate just in case
            for round_name in sorted(grouped_by_round.keys()):
                report_title = f"{round_name} Standings"
                # If you want to show the round name clearly at the top without another H2
                # html_sections += f'<h2>{round_name} Standings</h2>\n'

                for box_name in sorted(grouped_by_round[round_name].keys()):
                    html_sections += f'<h3>Box {box_name}</h3>\n'

                    html_sections += """
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
                    for player_stats in grouped_by_round[round_name][box_name]:
                        rank = player_stats[6] # RankInBox is 7th item (index 6)
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
                    """

        current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTC Box League - Current Round Standings</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>DTC Box League</h1>
            <nav>
                <ul>
                    <li><a href="current_round_fixtures.html">Current Round Fixtures</a></li>
                    <li><a href="current_round_standings.html" class="active">Current Standings</a></li> <li><a href="leaderboard.html">Overall Leaderboard</a></li>
                    <li><a href="previous_rounds.html">Previous Rounds</a></li>
                    <li><a href="info_rules.html">Info & Rules</a></li> </ul>
            </nav>
        </header>

        <main>
            <h2>{report_title}</h2>
            {html_sections}
        </main>

        <footer>
            <p>Data last updated: <span id="last-updated">{current_time}</span></p>
            <p>&copy; {datetime.datetime.now().year} Digswell Tennis Club Box League</p>
        </footer>
    </div>
</body>
</html>
        """
        output_file_path = os.path.join(output_dir, 'current_round_standings.html')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated {output_file_path} successfully!")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database error in generate_current_round_standings_report: {sqlstate} - {ex}")
        print(f"Please check your DB_SERVER, DB_NAME, ODBC_DRIVER settings, and that SQL Server is running.")
        print(f"Also ensure your view 'dbo.vw_CurrentStandings' exists and returns data.")
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

        # Query the vw_OverallLeaderboard view
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
            """

        current_time = datetime.datetime.now().strftime("%d %b %Y, %H:%M:%S")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTC Box League - Overall Leaderboard</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>DTC Box League</h1>
            <nav>
                <ul>
                    <li><a href="current_round_fixtures.html">Current Round Fixtures</a></li>
                    <li><a href="current_round_standings.html">Current Standings</a></li>
                    <li><a href="leaderboard.html" class="active">Overall Leaderboard</a></li>
                    <li><a href="previous_rounds.html">Previous Rounds</a></li>
                    <li><a href="info_rules.html">Info & Rules</a></li> </ul>
            </nav>
        </header>

        <main>
            <h2>Overall Leaderboard</h2>
            {html_sections}
        </main>

        <footer>
            <p>Data last updated: <span id="last-updated">{current_time}</span></p>
            <p>&copy; {datetime.datetime.now().year} Digswell Tennis Club Box League</p>
        </footer>
    </div>
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
        print(f"Please check your DB_SERVER, DB_NAME, ODBC_DRIVER settings, and that SQL Server is running.")
        print(f"Also ensure your view 'dbo.vw_OverallLeaderboard' exists and returns data.")
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

        # --- Fetch Previous Round Standings ---
        cursor.execute("""
            SELECT
                RoundID, RoundName, RoundStartDate, RoundEndDate, BoxName,
                PlayerName, MatchesPlayed, Wins, Losses, Draws, Points, RankInBox
            FROM dbo.vw_PreviousRoundStandings
            ORDER BY RoundEndDate DESC, RoundID DESC, BoxName ASC, RankInBox ASC
        """)
        previous_standings_data = cursor.fetchall()

        # --- Fetch Previous Round Matches ---
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
            # Group standings by RoundID, then BoxName
            grouped_standings = defaultdict(lambda: defaultdict(list))
            for row in previous_standings_data:
                round_id = row[0]
                round_name = row[1]
                round_start_date = row[2].strftime("%Y-%m-%d") if row[2] else 'N/A'
                round_end_date = row[3].strftime("%Y-%m-%d") if row[3] else 'N/A'
                box_name = row[4]
                player_stats = row[5:] # PlayerName, MatchesPlayed, Wins, Losses, Draws, Points, RankInBox
                grouped_standings[(round_id, round_name, round_start_date, round_end_date)][box_name].append(player_stats)

            # Group matches by RoundID, then BoxName
            grouped_matches = defaultdict(lambda: defaultdict(list))
            for row in previous_matches_data:
                round_id = row[0]
                round_name = row[1]
                round_start_date = row[2].strftime("%Y-%m-%d") if row[2] else 'N/A'
                round_end_date = row[3].strftime("%Y-%m-%d") if row[3] else 'N/A'
                box_name = row[4]
                match_details = row[5:] # Player1Name, Player2Name, Score, WinnerName, PlayedOn
                grouped_matches[(round_id, round_name, round_start_date, round_end_date)][box_name].append(match_details)


            # Get all unique round keys (round_id, name, start, end) from both data sets and sort them
            all_round_keys = set(grouped_standings.keys()) | set(grouped_matches.keys())

            for round_key in sorted(all_round_keys, key=lambda x: x[3], reverse=True): # Sort by EndDate DESC
                round_id, round_name, round_start_date, round_end_date = round_key
                html_sections += f'<h2>{round_name} ({round_start_date} - {round_end_date})</h2>\n'

                # Get all unique box names for this round from both data sets and sort them
                boxes_in_round = set(grouped_standings[round_key].keys()) | set(grouped_matches[round_key].keys())

                for box_name in sorted(boxes_in_round):
                    html_sections += f'<h3>Box {box_name}</h3>\n'

                    # --- Display Standings for this Box ---
                    if box_name in grouped_standings[round_key]:
                        html_sections += """
                        <h4>Standings</h4>
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
                        """
                    else:
                        html_sections += "<p>No standings available for this box in this round.</p>"


                    # --- Display Matches for this Box ---
                    if box_name in grouped_matches[round_key]:
                        html_sections += """
                        <h4>Matches</h4>
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
    <title>DTC Box League - Previous Rounds</title>
    <style>{COMMON_CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>DTC Box League</h1>
            <nav>
                <ul>
                    <li><a href="current_round_fixtures.html">Current Round Fixtures</a></li>
                    <li><a href="current_round_standings.html">Current Standings</a></li>
                    <li><a href="leaderboard.html">Overall Leaderboard</a></li>
                    <li><a href="previous_rounds.html" class="active">Previous Rounds</a></li>
                    <li><a href="info_rules.html">Info & Rules</a></li> </ul>
            </nav>
        </header>

        <main>
            <h1>Previous Rounds Overview</h1>
            {html_sections}
        </main>

        <footer>
            <p>Data last updated: <span id="last-updated">{current_time}</span></p>
            <p>&copy; {datetime.datetime.now().year} Digswell Tennis Club Box League</p>
        </footer>
    </div>
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
        print(f"Please check your DB_SERVER, DB_NAME, ODBC_DRIVER settings, and that SQL Server is running.")
        print(f"Also ensure your views 'dbo.vw_PreviousRoundStandings' and 'dbo.vw_PreviousRoundMatches' exist and return data.")
    except Exception as e:
        print(f"An unexpected error occurred in generate_previous_rounds_report: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --- Main Execution Block ---
if __name__ == "__main__":
    print("Starting HTML report generation...")
    generate_current_round_fixtures_report()
    generate_current_round_standings_report()
    generate_leaderboard_report()
    generate_previous_rounds_report()
    print("All HTML reports generated!")