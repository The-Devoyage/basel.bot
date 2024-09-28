import logging
from database.category import get_categories

from database.product import insert_product, select_products
from utils.parse import get_category_ids, get_html, get_product_data, scrape_product_page

logger = logging.getLogger(__name__)

def create_product(url: str):
    """
    Provided with the URL of the product, this function
    will handle the creation of the product in the database.
    This will scrape the product page for the necessary
    information and insert it into the database.

    Args:
        url (str): The URL of the product to be created.
    """

    logger.info(f"Creating product for URL: {url}")

    html = get_html(url)

    # Scrape the product page for the necessary information
    (images, text, headings)= scrape_product_page(html)

    # Use AI to get the datapoints we need
    product_data = get_product_data(images, text, headings)
    (name, description, thumbnail_url) = product_data

    category_ids = get_category_ids(product_data)

    # Insert the product into the database
    product = insert_product(name, url, thumbnail_url, description, category_ids)

    logger.info(f"Product created: {product}")

    return product

def get_products(search_terms: list[str]):
    """
    Provided with a list of search terms, this function
    will search the database for products that match
    the search terms.

    Args:
        search_terms (list): A list of search terms. Each item in the list can be a word or phrase. Always
        use at least 10 keywords. Only use A-Z characters, no special characters or numbers.
    """

    logger.info(f"Searching for products with terms: {search_terms}")

    # Get the categories that match the search terms
    categories = get_categories()

    # Get the products that match the search terms
    products = select_products(search_terms, categories)

    return products
