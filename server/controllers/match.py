import logging
from google.generativeai.protos import FunctionCall

from controllers.product import create_product, get_products

logger = logging.getLogger(__name__)

def match_function_call(fn: FunctionCall):
    match fn.name:
        case "get_products":
            logger.info("Function call: get_products")

            try:
                search_terms = fn.args["search_terms"]

                # This works....
                # for arg in search_terms:
                #     logger.info(f"Arg: {arg}")
                #     if not arg:
                #         logger.error("Missing required argument: search_terms")
                #         return []
                

                if not search_terms:
                    logger.error("Missing required argument: search_terms")
                    return []

                return get_products(search_terms)
            except KeyError as e:
                logger.error(f"Missing required argument: {e}")
                return []
        case "create_product":
            logger.info("Function call: create_product")
            try:
                return create_product(**fn.args)
            except Exception as e:
                logger.error(e)
                return []

            

