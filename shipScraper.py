import csv
import requests
from bs4 import BeautifulSoup

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

def parse_ships_and_stars(html_content, ally_code):
    """
    Parses the HTML content to extract ship names, star levels, and ally code.
    Args:
        html_content (str): The HTML content.
        ally_code (str): The ally code to include in the data.

    Returns:
        list[dict]: List of dictionaries containing ship names, star levels, and ally code.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # List to store ship data
    ship_data = []

    # Find all ship cards
    ship_cards = soup.find_all("div", class_="unit-card-grid__cell")

    for card in ship_cards:
        # Extract ship name from the data-unit-name attribute
        ship_name = card.get("data-unit-name", "Unknown")

        # Find the rarity range (star levels)
        rarity_div = card.find("div", class_="rarity-range")
        if rarity_div:
            # Count stars without the "rarity-range__star--inactive" class
            active_stars = len([
                star for star in rarity_div.find_all("div", class_="rarity-range__star")
                if "rarity-range__star--inactive" not in star.get("class", [])
            ])
        else:
            active_stars = 0  # Default to 0 if no stars are found

        # Debugging output
        print(f"Ship: {ship_name}, Stars: {active_stars}, Ally Code: {ally_code}")

        # Append the ship data
        ship_data.append({
            "ally_code": ally_code,
            "ship_name": ship_name,
            "stars": active_stars
        })

    return ship_data

def write_ship_data_to_csv(ship_data, csv_file):
    """
    Writes ship data to a CSV file.

    Args:
        ship_data (list[dict]): List of dictionaries containing ship data.
        csv_file (str): Path to the CSV file to write to.
    """
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["ally_code", "ship_name", "stars"])
        writer.writeheader()  # Write the header row
        writer.writerows(ship_data)  # Write the data rows

    print(f"Data has been written to {csv_file}.")

def main(url, csv_file, ally_code):
    """
    Main function to fetch HTML, parse ship data, and write to a CSV.

    Args:
        url (str): The URL to fetch.
        csv_file (str): Path to the CSV file.
        ally_code (str): The ally code to include in the data.
    """
    print(f"Fetching data from {url}...")
    html_content = fetch_html_from_url(url)
    ship_data = parse_ships_and_stars(html_content, ally_code)
    write_ship_data_to_csv(ship_data, csv_file)

if __name__ == "__main__":
    # Specify the URL, output CSV file, and ally code
    url = "https://swgoh.gg/p/317416922/ships/"
    output_csv = "ship_data.csv"
    ally_code = "317416922"  # Replace with your ally code

    # Run the main function
    main(url, output_csv, ally_code)
