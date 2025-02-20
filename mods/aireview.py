import requests
from mods.news import get_news
from mods.weather import get_weather_weatherapi
import openai

# API Keys (Replace with your own keys)

client = openai.OpenAI(
    api_key="your_groq_api_key", 
    base_url="http://0.0.0.0:1337/v1"
)


# Function to get AI-generated rating
def rate_location(news, weather):
    prompt = f"Based on the following news articles and weather report, provide a safety and livability rating out of 5 stars:\n\nNews:\n{news}\n\nWeather:\n{weather}\n\nRating:"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content  # ✅ Fixed indexing issue

if __name__ == "__main__":
    location = input("Enter location: ")
    news_info = get_news(location)
    news = ""
    i=0
    weather_info = get_weather_weatherapi(location)
    if "error" not in news_info and "Failed" not in weather_info:
        for n in news_info:
            news += n['title']
            i+=1
        rating = rate_location("\n".join(news), weather_info)
        print(f"Safety Rating: {rating}")
    else:
        print("Could not retrieve enough data for rating.")
