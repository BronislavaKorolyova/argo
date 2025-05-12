import logging
import requests
from flask import render_template
from back.models.week_weather import WeekWeather

from utils.weather_code import WEATHER_CODE_DESCRIPTIONS
from utils.week_day import get_day_of_week
from utils.history_saver import save_query_to_history

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherService:
    def get_weather_data(self, latitude: float, longitude: float, city: str, country: str) -> WeekWeather:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "relative_humidity_2m",
            "daily": "temperature_2m_max,temperature_2m_min,weathercode",
            "timezone": "auto"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            weather_data = response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f'Error while making API request: {e}', exc_info=True)
            raise
        except Exception as e:
            logging.critical(f'Unexpected error while fetching weather data: {e}', exc_info=True)
            raise
        
        processed = self._process_weather_data(weather_data, city, country)
        
        try:
            # Convert to dict before saving, if needed
            save_query_to_history(city, processed.to_dict())
        except Exception as e:
            logging.warning(f'Failed to save query history: {e}', exc_info=True)

        
        return processed
        
    def format_date(self, date: str) -> str:
        year, month, day = date.split('-')
        formatted_date = f'{day}/{month}/{year}'
        logging.debug(f'Formatted date: {formatted_date}')
        return formatted_date        
    
    def _process_weather_data(self, weather_data, city: str, country: str) -> WeekWeather:
        logging.info('Processing weather data')
        try:
            daily_dates = weather_data["daily"]["time"]
            daily_min_temp = weather_data["daily"]["temperature_2m_min"]
            daily_max_temp = weather_data["daily"]["temperature_2m_max"]
            daily_weather_codes = weather_data["daily"]["weathercode"]
            
            hourly_humidity = weather_data["hourly"]["relative_humidity_2m"]
            daily_humidity = self._calculate_daily_humidity(hourly_humidity, len(daily_dates))
            
            week_weather = WeekWeather(city, country)
            for i in range(len(daily_dates)):
                weather_summary = WEATHER_CODE_DESCRIPTIONS.get(daily_weather_codes[i], "Unknown")
                formatted_date = self.format_date(daily_dates[i])
                day_of_week = get_day_of_week(daily_dates[i])
                week_weather.add_day(
                    date=formatted_date,
                    day_of_week=day_of_week,
                    night_temp=daily_min_temp[i],
                    day_temp=daily_max_temp[i],
                    humidity=round(daily_humidity[i], 2), 
                    summary=weather_summary
                )
            logging.info('Successfully processed weather data')
            return week_weather
        except KeyError as e:
            logging.error(f'Missing expected key in weather data: {e}', exc_info=True)
            raise
        except Exception as e:
            logging.critical(f'Unexpected error while processing weather data: {e}', exc_info=True)
            raise
        
 
    def _calculate_daily_humidity(self, hourly_humidity, num_days: int):
        try:
            daily_humidity = []
            for i in range(num_days):
                start_index = i * 24
                end_index = start_index + 24
                average_humidity = sum(hourly_humidity[start_index:end_index]) / 24
                daily_humidity.append(average_humidity)
            logging.debug(f'Daily humidity calculated: {daily_humidity}')
            return daily_humidity
        except Exception as e:
            logging.error(f'Error while calculating daily humidity: {e}', exc_info=True)
            raise

