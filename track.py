import requests
from bs4 import BeautifulSoup
import re
import csv

def fetch_immoscoop_page():
    url = "https://www.immoscoop.be/zoeken/te-huur/brugge/appartement?minBedrooms=1&maxBedrooms=2&maxPrice=900&maxEpcScore=200&sort=price%2CASC"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch page: Status code {response.status_code}")

def parse_property_cards(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all property cards
    property_cards = soup.find_all('a', attrs={'data-mobile-selector': 'property-card_card'})
    
    results = []
    
    for card in property_cards:
        property_data = {}
        
        # Extract the href (property URL)
        property_data['url'] = card['href']
        
        # Extract the price
        price_element = card.find('p', class_=lambda c: c and 'property-card_price__' in c)
        if price_element:
            # Remove non-digit characters and convert to integer
            price_text = price_element.text.strip()
            price_digits = re.sub(r'[^\d]', '', price_text)
            property_data['price'] = int(price_digits) if price_digits else None
        
        # Extract the EPC value
        epc_element = card.find('text', class_=lambda c: c and 'epc-icon_label__' in c, string=lambda s: s and len(s) <= 3 and s != 'EPC')
        if epc_element:
            property_data['epc'] = epc_element.text.strip()
        else:
            property_data['epc'] = None
        
        results.append(property_data)
    
    return results

def save_to_csv(properties, filename='immoscoop_properties.csv'):
    if not properties:
        print("No properties to save")
        return
    
    fieldnames = ['url', 'price', 'epc']
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for prop in properties:
            writer.writerow(prop)
    
    print(f"Saved {len(properties)} properties to {filename}")

# Example usage
if __name__ == "__main__":
    html_content = fetch_immoscoop_page()
    print(f"Successfully fetched {len(html_content)} bytes of HTML")
    
    properties = parse_property_cards(html_content)
    print(f"Found {len(properties)} properties")
    print(properties)
    
    save_to_csv(properties)