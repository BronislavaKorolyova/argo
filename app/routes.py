import logging
import os

from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

from back.weather_service import WeatherService
from back.geo_service import GeoService

geo_service = GeoService()
weather_service = WeatherService()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def register_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def home():
        result = None
        instance_id = os.getenv("APP_INSTANCE", "unknown")
        if request.method == "POST":
            city = request.form.get("city")
            country = request.form.get("country")
            logging.debug(f'{instance_id} Received city: {city}, country: {country}')
            try:
                location = geo_service.get_location(city, country)
                if location:
                    logging.info(f'Location found: {location}')
                    return redirect(url_for("weather", lat=location.lat, lon=location.lon, city_name=location.name, country_code=location.country))
                else:
                    result = "No data found for the given location."
                    logging.warning('No data found for the given location')
            except Exception as e:
                result = f"Error: {e}"
        return render_template("index.html", result=result, instance_id=instance_id)

    @app.route("/weather", methods=["GET"])
    def weather():
        latitude = request.args.get("lat")
        longitude = request.args.get("lon")
        city_name = request.args.get("city_name")
        country_code = request.args.get("country_code")
        logging.debug(f'Query parameters - Latitude: {latitude}, Longitude: {longitude}, City: {city_name}, Country: {country_code}')
        if not latitude or not longitude:
            logging.error('Missing coordinates, redirecting to home page')        
            return redirect(url_for("home"))
        try:
            daily_weather = weather_service.get_weather_data(latitude, longitude, city_name, country_code)
            return render_template("weather.html", daily_weather=daily_weather)
        except Exception as e:
            logging.error(f'Error fetching weather data: {e}', exc_info=True)
            return render_template("weather.html", error=f"Error fetching weather data: {e}")

    @app.route('/history')
    def show_history():
        files = []
        if os.path.exists('history'):
            for f in os.listdir('history'):
                if f.endswith('.json'):
                    files.append(f)
        return render_template('history.html', files=sorted(files))

    @app.route('/download/<path:filename>')
    def download_history_file(filename):
        safe_name = secure_filename(filename)  # prevents path traversal
        history_dir = os.path.abspath('history')

        full_path = os.path.join(history_dir, safe_name)
        if not os.path.isfile(full_path):
            logging.warning(f'File not found: {safe_name}')
            return render_template('error.html', error_message='File not found'), 404
        return send_from_directory(history_dir, safe_name, as_attachment=True)
    
    @app.context_processor
    def inject_bg_color():
    #BG_COLOR='#add8e6'  # hex for light blue, 
    #BG_COLOR='#90ee90'  # hex for light green
        return {'bg_color': os.getenv('BG_COLOR', '#ffffff')}  # default white

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error('An exception occurred', exc_info=True)
        if hasattr(e, 'code') and 400 <= e.code <= 599:
        	logging.warning(f'HTTP error occurred: {e}')
        	return render_template("error.html", error_message=str(e)), e.code

        logging.critical('An unexpected error occurred', exc_info=True)
        return render_template("error.html", error_message="An unexpected error occurred."), 500            

