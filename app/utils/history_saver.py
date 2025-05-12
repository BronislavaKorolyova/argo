import os
import json
import unicodedata
from datetime import datetime

HISTORY_DIR = 'history'

def normalize_city_name(city):
    city = unicodedata.normalize('NFKD', city)
    return ''.join(c for c in city if c.isalnum() or c in (' ', '_')).lower().replace(' ', '_')

def save_query_to_history(city, data):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'{normalize_city_name(city)}_{timestamp}.json'
    path = os.path.join(HISTORY_DIR, filename)

    with open(path, 'w') as f:
        json.dump({'city': city, 'timestamp': timestamp, 'data': data}, f, indent=2)

