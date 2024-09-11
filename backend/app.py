from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
import json
import requests
from querys import fetch_restaurant_data
from sms_service import send_booking_verification, send_registry_verification

app = Flask(__name__)
CORS(app)


@app.route("/team/getMessages/<teamName>", methods=["GET", "POST"])
def get_messages(teamName):
    try:
        team_name_encoded = teamName.replace(" ", "%20")
        url = f"http://hackathons.masterschool.com:3030/team/getMessages/{team_name_encoded}"
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Received data: {response.json()}")
            return jsonify(response.json())
        else:
            return (
                jsonify(
                    {
                        "error": "Failed to fetch messages",
                        "status_code": response.status_code,
                    }
                ),
                response.status_code,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(
    "/register/phone_number/<phoneNumber>/city/<cityName>", methods=["GET", "POST"]
)
def register_number(phoneNumber, cityName):
    try:
        register_user = {
            "phone_number": phoneNumber,
            "city_name": cityName,
        }

        response_status_code = 200

        if response_status_code == 200:
            response = {
                "status": "success",
                "message": "User registered successfully",
                "data": register_user,
            }
            phone_number = register_user["phone_number"]
            city_name = register_user["city_name"]
            register_phone(phone_number)
            send_registry_verification(phone_number)
            return jsonify(response), 200
        else:
            return "Failed to register a user!", 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(
    "/book/phone_number/<phoneNumber>/<accept>/fsq_id/<fsq_id>", methods=["GET", "POST"]
)
def book(phoneNumber, accept, fsq_id):
    try:
        if accept.lower() not in ["true", "false"]:
            return "'accept' parameter must be either 'true' or 'false'.", 400


        if accept.lower() == "true":
            validate_restaurant_data(phoneNumber, accept, fsq_id)
            return f"Booking confirmed for phone number: {phoneNumber}"
        return jsonify({
                "message": "No seats available or booking not confirmed.",
                "prompt_new_selection": True
            }), 400
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


def register_phone(phone_number):
    try:
        url = "http://hackathons.masterschool.com:3030/team/registerNumber"
        headers = {"Content-Type": "application/json"}
        data = {"phoneNumber": phone_number, "teamName": "TeamPlaceFinder"}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print(
                f"Phone number registerd successfully! Status code : {response.status_code}"
            )
            send_registry_verfication(phone_number)
            return response.json()
        else:
            print(
                f"Failed to register phone number. Status code : {response.status_code}"
            )
            return {
                "error": "Failed to register phone number",
                "status_code": response.status_code,
                "response": response.text,
            }

    except Exception as e:
        return {"error": str(e)}, 500


def validate_restaurant_data(phone_number, accept, fsq_id):
    try:
        restaurant_data = fetch_restaurant_data(fsq_id)
        if "available_seats" not in restaurant_data:
            return jsonify({"error": "No available seats data found.", "prompt_new_selection": True}), 400
        restaurant_name = restaurant_data.get("name")
        available_seats = restaurant_data.get("available_seats", 0)
        if available_seats > 0 and accept.lower() == "true":
            get_latitude_longitude(fsq_id)
            send_booking_verification(phone_number, restaurant_name, available_seats)
            return (
                f"Seats available. Booking confirmed for phone number: {phone_number}"
            )
        else:
            return {"message": f"No seats available or booking not confirmed for phone number: {phone_number}", "prompt_new_selection": True}, 400
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": str(e)}, 500


def get_latitude_longitude(fsq_id):
    try:
        restaurant_data = fetch_restaurant_data(fsq_id)
        if not restaurant_data or "geocodes" not in restaurant_data:
            print(f"Failed to retrieve geocodes for fsq_id: {fsq_id}")
            return {"error": "No geocodes found for the restaurant"}, 400

        geo_data = restaurant_data["geocodes"]["main"]
        latitude = geo_data.get("latitude")
        longitude = geo_data.get("longitude")

        if latitude and longitude:
            response = requests.post("http://127.0.0.1:5002/post_geodata", json={
                "latitude": latitude,
                "longitude": longitude,
                "fsq_id": fsq_id
            })
            print(f"GeoData post response: {response.json()}")
            return response.json(), response.status_code
        else:
            print(f"Incomplete geo data for fsq_id: {fsq_id}")
            return {"error": "Incomplete geo data"}, 400
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": str(e)}, 500
    
    
@app.route("/post_geodata", methods=["POST"])
def post_geodata():
    try:
        geo_data = request.json  

        if not geo_data:
            return jsonify({"error": "No data provided"}), 400

        latitude = geo_data.get("latitude")
        longitude = geo_data.get("longitude")
        fsq_id = geo_data.get("fsq_id")

        if not latitude or not longitude or not fsq_id:
            return jsonify({"error": "Incomplete geo data"}), 400

        print(f"Received GeoData: Latitude: {latitude}, Longitude: {longitude}, FSQ ID: {fsq_id}")
        return jsonify({"status": "success", "data": geo_data}), 200
    except Exception as e:
        print(f"Error processing geodata: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
