import requests
import os

class GeoData:
    def __init__(self, data):
        self.lat = data.get('latitude')
        self.lon = data.get('longitude')
        self.country = data.get('country')
        self.state = data.get('admin1')
        self.name = data.get('name')

    def __repr__(self):
        return (
            f"GeoData(name={self.name}, lat={self.lat}, lon={self.lon}, "
            f"country={self.country}, state={self.state})"
        )

class GeoDataUtil:
    def __init__(self):
        self.base_url = "https://geocoding-api.open-meteo.com/v1/search"

    def fetch_geo_data(self, city_name, country_code=None, limit=1):
        params = {
            'name': city_name,
            'count': limit,
            'language': 'en',
            'format': 'json'
        }
        if country_code:
            params['name'] = f"{city_name},{country_code}"

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json().get('results', [])
        return [GeoData(item) for item in data]

if __name__ == "__main__":
    geo_util = GeoDataUtil()

    city_data = geo_util.fetch_geo_data("Tel Aviv", "IL")

    for item in city_data:
        print(item)

