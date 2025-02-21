import requests
# from geopy.geocoders import Nominatim

# API Key (Replace with your own key)
NEWS_API_KEY = "7911c7cdb7024fa6aa98108541d35a3b"

def get_news(location):
    url = f"https://newsapi.org/v2/everything?q={location}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            return {"error": "No news found for this location"}

        # Define keywords to filter traffic-related news
        traffic_keywords = ["traffic", "road", "highway", "accident", "congestion", "construction", "jam", "blockage","crime"]

        # Filter only traffic-related news
        traffic_news = []
        for article in articles:
            title = article["title"].lower()
            description = (article["description"] or "").lower()
            
            if any(keyword in title or keyword in description for keyword in traffic_keywords):
                traffic_news.append({
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"]
                })

        return traffic_news[:5] if traffic_news else {"error": "No traffic-related news found"}
    
    return {"error": "Failed to fetch news"}

    


if __name__ == "__main__":
    print("")
    # location = input("Enter location: ")
    # news_info = get_news(location)
