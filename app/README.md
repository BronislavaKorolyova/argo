Weather app
A Flask web application that provides a 7-day weather forecast for any city. The app is fully dockerized for easy deployment.

Features
Search for a city's weather forecast for the next week.
View detailed daily weather data (temperature, humidity).

Technologies Used
Flask – Python web framework
Requests – For calling weather APIs
Docker – Containerization
Jinja – Responsive UI (optional)
OpenMeteo API – Weather data source

Prerequisites
Docker installed

Installation
	Clone the repository:
	git clone https://github.com/yourusername/flask-weather-history.git

	Build and run with Docker:
	docker build -t weather-app .
	docker run -e BG_COLOR='lightgreen' -p 5000:5000 weather-app

Access the app:
	Open http://localhost:5000 in your browser.

License
MIT


30/04/2025 Added feature:
View and download your search history as a JSON file.
Dockerized for simple setup and deployment.

Example JSON History Output



Feel free to fork and contribute!
