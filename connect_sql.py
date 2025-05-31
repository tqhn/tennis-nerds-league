import pyodbc

try:
    # --- SQL Server Connection Details ---
    # IMPORTANT: Customize these values for YOUR SQL Server setup.
    YOUR_SERVER_NAME = r"tariqhassan2022\SQLEXPRESS"  # Or '.', 'YOURCOMPUTERNAME\SQLEXPRESS', etc.
    YOUR_DATABASE_NAME = r"DTC Box League" # The name of the database where your 'boxes' table is.
    ODBC_DRIVER_NAME = r"{ODBC Driver 17 for SQL Server}" # Or {ODBC Driver 18 for SQL Server}, {SQL Server}, etc.

    conn_str = (
        f"DRIVER={ODBC_DRIVER_NAME};"
        f"SERVER={YOUR_SERVER_NAME};"
        f"DATABASE={YOUR_DATABASE_NAME};"
        f"Trusted_Connection=yes;" # Use this for Windows Authentication
        # If using SQL Server Authentication, uncomment and fill these:
        # f"UID=YOUR_USERNAME;"
        # f"PWD=YOUR_PASSWORD;"
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    print("Successfully connected to SQL Server using Windows Authentication!")

    # --- Querying your 'boxes' table ---
    # This query assumes your table is named 'boxes' and has columns 'id' and 'box_name'.
    sql_query = "SELECT id, box_name FROM boxes ORDER BY id ASC;" # Added ORDER BY for consistent output

    print(f"\nExecuting query: {sql_query}")
    cursor.execute(sql_query)

    # Fetch all the rows returned by the query
    rows = cursor.fetchall()

    if rows:
        print("\n--- Data from 'boxes' table ---")
        # Print column headers (optional, but good practice)
        # You could fetch cursor.description for dynamic headers if needed
        print(f"{'ID':<5} | {'Box Name':<20}") # Basic header alignment
        print(f"-----|--------------------")

        for row in rows:
            # Each row is a tuple, e.g., (1, 'Red Box')
            print(f"{row[0]:<5} | {row[1]:<20}") # Aligning data
    else:
        print("\nNo data found in the 'boxes' table. The table might be empty.")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"\n--- ERROR CONNECTING TO SQL SERVER OR EXECUTING QUERY ---")
    print(f"Error: {ex}")
    print(f"SQLSTATE: {sqlstate}")

    print("\n**Common Troubleshooting Steps:**")
    print("1. **Verify Connection String:**")
    print(f"   - **SERVER:** Is '{YOUR_SERVER_NAME}' correct? (e.g., 'localhost', '.', or 'YOURCOMPUTERNAME\\SQLEXPRESS')")
    print(f"   - **DATABASE:** Is '{YOUR_DATABASE_NAME}' the exact database where your 'boxes' table lives?")
    print(f"   - **DRIVER:** Is '{ODBC_DRIVER_NAME}' exactly what's listed in 'ODBC Data Source Administrator' (Drivers tab)?")
    print("2. **Table/Column Name:** Does the table 'boxes' exist in '{YOUR_DATABASE_NAME}'? Are the columns exactly 'id' and 'box_name' (case-sensitive if your SQL Server collation is)?")
    print("3. **Permissions:** Does the Windows user running this script have permission to SELECT from the 'boxes' table in '{YOUR_DATABASE_NAME}'?")
    print("4. **SQL Server Services:** For named instances, ensure 'SQL Server Browser' service is running. Is your main SQL Server instance running?")
    print("5. **Firewall:** Could a firewall be blocking port 1433 (or custom port) on the SQL Server machine?")
    print("6. **Network:** Can you ping your server name/IP from the command prompt?")

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
        print("\nCursor closed.")
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")