import json
import requests
import random
import os
from dotenv import load_dotenv
load_dotenv()
foursquare_key = os.getenv("foursquare_key")


def fetch_restaurant_data(fsq_id):
    url = f"https://api.foursquare.com/v3/places/{fsq_id}"
    #params = {"near": fsq_id, "limit": 10, "query": "restaurants"}
    headers = {
        "accept": "application/json",
        "Authorization": f"{foursquare_key}",
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(f"Restaurant data for {fsq_id}: {data}")
    return insert_available_seats(data)


def insert_available_seats(data):
    data["total_seats"] = random.randint(20, 200)
    data["taken_seats"] = random.randint(0, data["total_seats"])
    data["available_seats"] = (
        data["total_seats"] - data["taken_seats"]
    )
    return data

