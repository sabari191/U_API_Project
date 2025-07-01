import pytest
from api.main import app
from api.weather import WeatherService

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_weather(mocker):
    # Mock at the instance level rather than class level
    mock = mocker.patch.object(WeatherService, 'get_weather', autospec=True)
    return mock

def test_weather_endpoint_success(client, mock_weather):
    # Setup mock return value
    mock_weather.return_value = {
        "name": "London",
        "main": {"temp": 15.0},
        "weather": [{"description": "clear sky"}]
    }
    
    response = client.get('/weather/London')
    assert response.status_code == 200
    assert response.json['city'] == "London"
    assert response.json['temperature'] == 15.0  # Now this will match

def test_weather_endpoint_failure(client, mock_weather):
    mock_weather.return_value = {"error": "API Error"}
    response = client.get('/weather/InvalidCity')
    assert response.status_code == 500
    assert "error" in response.json