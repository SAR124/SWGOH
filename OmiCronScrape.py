import requests
from bs4 import BeautifulSoup
import csv

def fetch_html_from_url(url):
    """
    Fetches the HTML content from a URL.
    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails
    return response.text

def parse_characters_and_relic_levels(html_content, ally_code):
    """
    Parses the HTML content to extract character names, relic levels, and Omicron status.
    Args:
        html_content (str): The HTML content.
        ally_code (str): The ally code of the player.

    Returns:
        list[dict]: List of dictionaries containing character names, relic levels, and Omicron status.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # List to store character data
    character_data = []

    # Find all character cards
    character_cards = soup.find_all("div", class_="unit-card")

    for card in character_cards:
        # Extract character name
        name_div = card.find("div", class_="unit-card__name")
        character_name = name_div.text.strip() if name_div else "Unknown"

        # Extract relic level
        relic_div = card.find("div", class_="relic-badge")  # Check for relic badge
        if relic_div:
            relic_level = relic_div.text.strip()
        else:
            relic_level = "0"  # Default to 0 if no relic is present

        # Check for Omicron
        omicron_div = card.find("div", class_="character-portrait__omicron")  # Change this if necessary
        has_omicron = "Yes" if omicron_div else "No"

        # Debugging output
        print(f"Character: {character_name}, Relic Level: {relic_level}, Omicron: {has_omicron}")

        # Append the character data
        character_data.append({
            "ally_code": ally_code,
            "character_name": character_name,
            "relic_level": relic_level,
            "omicron_applied": has_omicron
        })

    return character_data

def write_character_data_to_csv(character_data, csv_file):
    """
    Writes character data to a CSV file.

    Args:
        character_data (list[dict]): List of dictionaries containing character data.
        csv_file (str): Path to the CSV file to write to.
    """
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ally_code", "character_name", "relic_level", "omicron_applied"])
        writer.writeheader()  # Write the header row
        writer.writerows(character_data)  # Write the data rows

    print(f"Data has been written to {csv_file}.")

def main(url, csv_file, ally_code):
    """
    Main function to fetch HTML, parse character data, and write to a CSV.

    Args:
        url (str): The URL to fetch.
        csv_file (str): Path to the CSV file.
        ally_code (str): The ally code to include in the data.
    """
    print(f"Fetching data from {url}...")
    html_content = fetch_html_from_url(url)
    character_data = parse_characters_and_relic_levels(html_content, ally_code)
    write_character_data_to_csv(character_data, csv_file)

if __name__ == "__main__":
    # Specify the URL, output CSV file, and ally code
    url = "https://swgoh.gg/p/317416922/characters/"  # Replace with actual player character URL
    output_csv = "character_relic_data.csv"
    ally_code = "317416922"  # Replace with actual ally code

    # Run the main function
    main(url, output_csv, ally_code)
