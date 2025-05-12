
import logging
from utils.geo_util_meteo import GeoDataUtil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeoService:
    def __init__(self):
        self.geo_util = GeoDataUtil()
    
    def get_location(self, city: str, country: str):
        logging.info(f'Retrieving location for city: {city}, country: {country}')
        try:
            data = self.geo_util.fetch_geo_data(city, country)
            logging.debug(f'Retrieved geo data: {data}')
            if isinstance(data, list) and data:
                logging.info(f'Location found: {data[0]}')
                return data[0]
            logging.warning('No location data found for the given city and country')
            return None
        except Exception as e:
            logging.error(f'Error while retrieving location data: {e}', exc_info=True)
            raise

