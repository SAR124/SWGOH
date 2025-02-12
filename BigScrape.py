import csv
import os
from GuildScraper import scrape_guild
from PlayerScraper import parse_characters_and_relic_levels
from shipScraper import parse_ships_and_stars
from bs4 import BeautifulSoup
import requests


def fetch_html_from_url(url):
    """
    Fetches the HTML content from a URL.
    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def read_player_data(player_data_csv):
    """
    Reads player data from the player_data.csv file.
    Args:
        player_data_csv (str): The file path of the player data CSV.

    Returns:
        list[dict]: A list of player data dictionaries.
    """
    with open(player_data_csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def write_to_csv(data, csv_file, fieldnames, mode="w"):
    """
    Writes data to a CSV file.
    Args:
        data (list[dict]): The data to write.
        csv_file (str): The CSV file path.
        fieldnames (list[str]): The column headers.
        mode (str): The file mode ('w' for overwrite, 'a' for append).
    """
    with open(csv_file, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if mode == "w":  # Write header only if overwriting
            writer.writeheader()
        writer.writerows(data)


def scrape_guild_characters_and_ships(guild_url, output_dir):
    """
    Scrapes all character and ship data for a guild.
    Args:
        guild_url (str): The guild URL.
        output_dir (str): The directory to save the CSV files.
    """
    # File paths
    player_data_csv = os.path.join(output_dir, "player_data.csv")
    character_csv = os.path.join(output_dir, "character_relic_data.csv")
    ship_csv = os.path.join(output_dir, "ship_data.csv")

    # Step 1: Scrape guild data
    print("Scraping guild player data...")
    scrape_guild(guild_url, player_data_csv)

    # Step 2: Read player data
    players = read_player_data(player_data_csv)
    print(f"Found {len(players)} players in the guild.")

    # Step 3: Initialize CSV files for character and ship data
    write_to_csv([], character_csv, ["ally_code", "character_name", "relic_level", "omicron_applied"], mode="w")
    write_to_csv([], ship_csv, ["ally_code", "ship_name", "stars"], mode="w")

    # Step 4: Scrape character and ship data for each player
    base_profile_url = "https://swgoh.gg/p/"

    for player in players:
        ally_code = player["ally_code"]
        print(f"Scraping data for player: {player['player_name']} (Ally Code: {ally_code})")

        # Scrape character data
        character_url = f"{base_profile_url}{ally_code}/characters/"
        # Inside your loop in BigScrape.py
        character_html = fetch_html_from_url(character_url)
        characters = parse_characters_and_relic_levels(character_html, ally_code)
        write_to_csv(characters, character_csv, ["ally_code", "character_name", "relic_level", "omicron_applied"], mode="a")


        # Scrape ship data
        ship_url = f"{base_profile_url}{ally_code}/ships/"
        ship_html = fetch_html_from_url(ship_url)
        ships = parse_ships_and_stars(ship_html, ally_code)
        write_to_csv(ships, ship_csv, ["ally_code", "ship_name", "stars"], mode="a")

    print("Scraping completed!")


if __name__ == "__main__":
    # Guild URL and output directory
    guild_url = "https://swgoh.gg/g/tgo6MJitRvqRRvARhr60pQ/"  # Replace with your guild URL
    output_dir = "./output"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Run the scraper
    scrape_guild_characters_and_ships(guild_url, output_dir)
