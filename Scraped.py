'''

Thank You for given me this assignment and opportunity.

--------------ASSIGNMENT-----------------

Part 1
In this assignment you are required to scrape all products from this URL: 
https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2
C283&ref=sr_pg_1
Need to scrape atleast 20 pages of product listing pages
Items to scrape
• Product URL
• Product Name
• Product Price
• Rating
• Number of reviews

Part 2
With the Product URL received in the above case, hit each URL, and add below items:
• Description
• ASIN
• Product Description
• Manufacturer
Need to hit around 200 product URL’s and fetch various information.
The entire data needs to be exported in a csv format

Must be sure to have the Beautiful Soup4, and Requests Libraries.
'''

import csv
import requests
from bs4 import BeautifulSoup


def scrape_product_list(url): # Send a GET request to the URL
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    product_listings = soup.find_all('div', {'data-component-type': 's-search-result'})

    scraped_data = []

   
    for listing in product_listings:
        
        product_url = listing.find('a', class_='a-link-normal')['href']
        product_name = listing.find('span', class_='a-size-medium').text.strip()
        product_price = listing.find('span', class_='a-price-whole').text.strip()
        rating = listing.find('span', {'class': 'a-icon-alt'}).text.split(' ')[0]
        num_reviews_element = listing.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        num_reviews = num_reviews_element.text.strip() if num_reviews_element else 'N/A'

        
        product_data = {
            'Product URL': 'https://www.amazon.in' + product_url,
            'Product Name': product_name,
            'Product Price': product_price,
            'Rating': rating,
            'Number of reviews': num_reviews
        }

        
        scraped_data.append(product_data)

    return scraped_data



def scrape_product_details(url):
    
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    soup = BeautifulSoup(response.text, 'html.parser')

    
    description_element = soup.find('div', {'id': 'productDescription'})
    description = description_element.text.strip() if description_element else 'N/A'

    asin_element = soup.find('th', string='ASIN')
    asin = asin_element.find_next_sibling('td').text.strip() if asin_element else 'N/A'

    product_description_element = soup.find('div', {'id': 'feature-bullets'})
    product_description = product_description_element.text.strip() if product_description_element else 'N/A'

    manufacturer_element = soup.find('a', {'id': 'bylineInfo'})
    manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

    
    product_data = {
        'Description': description,
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }

    return product_data


# Main function to scrape multiple pages and save data to CSV
def scrape_and_save_data():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    total_pages = 20  
    products_per_page = 10 
    total_products = 200  
    scraped_data = []

    
    for page in range(1, total_pages + 1):
        url = base_url + str(page)
        product_listings = scrape_product_list(url)

        
        for product_listing in product_listings:
            product_url = product_listing['Product URL']

            
            product_details = scrape_product_details(product_url)

            
            product_data = {**product_listing, **product_details}

          
            scraped_data.append(product_data)

            
            if len(scraped_data) == total_products:
                break

       
        if len(scraped_data) == total_products:
            break

    # Save the scraped data to a CSV file
    filename = 'scraped_data.csv'
    field_names = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of reviews',
                   'Description', 'ASIN', 'Product Description', 'Manufacturer']

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(scraped_data)

    print(f"Data saved to {filename} successfully.")


# Call the main function to start scraping and saving data
scrape_and_save_data()
