import requests

class WeatherForecastTool:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenWeatherMap API key is missing. Please provide a valid API key.")
        
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, place: str):
        """Get current weather of a place"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": place,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {"error": f"API error: {response.status_code}"}
        except Exception as e:
            print(f"[ERROR] Failed to get current weather for '{place}': {e}")
            return {"error": str(e)}

    def get_forecast_weather(self, place: str):
        """Get weather forecast of a place"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": place,
                "appid": self.api_key,
                "cnt": 10,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {"error": f"API error: {response.status_code}"}
        except Exception as e:
            print(f"[ERROR] Failed to get forecast weather for '{place}': {e}")
            return {"error": str(e)}
