import json
import requests

# # Define the latitude, longitude, and radius (in meters)
# lat = 52.520008  # Example: Latitude of New York (near Times Square)
# lon = 13.404954  # Example: Longitude of New York (near Times Square)
# radius = 1000  # 1000 meters (1 km)

# # Overpass API URL
# overpass_url = "http://overpass-api.de/api/interpreter"

# # Query to fetch restaurants and bars
# overpass_query = f"""
#     [out:json];
#     (
#       node["amenity"="restaurant"](around:{radius},{lat},{lon});
#       node["amenity"="bar"](around:{radius},{lat},{lon});
#     );
#     out body;
# """

# # Send the request to the Overpass API
# response = requests.get(overpass_url, params={'data': overpass_query})
# data = response.json()
# json_string = json.dumps(data, indent=4)
# print(f"The reuslt of the query response : {(json_string)}")

# # Parse and display the results
# for element in data['elements']:
#     name = element['tags'].get('name', 'Unnamed')
#     amenity = element['tags'].get('amenity', 'Unknown')
#     lat = element.get('lat')
#     lon = element.get('lon')
#     #print(f"{name} - {amenity} at ({lat}, {lon})")

import requests

url = "https://api.foursquare.com/v3/places/search"

params = {"near": "Berlin", "limit": 10, "query": "restaurants"}

headers = {
    "accept": "application/json",
    "Authorization": "fsq3/zLKLY9q1TvI6IHpkIuZ9z+pv3Ry051CDowF20mXaOs=",
}

response = requests.get(url, headers=headers, params=params)

print(response.text)
