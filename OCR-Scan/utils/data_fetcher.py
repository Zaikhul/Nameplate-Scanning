# utils/data_fetcher.py
import requests
from utils.logger import logger

def fetch_data(url: str) -> dict:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error fetching data from URL: {url}. Status code: {response.status_code}")
            return {'error': f"Error fetching data from URL: {url}. Status code: {response.status_code}"}
    except Exception as e:
        logger.error(f"Error fetching data from URL: {url}: {e}")
        return {'error': f"Error fetching data from URL: {url}: {e}"}

def post_record(url: str, field: str, image: bytes) -> dict:
    try:
        files = {'image': ('image.png', image, 'image/png')}
        data = {'field': field}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error posting record to URL: {url}. Status code: {response.status_code}")
            return {'error': f"Error posting record to URL: {url}. Status code: {response.status_code}"}
    except Exception as e:
        logger.error(f"Error posting record to URL: {url}: {e}")
        return {'error': f"Error posting record to URL: {url}: {e}"}
