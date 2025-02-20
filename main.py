from flask import Flask, render_template,jsonify,request
from mods.news import get_news
from mods.weather import get_weather_weatherapi
from mods.aireview import rate_location
from mods.geocode import get_city
app = Flask(__name__)


last_location = {"latitude": None, "longitude": None}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def get_location():
    global last_location
    data = request.get_json()
    last_location['latitude'] = data.get('latitude')
    last_location['longitude'] = data.get('longitude')
    
    print(f"Received Location: Latitude {last_location['latitude']}, Longitude {last_location['longitude']}")

    return jsonify({"message": "Location received", "latitude": last_location['latitude'], "longitude": last_location['longitude']})

@app.route('/get-info', methods=['GET'])
def get_relevant_info():
    if last_location["latitude"] is None or last_location["longitude"] is None:
        return jsonify({"message": "No location data available yet."})
    
    city = get_city(last_location['latitude'],last_location['longitude'])
    news = get_news(city)
    weather = get_weather_weatherapi(city)
    rate = rate_location(city,weather)
    print(type(get_news(city)))
    print(get_weather_weatherapi(city))
    # Generate some relevant information based on location (example)
    info = {
    "city": city,
    "traffic": news,
    "weather": weather,
    "rate": rate
}

    return jsonify(info)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 