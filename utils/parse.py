import os
import requests
import json
from bs4 import BeautifulSoup
import google.generativeai as genai
import logging 
from database.category import create_category, get_categories

logger = logging.getLogger(__name__)
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config={"response_mime_type": "application/json"})
chat = model.start_chat()

def get_html(url: str):
    """
    Given a url, use the requests library to get the HTML of the page.
    """
    logger.info(f"Getting HTML for URL: {url}")
    response = requests.get(url)
    text = response.text
    logger.debug(f"HTML: {text}")
    return text

def scrape_product_page(html: str):
    """
    Given the HTML of a product page, scrape it for the necessary information.
    """
    logger.info("Scraping product page")
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img')
    text = bs.find_all('p')
    headings = bs.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    logger.debug(f"Images: {images}")
    logger.debug(f"Text: {text}")
    logger.debug(f"Headings: {headings}")
    return (images, text, headings)

def get_product_data(images, text, headings):
    """
    Given the scraped data, this function will use AI to get the required data points.
    """
    logger.info("Getting product data")
    try:
        prompt = f"""
                Given the following information, return the name, description, and thumbnail URL of the product:

                Headings: {headings}    
                Images: {images}
                Text: {text}

                Using this JSON schema
                    ProductDetail = {{
                        "name": str,
                        "thumbnail_url": str,
                        "description": str,
                    }}
                Return a ProductDetail
                """
        response = chat.send_message(prompt)
        logger.debug(f"Response: {response.text}")
        text = response.text
        data = json.loads(text)
        return (data['name'], data['description'], data['thumbnail_url']) 
    except Exception as e:
        logger.error(f"Error getting product data: {e}")
        raise e

def get_category_ids(product_data: tuple):
    logger.info("Getting category IDs")
    name, description, thumbnail_url = product_data
    categories = get_categories()
    try:
        prompt = f"""
                Given the following product data:
                    Name: {name}
                    Description: {description}
                    Thumbnail URL: {thumbnail_url}
                    Available categories: {categories}

                Return a list of current category ids that apply. Feel free to make new ones by returning a list of strings.

                Using this JSON schema
                    {{
                        "category_ids": list[int],
                        "create": list[str]
                    }}
                Return a list[int] of category IDs that apply to this product.
                """
        response = chat.send_message(prompt)
        logger.debug(f"Response: {response.text}")
        text = response.text
        data = json.loads(text)

        new_categories = data['create']
        created = []
        for new_category in new_categories:
            category = create_category(new_category)
            created.append(category[0])


        for category_id in created:
            categories.append(category_id)

        categories = data['category_ids']
        return data['category_ids']
    except Exception as e:
        logger.error(f"Error getting category IDs: {e}")
        raise e


