import json
import requests
import random

url = "https://api.foursquare.com/v3/places/search"

params = {"near": "Berlin", "limit": 10, "query": "restaurants"}

headers = {
    "accept": "application/json",
    "Authorization": "fsq3/zLKLY9q1TvI6IHpkIuZ9z+pv3Ry051CDowF20mXaOs=",
}

response = requests.get(url, headers=headers, params=params)

data = response.json()

def insert_available_seats():
  for restaurant in data["results"]:
      restaurant["total_seats"] = random.randint(20, 200)
      restaurant["taken_seats"] = random.randint(0, restaurant["total_seats"])
      restaurant["available_seats"] = restaurant["total_seats"] - restaurant["taken_seats"]
      
  json_data = json.dumps(data, indent=4)


  with open("fouraquremap.json", "w") as outfile:
      outfile.write(json_data)


insert_available_seats()
