from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
import json
import requests
from querys import fetch_restaurant_data

app = Flask(__name__)
CORS(app)


@app.route("/team/getMessages/<teamName>", methods=["GET", "POST"])
def get_messages(teamName):
    try:
        team_name_encoded = teamName.replace(" ", "%20")
        url = f"http://hackathons.masterschool.com:3030/team/getMessages/{team_name_encoded}"
        response = requests.get(url)
        
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")


        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")

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

        print(register_user)

        response_status_code = 200

        if response_status_code == 200:
            response = {
                "status": "success",
                "message": "User registered successfully",
                "data": register_user,
            }
            phone_number = register_user["phone_number"]
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
    print(f"The type of phone number : {type(phoneNumber)}")
    try:
        if accept.lower() not in ["true", "false"]:
            return "'accept' parameter must be either 'true' or 'false'.", 400

        if accept.lower() == "true":
            validate_restaurant_data(phoneNumber, accept, fsq_id)
            return f"Booking confirmed for phone number: {phoneNumber}"
        else:
            return f"Booking canceled for phone number: {phoneNumber}"
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


def register_phone(phone_number):
    try:
        url = "http://hackathons.masterschool.com:3030/team/registerNumber"
        headers = {"Content-Type": "application/json"}
        data = {"phoneNumber": phone_number, "teamName": "TeamPlaceFinder"}
        response = requests.post(url, json=data, headers=headers)

        print(f"Show phone number : {response}")
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
            return "No available seats data found.", 400
        restaurant_name = restaurant_data.get("name")
        available_seats = restaurant_data.get("available_seats", 0)
        if available_seats > 0 and accept.lower() == "true":
            get_latitude_longitude(fsq_id)
            send_booking_verification(phone_number, restaurant_name, available_seats)
            return (
                f"Seats available. Booking confirmed for phone number: {phone_number}"
            )
        else:
            return f"No seats available or booking not confirmed for phone number: {phone_number}"
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


def get_latitude_longitude(fsq_id):
    try:
        restaurant_data = fetch_restaurant_data(fsq_id)
        geo_data = restaurant_data["geocodes"]["main"]
        post_geodata(geo_data, fsq_id)
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": str(e)}, 500


def post_geodata(geo_data, fsq_id):
    url = "http://localhost:5002/post_geodata"
    payload = {
        "latitude": geo_data["latitude"],
        "longitude": geo_data["longitude"],
        "fsq_id": fsq_id,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"Data posted successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def send_booking_verification(phoneNumber, restaurant_name, available_seats):
    try:
        url = "http://hackathons.masterschool.com:3030/sms/send"
        headers = {"Content-Type": "application/json"}

        data = {
            "phoneNumber": phoneNumber,
            "message": f"Do you want to book a table in {restaurant_name}? There are currently {available_seats} seats available! Answer: Yes or No",
            "sender": "",
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print(f"SMS sent successfully! Status Code: {response.status_code}")
            return response.json()
        else:
            print(f"Failed to send SMS. Status Code: {response.status_code}")
            return {
                "error": "Failed to send SMS",
                "status_code": response.status_code,
                "response": response.text,
            }

    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return {"error": str(e)}, 500
    

def send_registry_verification(phone_number):
    try:
        url = "http://hackathons.masterschool.com:3030/sms/send"
        headers = {"Content-Type": "application/json"}

        data = {
            "phoneNumber": phone_number,
            "message": f"Phone number +{phone_number} was registerd successfully!",
            "sender": "",
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print(f"SMS sent successfully! Status Code: {response.status_code}")
            return response.json()
        else:
            print(f"Failed to send SMS. Status Code: {response.status_code}")
            return {
                "error": "Failed to send SMS",
                "status_code": response.status_code,
                "response": response.text,
            }

    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
