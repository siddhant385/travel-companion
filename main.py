from flask import Flask, render_template,jsonify,request
from mods.news import get_news
from mods.weather import get_weather_weatherapi
from mods.aireview import rate_location
from mods.geocode import get_city #gets city name
import openai
app = Flask(__name__)


client = openai.OpenAI(
    api_key="your_groq_api_key", 
    base_url="http://127.0.0.1:1337/v1"
)
last_location = {"latitude": None, "longitude": None}


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/location', methods=['POST'])
def get_location():
    global last_location
    data = request.get_json()
    last_location['latitude'] = data.get('latitude')
    last_location['longitude'] = data.get('longitude')
    
    print(f"Received Location: Latitude {last_location['latitude']}, Longitude {last_location['longitude']}")

    return jsonify({"message": "Location received", "latitude": last_location['latitude'], "longitude": last_location['longitude']})

@app.route('/get_info', methods=['GET'])
def get_relevant_info():
    if last_location["latitude"] is None or last_location["longitude"] is None:
        return jsonify({"message": "No location data available yet."})
    
    
    city = get_city(longitude=last_location['longitude'],latitude=last_location['latitude'])
    print(city)
    news = get_news(city)
    weather = get_weather_weatherapi(city)
    source = weather['source']
    temperature = weather['temperature']
    description = weather['description']
    humidity = weather['humidity']
    wind_speed = weather['wind_speed']
    rate = rate_location(city,weather)
    print(type(get_news(city)))
    print(get_weather_weatherapi(city))
    # Generate some relevant information based on location (example)
    info = {
    "city": city,
    "traffic": news,
    "weather": weather,
    "rate": rate,
    "police_station":f"https://www.google.com/maps/search/police+station/@{last_location['latitude']},{last_location['longitude']},15z",
    "hospital":f"https://www.google.com/maps/search/hospital/@{last_location['latitude']},{last_location['longitude']},15z"
}

    return render_template(
        'travel.html',

        city=city,
        source = source,
        temperature=temperature,
        description=description,
        humidity=humidity,
        wind_speed=wind_speed,
        news=news,
        # rate=rate,
        police_station=f"https://www.google.com/maps/search/police+station/@{last_location['latitude']},{last_location['longitude']},15z",
        hospital=f"https://www.google.com/maps/search/hospital/@{last_location['latitude']},{last_location['longitude']},15z",
        rate = rate_location(news=news,weather=weather)
    )

@app.route('/search', methods=['POST'])
def search():
    city = request.form.get("city")
    print(city)
    news = get_news(city)
    weather = get_weather_weatherapi(city)
    source = weather['source']
    temperature = weather['temperature']
    description = weather['description']
    humidity = weather['humidity']
    wind_speed = weather['wind_speed']
    rate = rate_location(city,weather)
    print(get_news(city))
    # print(get_weather_weatherapi(city))
    # Generate some relevant information based on location (example)
#     info = {
#     "city": city,
#     "traffic": news,
#     "weather": weather,
#     "rate": rate,
#     "police_station":f"https://www.google.com/maps/search/police+station/@{last_location['latitude']},{last_location['longitude']},15z",
#     "hospital":f"https://www.google.com/maps/search/hospital/@{last_location['latitude']},{last_location['longitude']},15z"
# }

    return render_template(
        'travel.html',

        city=city,
        source = source,
        temperature=temperature,
        description=description,
        humidity=humidity,
        wind_speed=wind_speed,
        news=news,
        police_station=f"https://www.google.com/maps/search/police+stationin{city}",
        hospital=f"https://www.google.com/maps/search/hospitalin{city}",
        rate = rate_location(news=news,weather=weather)
    )

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"response": "Please provide a message."})

    # Call OpenAI API
    prompt = f"You are an AI assistant specializing in travel safety and travel locations. Provide concise and accurate safety advice based on the user's location, recent news, crime statistics, and general travel precautions. If location-specific data is unavailable, offer general travel safety tips. Ensure the response is practical and easy to understand with some humor in it also provide funny emojis for user interaction. And if user asks for query other than travel or entirely different from it then politely reply that you can only provide travel related information and the query of user is{user_message}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    print(response)

    

    bot_response = response.choices[0].message.content
    return jsonify({"response": bot_response})


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/terms')
def func_name(foo):
    return render_template('')








if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 
