#menu scraper
from bs4 import BeautifulSoup
import requests

def scrape_nutrislice(dining_hall, meal, date):
    url = f"https://rutgers.nutrislice.com/menu/{dining_hall}/{meal}/{date}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Inspect the page and find food items
    # Return list of food items
    pass