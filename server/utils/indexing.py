import logging

# from llama_index.core.schema import Document
# from llama_index.readers.database import DatabaseReader

from utils.environment import get_env_var

logger = logging.getLogger(__name__)

# DATABASE_URL = get_env_var("DATABASE_URL")


def get_documents():
    # Initialize DatabaseReader with the SQL database connection details
    # reader = DatabaseReader(
    #     # sql_database="<SQLDatabase Object>",  # Optional: SQLDatabase object
    #     # engine="<SQLAlchemy Engine Object>",  # Optional: SQLAlchemy Engine object
    #     uri=DATABASE_URL,  # Optional: Connection URI
    #     # scheme="<Scheme>",  # Optional: Scheme
    #     # host="<Host>",  # Optional: Host
    #     # port="<Port>",  # Optional: Port
    #     # user="<Username>",  # Optional: Username
    #     # password="<Password>",  # Optional: Password
    #     # dbname="<Database Name>",  # Optional: Database Name
    # )

    # # Load data from the database using a query
    # documents = reader.load_data(
    #     query="SELECT * FROM message;"  # SQL query parameter to filter tables and rows
    # )

    logger.info("GET DOCS")
