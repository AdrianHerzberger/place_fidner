import json
import requests
import random
import os
from dotenv import load_dotenv
load_dotenv()
foursquare_key = os.getenv("foursquare_key")


def fetch_restaurant_data():
    url = "https://api.foursquare.com/v3/places/search"
    params = {"near": "Berlin", "limit": 10, "query": "restaurants"}
    headers = {
        "accept": "application/json",
        "Authorization": f"{foursquare_key}",
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return insert_available_seats(data)


def insert_available_seats(data):
    for restaurant in data["results"]:
        restaurant["total_seats"] = random.randint(20, 200)
        restaurant["taken_seats"] = random.randint(0, restaurant["total_seats"])
        restaurant["available_seats"] = (
            restaurant["total_seats"] - restaurant["taken_seats"]
        )

    return data
