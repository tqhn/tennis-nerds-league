import itertools # This library is great for generating combinations

def generate_fixture_sql(round_id, box_id, player_ids):
    """
    Generates SQL INSERT statements for round-robin match fixtures
    for a given box and round, based on a list of player IDs.

    Args:
        round_id (int): The ID of the round for which to generate fixtures.
        box_id (int): The ID of the box for which to generate fixtures.
        player_ids (list): A list of integer player IDs assigned to this box.
    """
    print(f"-- SQL INSERT statements for Round ID: {round_id}, Box ID: {box_id}")
    print(f"-- Players involved: {player_ids}\n")

    if not player_ids or len(player_ids) < 2:
        print(f"-- Warning: Not enough players ({len(player_ids)}) provided to create fixtures.")
        print("-- Please provide at least 2 player IDs.")
        return

    # Generate all unique pairs of players (fixtures)
    # itertools.combinations(iterable, r) returns r-length tuples of elements from the input iterable.
    # This gives us all unique pairs for a round-robin format.
    fixtures = list(itertools.combinations(player_ids, 2))

    if not fixtures:
        print("-- No fixtures generated. This might happen if there's only one player.")
        return

    print(f"INSERT INTO dbo.matches (round_id, box_id, player1_id, player2_id) VALUES")

    # Format each fixture as a part of the VALUES clause
    insert_values = []
    for player1, player2 in fixtures:
        insert_values.append(f"({round_id}, {box_id}, {player1}, {player2})")

    # Join the values with a comma and print
    # Add a semicolon at the end of the last statement
    print(",\n".join(insert_values) + ";")

    print("\n-- Remember: These matches are initially unplayed. Update them with scores later.")

# --- Main execution block ---
if __name__ == "__main__":
    try:
        print("--- Generate Match Fixtures SQL ---")

        # Get inputs from the user
        current_round_id = int(input("Enter the Round ID (e.g., 1): "))
        current_box_id = int(input("Enter the Box ID (e.g., 10): "))

        # Get player IDs as a comma-separated string, then convert to a list of integers
        players_input = input("Enter player IDs for this box, comma-separated (e.g., 1,2,3,4,5): ")
        
        # Clean and convert player IDs
        player_ids_list = [
            int(p.strip()) for p in players_input.split(',') if p.strip().isdigit()
        ]

        if not player_ids_list:
            print("Error: No valid player IDs entered. Please try again.")
        else:
            generate_fixture_sql(current_round_id, current_box_id, player_ids_list)

    except ValueError:
        print("Invalid input. Please ensure IDs are numbers and player IDs are comma-separated numbers.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")