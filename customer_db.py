import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_customer_id(national_id):
    try:
        df = pd.read_csv("data/customers.csv")
        if national_id in df["national_id"].astype(str).values:
            customer_id = df[df["national_id"].astype(str) == national_id]["customer_id"].iloc[0]
            logger.info(f"Found customer_id {customer_id} for national_id {national_id}")
            return customer_id
        logger.warning(f"No customer found for national_id {national_id}")
        return None
    except Exception as e:
        logger.error(f"Error accessing customer database: {str(e)}")
        return None