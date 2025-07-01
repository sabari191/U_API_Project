import os

class Config:
    OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY', 'e200c72831ddbb5f765391b6a3b620f4')
    OPENWEATHERMAP_BASE_URL = 'http://api.openweathermap.org/data/2.5'