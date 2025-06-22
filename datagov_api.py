import logging.config
import requests
import json
import time
import logging
from typing import Optional, Literal, Dict, Any, List

logging.basicConfig(
    filename='api_call.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

CatalogueItem = Literal["fuelprice"]

#TODO: add start and end date optional parameter
def _fetch_data(item_id: CatalogueItem, limit: Optional[int] = None) -> Optional[List[Dict[str, Any]]]:
    base_url = 'http://api.data.gov.my/data-catalogue'
    request_params = {
        'id': item_id,
        **({"limit": limit} if limit is not None else {})
    }

    try:
        response = requests.get(base_url, params=request_params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        logging.info("Data fetch successfully, item id: %s", item_id)
        return data
        
    except requests.exceptions.HTTPError as err:
        logging.error("HTTP error occurred: %s", err)

    except requests.exceptions.ConnectionError as err:
        logging.error("Connection error occurred: %s", err)

    except requests.exceptions.Timeout as err:
        logging.error("Timeout error occurred: %s", err)

    except requests.exceptions.RequestException as err:
        logging.error("An error occurred: %s", err)

def fetch_fuel_price(limit: Optional[int] = None, retry: int = 3) -> Optional[List[Dict[str, Any]]]:
    for _ in range(retry):
        data = _fetch_data(item_id='fuelprice', limit=limit)

        if data is not None:
            return data
        
        else:
            time.sleep(0.5)
            continue

    return None