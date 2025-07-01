import sys
import os
import pytest
from flask import Flask

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import using consistent paths
from api.main import app
from api.weather import WeatherService

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_weather_endpoint_success(client, mocker):
    # Corrected mock path to match actual import
    mocker.patch('api.weather.WeatherService.get_weather', return_value={
        "name": "London",
        "main": {"temp": 28.66},
        "weather": [{"description": "clear sky"}]
    })
    response = client.get('/weather/London')
    assert response.status_code == 200
    assert response.json['city'] == "London"
    assert response.json['temperature'] == 28.66

def test_weather_endpoint_failure(client, mocker):
    # Corrected mock path to match actual import
    mocker.patch('api.weather.WeatherService.get_weather', return_value={"error": "API Error"})
    response = client.get('/weather/InvalidCity')
    assert response.status_code == 500
    assert "error" in response.json

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if exitstatus == 0:
        print("\nAll tests passed successfully! The weather API endpoints are functioning as expected.")