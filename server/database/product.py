import sqlite3
import logging

logger = logging.getLogger(__name__)

def select_products(descriptions: list[str], categories: list[str]):
    """Fetches products from the database based on the descriptions and categories.

    Args:
        descriptions (list): A list of descriptions to search for.
        categories (list): A list of categories to search for by id.
    """

    logger.info("Get Products")

    logger.debug(f"Descriptions: {descriptions}")
    logger.debug(f"Categories: {categories}")

    conn = sqlite3.connect('flickcart.db')
    cursor = conn.cursor()

    try:
        # description_clauses = " OR ".join(["description MATCH ?"] * len(descriptions))
        description_clauses = " OR ".join(descriptions)
        # category_clauses = " OR ".join(["c.name = ?"] * len(categories))

        logger.debug(f"Description Clauses: {description_clauses}")
        # logger.debug(f"Category Clauses: {category_clauses}")

        cursor.execute(f"""
                        SELECT * 
                        FROM product p
                        JOIN product_meta pm ON p.rowid = pm.product_id 
                        WHERE p.description MATCH ?
                        AND pm.status = 1
                        LIMIT 20
                        """, (description_clauses, ))
        products = cursor.fetchall()

        logger.debug(f"Products: {products}")

        conn.close()
        return products
    except Exception as e:
        conn.close()
        raise e

def insert_product(name: str, url: str, thumbnail_url: str, description: str, category_ids: list[int]):
    """Creates a new product in the database.

    Args:
        url (str): The URL of the product.
        thumbnail_url (str): The URL of the thumbnail image.
        description (str): The description of the product.
        category_ids (list): A list of category ids to associate with the product.
    """

    logger.info("Insert Product")

    conn = sqlite3.connect('flickcart.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
                       INSERT INTO product (name, description)
                       VALUES (?, ?) 
                       """, (name, description))
        product_id = cursor.lastrowid

        cursor.execute("""
                       INSERT INTO product_meta(product_id, url, thumbnail_url)
                       VALUES (?, ?, ?)
                       """, (product_id, url, thumbnail_url))

        for category_id in category_ids:
            cursor.execute("""
                           INSERT INTO product_category (product_id, category_id)
                           VALUES (?, ?)
                           """, (product_id, category_id))
        conn.commit()

        product = cursor.execute("""
                                 SELECT * FROM product
                                 WHERE rowid = ?
                                 """, (product_id,)).fetchone()
        conn.close()
        return product
    except Exception as e:
        conn.close()
        raise e

