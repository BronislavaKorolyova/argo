class WeekWeather:
	def __init__(self, city, country):
		self.city = city
		self.country = country
		self.days = [] #list of weather
		self.next_id = 1
        
	def add_day(self, date, day_of_week, night_temp, day_temp, humidity, summary):
		from back.models.day_weather import Weather
		self.days.append(Weather(night_temp, day_temp, humidity, date, day_of_week, summary))
	
	def to_dict(self):
		return {'city': self.city, 'country': self.country, 'days': [day.to_dict() for day in self.days] }
