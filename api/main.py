from flask import Flask, jsonify, request
from weather import WeatherService

app = Flask(__name__)
weather_service = WeatherService()

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    data = weather_service.get_weather(city)
    if "error" in data:
        return jsonify({"error": data["error"]}), 500
    return jsonify({
        "city": data.get("name"),
        "temperature": data.get("main", {}).get("temp"),
        "description": data.get("weather", [{}])[0].get("description")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)