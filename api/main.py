from flask import Flask, jsonify, request
from weather import WeatherService

app = Flask(__name__)
weather_service = WeatherService()

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        data = weather_service.get_weather(city)
        
        # Check for API error response
        if "error" in data or data.get("cod") != 200:
            error_msg = data.get("message", "Weather data unavailable")
            return jsonify({"error": error_msg}), 500
        
        # Successful response
        return jsonify({
            "city": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "description": data.get("weather", [{}])[0].get("description")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)