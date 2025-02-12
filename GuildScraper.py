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

def parse_html_to_player_data(html_content):
    """
    Parses the HTML content to extract player data (name, ally code, GP).
    Args:
        html_content (str): The HTML content.

    Returns:
        list[dict]: List of dictionaries containing player data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table containing the player data
    table = soup.find("table", class_="data-table")

    # List to store extracted data
    players_data = []

    # Iterate through each row in the table body
    for row in table.find("tbody").find_all("tr"):
        # Extract the player name
        player_name = row.find("div", class_="fw-bold text-white").text.strip()

        # Extract the ally code from the href attribute of the link
        ally_code = row.find("a")["href"].split("/")[-2]

        # Extract the Galactic Power (GP)
        gp = row.find_all("td")[1].text.strip()

        # Append the extracted data to the list
        players_data.append({
            "player_name": player_name,
            "ally_code": ally_code,
            "gp": gp
        })
    
    return players_data

def write_player_data_to_csv(players_data, csv_file):
    """
    Writes player data to a CSV file.

    Args:
        players_data (list[dict]): List of dictionaries containing player data.
        csv_file (str): Path to the CSV file to write to.
    """
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["player_name", "ally_code", "gp"])
        writer.writeheader()  # Write the header row
        writer.writerows(players_data)  # Write the data rows

    print(f"Data has been written to {csv_file}.")

def scrape_guild(url, csv_file):
    """
    Scrapes guild data and writes it to a CSV file.
    Args:
        url (str): The URL of the guild page.
        csv_file (str): Path to the CSV file.
    """
    print(f"Fetching data from {url}...")
    html_content = fetch_html_from_url(url)
    players_data = parse_html_to_player_data(html_content)
    write_player_data_to_csv(players_data, csv_file)

if __name__ == "__main__":
    # Specify the URL and output CSV file
    url = "https://swgoh.gg/g/tgo6MJitRvqRRvARhr60pQ/"
    output_csv = "players_data.csv"

    # Run the scrape_guild function
    scrape_guild(url, output_csv)
