import json
import requests
import random
import os
from dotenv import load_dotenv
load_dotenv()
foursquare_key = os.getenv("foursquare_key")


def fetch_restaurant_by_fsq(fsq_id):
    url = f"https://api.foursquare.com/v3/places/{fsq_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"{foursquare_key}",
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return insert_available_seats(data)

def fetch_restaurants_by_city(cityName):
    url = f"https://api.foursquare.com/v3/places/search"
    params = {
        "near": cityName,
        "limit": 50, 
        "query": "restaurant"
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"{foursquare_key}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        restaurants = response.json().get("results", [])
        return restaurants
    else:
        return {"error": "Failed to fetch restaurants", "status_code": response.status_code}



def insert_available_seats(data):
    data["total_seats"] = random.randint(20, 200)
    data["taken_seats"] = random.randint(0, data["total_seats"])
    data["available_seats"] = (
        data["total_seats"] - data["taken_seats"]
    )
    return data

