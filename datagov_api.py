import requests
import time
import logging
from typing import Optional, Literal, Dict, Any, List

logging.basicConfig(
    filename='api_call.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

CatalogueItem = Literal["fuelprice"]

def _fetch_data(
    item_id: CatalogueItem,
    limit: Optional[int] = None,
    start_date: Optional[str] = None,  # expected format: YYYY-MM-DD
    end_date: Optional[str] = None,
    date_column: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    
    base_url = 'http://api.data.gov.my/data-catalogue'
    params: Dict[str, Any] = {'id': item_id}

    if limit is not None:
        params['limit'] = limit
    if start_date is not None:
        params['date_start'] = f"{start_date}@{date_column}" 
    if end_date is not None:
        params['date_end'] = f"{end_date}@{date_column}"

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logging.info(
            "Data fetched successfully: item_id=%s, limit=%s, start_date=%s, end_date=%s",
            item_id, limit, start_date, end_date
        )
        return data

    except requests.exceptions.HTTPError as err:
        logging.error("HTTP error occurred: %s", err)
    except requests.exceptions.ConnectionError as err:
        logging.error("Connection error occurred: %s", err)
    except requests.exceptions.Timeout as err:
        logging.error("Timeout error occurred: %s", err)
    except requests.exceptions.RequestException as err:
        logging.error("An error occurred: %s", err)

    return None

def fetch_fuel_price(limit: Optional[int] = None, 
                     start_date: Optional[str] = None, 
                     end_date: Optional[str] = None, 
                     date_column: Optional[str] = None,
                     retry: int = 3) -> Optional[List[Dict[str, Any]]]:
    for _ in range(retry):
        data = _fetch_data(item_id='fuelprice', limit=limit, start_date=start_date, end_date=end_date, date_column=date_column)

        if data is not None:
            return data
        
        else:
            time.sleep(0.5)
            continue

    return None