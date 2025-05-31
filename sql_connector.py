import pyodbc

# --- Configuration for your SQL Server connection ---
# Replace this placeholder with your actual details
# IMPORTANT: Use 'r' before the string literal if your server name contains backslashes
SERVER_NAME = r'tariqhassan2022\SQLEXPRESS' # Example: r'MYPC\SQLEXPRESS' or r'localhost\SQLEXPRESS'

# Your database name
DATABASE_NAME = 'DTC Box League'

# --- Construct the connection string for Windows Authentication ---
# 'Trusted_Connection=yes' tells pyodbc to use the Windows credentials
# of the user running this Python script.
# We're using 'ODBC Driver 17 for SQL Server'.
CONN_STR = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={tariqhassan2022\SQLEXPRESS};"
    f"DATABASE={DTC Box League};"
    f"Trusted_Connection=yes;"
)

# --- Test the connection and fetch data ---
try:
    # Establish the connection
    cnxn = pyodbc.connect(CONN_STR)
    cursor = cnxn.cursor()

    print("Successfully connected to SQL Server using Windows Authentication!")

    # Example: Fetch 5 players from the players table
    print("\nFetching players from dbo.players:")
    cursor.execute("SELECT TOP 5 id, player_name FROM dbo.players")
    rows = cursor.fetchall()

    if rows:
        print("Player ID | Player Name")
        print("--------------------")
        for row in rows:
            print(f"{row.id:<9} | {row.player_name}")
    else:
        print("No players found in dbo.players or table is empty.")

    # Example: Fetch 5 matches from the matches table
    print("\nFetching matches from dbo.matches (first 5 rows):")
    cursor.execute("SELECT TOP 5 id, round_id, player1_id, player2_id, played_on FROM dbo.matches")
    match_rows = cursor.fetchall()

    if match_rows:
        print("Match ID | Round ID | P1 ID | P2 ID | Played On")
        print("-------------------------------------------------")
        for row in match_rows:
            # Check if played_on is not None before formatting
            played_on_str = row.played_on.strftime('%Y-%m-%d') if row.played_on else 'N/A'
            print(f"{row.id:<8} | {row.round_id:<8} | {row.player1_id:<5} | {row.player2_id:<5} | {played_on_str}")
    else:
        print("No matches found in dbo.matches or table is empty.")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"\nError connecting to SQL Server or executing query: {sqlstate}")
    print(f"Error details: {ex}")
    print("\nPlease check:")
    print("1. SQL Server is running.")
    print("2. 'ODBC Driver 17 for SQL Server' is installed.")
    print("3. Your Server Name and Database Name are correct.")
    print("4. Your Windows user has permissions to access the 'DTC Box League' database.")
    print("5. SQL Server is configured to allow 'Windows Authentication'.")
    print("6. If using IP address, ensure SQL Server Network Configuration (TCP/IP) is enabled.")

finally:
    # Close the connection
    if 'cnxn' in locals() and cnxn:
        cnxn.close()
        print("\nConnection closed.")