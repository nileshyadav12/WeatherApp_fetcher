
import requests
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(rf"C:\Users\Deepak\api\.env")

class WeatherAPI:
    def __init__(self):
        # Retrieve the API key securely from environment variable
        self.api_key = os.getenv('API_KEY')

        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")

    def get_coordinates_from_location(self, location):
        """Fetch coordinates from OpenWeatherMap API using location."""
        geocode_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        try:
            response = requests.get(geocode_url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            if 'coord' in data:
                lat = data['coord']['lat']
                lon = data['coord']['lon']
                logging.info(f"Coordinates for {location}: Latitude: {lat}, Longitude: {lon}")
                return lat, lon
            else:
                logging.warning(f"Could not find coordinates for {location}.")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data for {location}: {e}")
            return None

    def get_current_weather_by_coordinates(self, lat, lon):
        """Fetch weather data from OpenWeatherMap API using coordinates."""
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            city = data['name']
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            sunrise = data['sys']['sunrise']
            sunset = data['sys']['sunset']

            logging.info(f"Weather in {city}:")
            logging.info(f"Temperature: {temperature}°C")
            logging.info(f"Weather: {weather_description}")
            logging.info(f"Humidity: {humidity}%")
            logging.info(f"Wind Speed: {wind_speed} m/s")
            logging.info(f"Pressure: {pressure} hPa")
            logging.info(f"Sunrise: {sunrise} Unix Timestamp")
            logging.info(f"Sunset: {sunset} Unix Timestamp")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data for coordinates ({lat}, {lon}): {e}")

class WeatherApp:
    def __init__(self):
        self.weather_api = WeatherAPI()

    def run(self):
        """Main method to handle user input and display weather data."""
        location = input("Enter the city name, area, or pincode: ").strip()

        # Fetch coordinates for the location
        coordinates = self.weather_api.get_coordinates_from_location(location)
        if coordinates:
            lat, lon = coordinates
            # Fetch weather data for the coordinates
            self.weather_api.get_current_weather_by_coordinates(lat, lon)
        else:
            logging.warning("Could not fetch coordinates. Try again with a valid city or pincode.")

if __name__ == "__main__":
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO)

    try:
        app = WeatherApp()
        app.run()
    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")
