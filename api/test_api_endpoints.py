import pytest
from api.main import app
from api.weather import WeatherService

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_weather_service(mocker):
    # Create a mock WeatherService instance
    mock_service = mocker.MagicMock(spec=WeatherService)
    
    # Patch the weather_service used in main.py
    mocker.patch('api.main.weather_service', new=mock_service)
    return mock_service

def test_weather_endpoint_success(client, mock_weather_service):
    # Configure mock return value
    mock_weather_service.get_weather.return_value = {
        "name": "London",
        "main": {"temp": 15.0},
        "weather": [{"description": "clear sky"}],
        "cod": 200
    }
    
    response = client.get('/weather/London')
    
    # Verify response
    assert response.status_code == 200
    assert response.json == {
        "city": "London",
        "temperature": 15.0,
        "description": "clear sky"
    }
    
    # Verify mock was called correctly
    mock_weather_service.get_weather.assert_called_once_with("London")

def test_weather_endpoint_failure(client, mock_weather_service):
    # Configure mock to return error
    mock_weather_service.get_weather.return_value = {
        "cod": 404,
        "message": "city not found"
    }
    
    response = client.get('/weather/InvalidCity')
    
    # Verify error response
    assert response.status_code == 500
    assert "error" in response.json
    assert response.json["error"] == "city not found"
    
    # Verify mock was called correctly
    mock_weather_service.get_weather.assert_called_once_with("InvalidCity")

def test_weather_endpoint_exception(client, mock_weather_service):
    # Configure mock to raise exception
    mock_weather_service.get_weather.side_effect = Exception("API timeout")
    
    response = client.get('/weather/London')
    
    # Verify error response
    assert response.status_code == 500
    assert "error" in response.json
    assert "API timeout" in response.json["error"]