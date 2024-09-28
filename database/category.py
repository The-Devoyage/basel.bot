import sqlite3
import logging

logger = logging.getLogger(__name__)

def get_categories():
    """Fetches all categories from the database.
    
    Returns:
        All available categories.
    """
    conn = sqlite3.connect('flickcart.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        conn.close()
        return categories
    except Exception as e:
        conn.close()
        raise e

def create_category(name: str):
    """
    Create a new category.

    Args:
        name: The name of the category.
    """

    logger.info(f"Creating category: {name}")
    
    conn = sqlite3.connect('flickcart.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO category (name) VALUES (?)", (name,))
        conn.commit()
        cursor.execute("SELECT * FROM category WHERE name = ?", (name,))
        category = cursor.fetchone()
        logger.debug(f"Category created: {category}")
        conn.close()
        return category
    except Exception as e:
        conn.close()
        raise e
