import pyodbc
import datetime
import os
from collections import defaultdict
from playwright.sync_api import sync_playwright 
import time
import shutil

# --- Configuration ---
DB_SERVER = 'tariqhassan2022\SQLEXPRESS'
DB_NAME = 'DTC Box League'
ODBC_DRIVER = 'ODBC Driver 17 for SQL Server' 

# Output directory 
output_dir = 'docs_test'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Directory for CSS files 
css_dir = os.path.join(output_dir, 'css') 
if not os.path.exists(css_dir):
    os.makedirs(css_dir)

# Directory for assets 
assets_dir = os.path.join(output_dir, 'assets')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Path to the logo image (keep as before)
LOGO_PATH = 'assets/TNL_logo.png' 

# Make sure logo path exists or warn (optional)
# Define the target Instagram resolution
INSTA_WIDTH = 1080
INSTA_HEIGHT = 1920 

# Local source of your background image (developer-provided path in container)
LOCAL_BK_IMAGE_SRC = '/mnt/data/bk-image.PNG'   # <-- local path provided by developer
COPIED_BK_IMAGE_NAME = 'bk-image.png'           # name inside docs_test/assets
TARGET_BK_IMAGE_PATH = os.path.join(assets_dir, COPIED_BK_IMAGE_NAME)

# --- Helper Function: Player Name Formatting (Unchanged) ---
def format_player_name(full_name):
    """Converts 'Firstname Lastname' to 'Firstname L.'"""
    if not full_name:
        return ""
    parts = full_name.split()
    if len(parts) > 1:
        first_name = parts[0]
        last_initial = parts[-1][0].upper()
        return f"{first_name} {last_initial}."
    return full_name 

# ---------------------------------------------
# --- Helper Function: CSS Generation (UPDATED) ---
def create_instagram_post_css():
    """
    Creates the dedicated CSS for the Instagram posts.
    Uses the background image placed into docs_test/assets/bk-image.png
    and removes the previous .top-graphic-overlay element entirely.
    """
    # Keep font import and text styles; remove overlay and background-color usage.
    css_content = f"""
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap');

    /* General Styling for screenshot optimization */
    body {{
        font-family: 'Montserrat', sans-serif;
        background-color: #f5f5f5ff; 
        margin: 0;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 10vh;
    }}

    /* Instagram Post Container Styling (9:16 IG Story Aspect Ratio: 1080x1920px) */
    .insta-post {{
        width: 1080px; 
        height: 1920px; /* 9:16 Story Aspect Ratio */

        /* NEW: Use the bundled background image from docs_test/assets */
        /* CSS file is located in docs_test/css, so ../assets/bk-image.png is correct */
        background-image: url('../assets/{COPIED_BK_IMAGE_NAME}');
        background-size: cover;        /* fills the 1080×1920 cleanly */
        background-position: center;   /* keeps image centered */
        background-repeat: repeat;
        /* Implementing the recommended 250px top/bottom safe zone */
        padding: 250px 50px 250px 50px; 
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: flex-start; 
        align-items: center;
        text-align: center;
        position: relative;
        overflow: hidden; 
    }}

    /* Titles and text should sit above the background image */
    .insta-post h2 {{ 
        font-family: 'Montserrat', sans-serif;
        font-size: 3.5em; 
        font-weight: 800;
        margin-top: 0px; 
        margin-bottom: 20px;
        color: #8bc34a;
        line-height: 1.2;
        position: relative; 
        z-index: 1; 
    }}
    
    .insta-post .report-date {{
        font-size: 1.8em;
        font-weight: 700;
        color: #333; 
        margin-top: -10px; 
        margin-bottom: 20px;
        width: auto; 
        position: relative; 
        z-index: 1;
    }}
    
    .insta-post h3 {{ 
        font-family: 'Montserrat', sans-serif;
        font-size: 2.5em;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #333;
        position: relative; 
        z-index: 1;
    }}
    
    /* Table Styling */
    .insta-post table {{
        width: 100%; 
        margin-top: 10px;
        border-collapse: collapse;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        position: relative; 
        z-index: 1;
        background-color: rgba(255,255,255,0); /* transparent to let bg show */
    }}
    .insta-post th, .insta-post td {{
        padding: 18px;
        font-size: 1.6em;
        font-weight: 600;
        border-bottom: 1px solid #eee;
        white-space: nowrap;
        background-color: transparent; 
    }}
    .insta-post th {{
        color: #555;
        border-bottom: 5px solid #8bc34a; 
    }}
    
    .insta-post #insta_post_1_standings td:first-child,
    .insta-post #insta_post_3_leaderboard td:first-child {{ 
        font-weight: 800; 
        color: #8bc34a; 
    }}
    
    .insta-post #insta_post_2_matches_summary td:first-child {{ 
        font-weight: 600; 
        color: #333; 
        white-space: normal; 
    }}
    
    .match-comment-full {{
        font-size: 0.8em; 
        font-weight: 400;
        color: #222222;
        padding-top: 5px;
        margin-top: 5px;
        border-top: 1px dotted #ccc; 
        line-height: 1.2;
        text-align: left; 
        white-space: normal; 
        position: relative;
        z-index: 1;
    }}
    
    .comment-title {{
        font-weight: 700;
        color: #333;
        margin-right: 5px;
    }}

    /* Footer */
    .insta-footer {{
        position: absolute;
        bottom: 50px; 
        left: 50%; 
        transform: translateX(-50%); 
        right: auto; 
        display: flex;
        justify-content: center; 
        align-items: center;
        width: auto;
        z-index: 1; 
    }}
    
    .insta-footer .logo-img {{
        width: 250px; 
        height: 250px; 
        object-fit: contain;
    }}
    """
    css_file_path = os.path.join(css_dir, 'insta_style.css')
    with open(css_file_path, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"Wrote CSS to {css_file_path}")

# --- Post 1: Current Round Standings (UNIFIED HTML with overlay removed) ---
def generate_current_standings_post():
    """Generates the Current Round Top Box Standings post HTML."""
    conn = None
    cursor = None
    html_sections = ""
    output_file_path = os.path.join(output_dir, 'insta_post_1_standings.html')

    try:
        today_date = datetime.date.today().strftime('%d %b %Y').lstrip('0')
        
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
        round_date_range = ""
        if round_info:
            round_name = round_info[0]
            start_date_obj = round_info[1]
            end_date_obj = round_info[2]
            round_date_range = f"({start_date_obj.strftime('%d %b')} - {end_date_obj.strftime('%d %b')})"

        cursor.execute("""
             SELECT
                 BoxName, PlayerName, MatchesPlayed, Wins, Losses, Points, RankInBox
             FROM dbo.vw_CurrentStandings
             ORDER BY BoxName ASC, RankInBox ASC
        """)
        standings_data = cursor.fetchall()
        
        if not standings_data:
            html_sections = "<p style='font-size:2em; margin-top:200px;'>No standings available for the current round.</p>"
        else:
            grouped_standings = defaultdict(list)
            for row in standings_data:
                grouped_standings[row[0]].append(row[1:]) 
            
            top_boxes = sorted(grouped_standings.keys())[:3] 
            
            for box_name in top_boxes:
                html_sections += f"<h3>{box_name} Standings</h3>"
                html_sections += """
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Player</th>
                            <th>Played</th>
                            <th>Points</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                for player_stats in grouped_standings[box_name]:
                    player_name = format_player_name(player_stats[0]) 
                    matches_played = player_stats[1]
                    points = int(player_stats[4])
                    rank = player_stats[5]
                    html_sections += f"""
                        <tr>
                            <td>#{rank}</td>
                            <td>{player_name}</td>
                            <td>{matches_played}</td>
                            <td>{points}</td>
                        </tr>
                    """
                html_sections += "</tbody></table>"
        post_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Post - Standings</title>
    <link rel="stylesheet" href="css/insta_style.css">
</head>
<body>
    <div class="insta-post" id="insta_post_1_standings">
        <h2>{round_name} <br> Current Standings</h2>
        <div class="report-date">{today_date}</div>
        {html_sections}
        <div class="insta-footer">
            <img src="{LOGO_PATH}" alt="Logo" class="logo-img">
        </div>
    </div>
</body>
</html>
        """
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(post_html)
        print(f"Generated {output_file_path} (Current Standings Post) successfully!")
        return output_file_path

    except pyodbc.Error as ex:
        print(f"Database error in generate_current_standings_post: {ex}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_current_standings_post: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return None

# ---------------------------------------------

# --- Post 2: Summary of Matches Played So Far (UNIFIED HTML with overlay removed) ---
def generate_matches_summary_post():
    """
    Generates a summary of played matches, filtered by user input ('all' or 'week').
    """
    conn = None
    cursor = None
    html_sections = ""
    output_file_path = os.path.join(output_dir, 'insta_post_2_matches_summary.html')
    
    today_date = datetime.date.today().strftime('%d %b %Y').lstrip('0')

    time_filter = input("Show matches from 'all' time or last 'week'? Enter 'all' or 'week': ").lower().strip()
    
    if time_filter not in ['all', 'week']:
        print("Invalid input. Defaulting to 'all' matches.")
        time_filter = 'all'

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
             SELECT TOP 1 [name]
             FROM dbo.rounds
             WHERE GETDATE() BETWEEN start_date AND end_date
             ORDER BY start_date DESC
        """)
        round_info = cursor.fetchone()
        round_name = round_info[0] if round_info else "Current Round"

        sql_query = """
             SELECT BoxName, Player1Name, Player2Name, Score, WinnerName, PlayedOn, Comments_Match_Summary 
             FROM dbo.vw_CurrentRoundMatches 
             WHERE WinnerName IS NOT NULL AND WinnerName <> 'Pending' 
        """
        
        heading_text = "Recent Results"
        
        if time_filter == 'week':
            sql_query += "AND PlayedOn >= DATEADD(day, -7, GETDATE()) "
            heading_text = "Last Week's Results"
        elif time_filter == 'all':
            heading_text = "Match Results"

        sql_query += "ORDER BY BoxName ASC, PlayedOn DESC, Player1Name ASC"
        
        cursor.execute(sql_query)
        matches_data = cursor.fetchall() 
        
        
        if not matches_data:
            html_sections = f"<p style='font-size:2em; margin-top:200px;'>No matches found for {heading_text.lower()} in the current round yet.</p>"
        else:
            grouped_matches = defaultdict(list)
            for row in matches_data:
                grouped_matches[row[0]].append(row[1:])
            
            top_boxes = sorted(grouped_matches.keys())[:3] 
            
            for box_name in top_boxes:
                box_matches = grouped_matches[box_name]
                
                if not box_matches:
                    html_sections += f"<h3>{box_name} Results</h3><p>No results posted yet.</p>"
                    continue
                    
                html_sections += f"<h3>{box_name} Results</h3>"
                html_sections += """
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Matchup</th>
                            <th>Winner & Score</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                for match in box_matches:
                    player1_name = format_player_name(match[0]) 
                    player2_name = format_player_name(match[1]) 
                    score = match[2] if match[2] else 'Unknown Score'
                    
                    winner_full_name = match[3] 
                    formatted_winner = format_player_name(winner_full_name) 

                    comments = match[5].strip() if match[5] else None 
                    
                    comment_content = comments if comments else ""
                        
                    comment_html = f"""
                        <div class='match-comment-full'>
                            <span class='comment-title'>Comments/Match Summary:</span> {comment_content}
                        </div>
                    """
                    
                    match_summary = f"""
                        {player1_name} vs {player2_name}
                        {comment_html}
                    """
                        
                    result_cell = f"<strong style='color:#388e3c;'>{formatted_winner if formatted_winner else 'Draw'}</strong><br><small>({score})</small>" 
                        
                    html_sections += f"""
                        <tr>
                            <td style="text-align:left; vertical-align:top;">{match_summary}</td>
                            <td style="text-align:center; vertical-align:top;">{result_cell}</td>
                        </tr>
                    """
                html_sections += "</tbody></table>"

        post_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Post - Matches Summary</title>
    <link rel="stylesheet" href="css/insta_style.css">
</head>
<body>
    <div class="insta-post" id="insta_post_2_matches_summary">
        <h2>{round_name} <br> {heading_text}</h2>
        <div class="report-date">{today_date}</div>
        {html_sections}
        <div class="insta-footer">
            <img src="{LOGO_PATH}" alt="Logo" class="logo-img">
        </div>
    </div>
</body>
</html>
        """
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(post_html)
        print(f"Generated {output_file_path} (Matches Summary Post - Filter: {time_filter}) successfully!")
        return output_file_path

    except pyodbc.Error as ex:
        print(f"Database error in generate_matches_summary_post: {ex}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_matches_summary_post: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return None


# --- Post 3: Leaderboard Report (UNIFIED HTML with overlay removed) ---
def generate_leaderboard_post():
    """Generates the overall top 10 players Leaderboard post HTML."""
    conn = None
    cursor = None
    html_sections = ""
    output_file_path = os.path.join(output_dir, 'insta_post_3_leaderboard.html')

    try:
        today_date = datetime.date.today().strftime('%d %b %Y').lstrip('0')
        
        conn_str = (
            f"DRIVER={{{ODBC_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
             SELECT TOP 10 PlayerName, TotalPoints, OverallRank 
             FROM dbo.vw_OverallLeaderboard 
             ORDER BY OverallRank ASC
        """)
        leaderboard_data = cursor.fetchall()
        
        if not leaderboard_data:
            html_sections = "<p style='font-size:2em; margin-top:200px;'>No overall leaderboard data available.</p>"
        else:
            html_sections += """
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Overall Ranking Points</th>
                    </tr>
                </thead>
                <tbody>
            """
            for row in leaderboard_data:
                player_name = format_player_name(row[0]) 
                total_points = int(row[1])
                rank = row[2] 
                html_sections += f"""
                    <tr>
                        <td>#{rank}</td>
                        <td>{player_name}</td>
                        <td>{total_points}</td>
                    </tr>
                """
            html_sections += "</tbody></table>"

        post_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Post - Leaderboard</title>
    <link rel="stylesheet" href="css/insta_style.css">
</head>
<body>
    <div class="insta-post" id="insta_post_3_leaderboard">
        <h2>Overall League <br> Leaderboard</h2>
        <div class="report-date">{today_date}</div>
        {html_sections}
        <div class="insta-footer">
            <img src="{LOGO_PATH}" alt="Logo" class="logo-img">
        </div>
    </div>
</body>
</html>
        """
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(post_html)
        print(f"Generated {output_file_path} (Leaderboard Post) successfully!")
        return output_file_path

    except pyodbc.Error as ex:
        print(f"Database error in generate_leaderboard_post: {ex}")
    except Exception as e:
        print(f"An unexpected error occurred in generate_leaderboard_post: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return None

# ---------------------------------------------


# --- Automated Screenshot Function (Unchanged) ---
def capture_insta_post_png(html_file_path, output_png_name):
    """
    Uses Playwright (Chromium) to open the HTML file, capture the 
    .insta-post element, and save it as a PNG.
    """
    output_png_path = os.path.join(output_dir, output_png_name)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                viewport={'width': INSTA_WIDTH + 50, 'height': INSTA_HEIGHT + 50} 
            )
            page = context.new_page()

            full_path = 'file:///' + os.path.abspath(html_file_path).replace('\\', '/')
            page.goto(full_path)
            
            page.wait_for_selector('.insta-post') 

            page.locator('.insta-post').screenshot(path=output_png_path)
            
            browser.close()
            
            print(f"Successfully captured PNG using Playwright: {output_png_path}")
            return output_png_path

    except Exception as e:
        print(f"Error capturing screenshot for {html_file_path}: {e}")
        print("\n*** ACTION REQUIRED ***")
        print("Please ensure Playwright is installed correctly:")
        print("1. pip install playwright")
        print("2. playwright install")
        print("***********************\n")
        return None


# --- Main Execution Block ---
if __name__ == "__main__":
    print("Starting Instagram post generation...")

    # Copy the background image from the provided container path into docs_test/assets/
    try:
        if os.path.exists(LOCAL_BK_IMAGE_SRC):
            shutil.copyfile(LOCAL_BK_IMAGE_SRC, TARGET_BK_IMAGE_PATH)
            print(f"Copied background image to: {TARGET_BK_IMAGE_PATH}")
        else:
            print(f"Warning: local background image not found at {LOCAL_BK_IMAGE_SRC}.")
            print("Make sure your bk-image.png is placed into the docs_test/assets/ folder or update LOCAL_BK_IMAGE_SRC.")
    except Exception as e:
        print(f"Failed to copy background image: {e}")

    # 1. Create the dedicated CSS file
    create_instagram_post_css()

    # 2. Generate the three HTML files (The match summary will prompt for input)
    standings_html_path = generate_current_standings_post()
    matches_html_path = generate_matches_summary_post()
    leaderboard_html_path = generate_leaderboard_post()
    
    print("\n--- Starting Automated PNG Capture (Using Playwright) ---\n")

    # 3. Capture the PNGs from the generated HTML files
    if standings_html_path:
        capture_insta_post_png(standings_html_path, 'insta_post_1_standings.png')
        
    if matches_html_path:
        capture_insta_post_png(matches_html_path, 'insta_post_2_matches_summary.png')

    if leaderboard_html_path:
        capture_insta_post_png(leaderboard_html_path, 'insta_post_3_leaderboard.png')
    
    print("\nGeneration Complete! Check the 'docs_test' folder for your PNG files.")
