import csv
from collections import defaultdict

# Load CSV Data
def load_csv_data(filename):
    """Loads CSV data into a list of dictionaries."""
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []

# Assign Players to ROTE Phase 1 Operations

def assign_players_to_operations(player_data, character_data, ship_data, rote_operations):
    """Assigns players to operations while ensuring max daily limits and unique character usage."""
    
    assignments = []
    
    # Convert player character and ship data into lookup dictionaries
    player_characters = defaultdict(dict)
    for char in character_data:
        player_characters[char["ally_code"]][char["character_name"]] = int(char["relic_level"])

    player_ships = defaultdict(dict)
    for ship in ship_data:
        player_ships[ship["ally_code"]][ship["ship_name"]] = int(ship["stars"])
    
    # Convert player GP data into a lookup dictionary
    player_gp = {p["ally_code"]: int(p["gp"].replace(",", "")) for p in player_data}

    # Track daily placements
    daily_limits = defaultdict(lambda: defaultdict(int))  # {day: {ally_code: count}}
    daily_character_usage = defaultdict(lambda: defaultdict(set))  # {day: {ally_code: {characters_used}}}

    # Sort players by least matches first (so those with most options go last)
    sorted_players = sorted(player_data, key=lambda p: len(player_characters[p["ally_code"]]))

    for op in rote_operations:
        alignment = op["alignment"]
        phase = op["phase"]
        planet = op["planet"]
        operation = op["operation"]
        required_character = op["character_name"]
        
        # FIX: Handle empty relicrequired values safely
        relic_required = int(op["relicrequired"]) if op["relicrequired"].strip().isdigit() else 0
        
        assigned = False

        # Try to assign the requirement to a player
        for day in [1, 2, 3]:  # Assign to Day 1 first, then Day 2, then Day 3
            for player in sorted_players:
                ally_code = player["ally_code"]
                player_name = player["player_name"]

                # Check if player has the required character at the required relic level
                if player_characters.get(ally_code, {}).get(required_character, 0) >= relic_required:
                    
                    # Check if the player has already used this character today
                    if required_character in daily_character_usage[day][ally_code]:
                        continue  # Skip if this character is already assigned today

                    # Check daily unit limit per alignment
                    if daily_limits[day][ally_code] < 10:
                        assignments.append({
                            "day": day,
                            "player_name": player_name,
                            "ally_code": ally_code,
                            "alignment": alignment,
                            "phase": phase,
                            "planet": planet,
                            "operation": operation,
                            "character_name": required_character,
                            "relic_required": relic_required
                        })
                        
                        # Increase daily count for this player
                        daily_limits[day][ally_code] += 1

                        # Mark character as used for the day
                        daily_character_usage[day][ally_code].add(required_character)

                        assigned = True
                        break  # Stop searching once assigned
            
            if assigned:
                break  # Move to next requirement

    return assignments



# Write Assignments to CSV
def write_assignments_to_csv(assignments, output_file):
    """Writes the assigned players to a CSV file."""
    fieldnames = ["day", "player_name", "ally_code", "alignment", "phase", "planet", "operation", "character_name", "relic_required"]
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(assignments)

    print(f"Assignments written to {output_file}")

# Main Execution
def main():
    # Load data from CSV files
    player_data = load_csv_data("player_data.csv")
    character_data = load_csv_data("character_relic_data.csv")
    ship_data = load_csv_data("ship_data.csv")
    rote_operations = load_csv_data("ROTE_OPERATIONS.csv")

    # Assign players to missions
    assignments = assign_players_to_operations(player_data, character_data, ship_data, rote_operations)

    # Write assignments to a CSV file
    write_assignments_to_csv(assignments, "rote_phase_one_assignments.csv")

if __name__ == "__main__":
    main()
