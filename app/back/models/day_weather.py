import datetime as dt

class Weather(object):
	def __init__(self, night_temp: float, day_temp: float, humidity: float, date, day_of_week: str, summary: str):
		self.night_temp = night_temp 
		self.day_temp = day_temp 
		self.humidity = humidity
		self.date = date
		self.day_of_week = day_of_week
		self.summary = summary
	
	def to_dict(self):
		return {  'date': self.date, 'day_of_week': self.day_of_week, 'night_temp': self.night_temp, 'day_temp': self.day_temp, 'humidity': self.humidity, 'summary': self.summary }
