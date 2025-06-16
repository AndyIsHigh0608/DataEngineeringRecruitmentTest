import requests
import json
import time
from typing import Optional, Literal, Dict, Any, List

CatalogueItem = Literal["fuelprice"]

#TODO: implement retry mechanism and replace print statement with logger
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
        return data
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")

    except requests.exceptions.ConnectionError as err:
        print(f"Connection error occurred: {err}")

    except requests.exceptions.Timeout as err:
        print(f"Timeout error occurred: {err}")

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

def fetch_fuel_price(limit: Optional[int] = None, retry: int = 3) -> Optional[List[Dict[str, Any]]]:
    for _ in range(retry):
        data = _fetch_data(item_id='fuelprice', limit=limit)

        if data is not None:
            return data
        
        else:
            time.sleep(0.5)
            continue

    return None