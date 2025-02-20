from opencage.geocoder import OpenCageGeocode

API_KEY = "70e1fa944a0847d7b8901d039ad72ded"  # Replace with your actual API key
geocoder = OpenCageGeocode(API_KEY)

def get_city(latitude, longitude):
    result = geocoder.reverse_geocode(latitude, longitude)
    if result and len(result) > 0:
        city = result[0].get("components", {}).get("city") or \
               result[0].get("components", {}).get("town") or \
               result[0].get("components", {}).get("village")
        return city if city else "City not found"
    return "Location not found"

# Example usage
latitude = 40.7128
longitude = -74.0060  # New York City

city = get_city(latitude, longitude)
print(f"The city is: {city}")
