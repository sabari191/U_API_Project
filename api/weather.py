import requests
from config import Config

class WeatherService:
    def __init__(self):
        self.base_url = Config.OPENWEATHERMAP_BASE_URL
        self.api_key = Config.OPENWEATHERMAP_API_KEY

    def get_weather(self, city: str) -> dict:
        try:
            response = requests.get(
                f"{self.base_url}/weather",
                params={"q": city, "appid": self.api_key, "units": "metric"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}