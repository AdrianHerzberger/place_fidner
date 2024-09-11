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
        print(f"Whats is the team name string : {team_name_encoded}")
        url = f"http://hackathons.masterschool.com:3030/team/getMessages/{team_name_encoded}"
        print(f"Constructed URL: {url}")
        
        response = requests.get(url)
        
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
                "message": "User registerd successfully",
                "data": register_user,
            }
            phone_number = register_user["phone_number"]
            register_phone(phone_number)
            return jsonify(response), 200
        else:
            return "Failed to register a user!", 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/book/phone_number/<phoneNumber>/<accept>/fsq_id/<fsq_id>", methods=["GET", "POST"])
def book(phoneNumber, accept, fsq_id):
    try:
        if accept.lower() not in ["true", "false"]:
            return "'accept' parameter must be either 'true' or 'false'.", 400

        if accept.lower() == "true":
            validate_available_seats(phoneNumber, accept, fsq_id)
            print(f"Passes values to {validate_available_seats} function")
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


def validate_available_seats(phone_number, accept, fsq_id):
    try:
        restaurant_data = fetch_restaurant_data(fsq_id)
        print(f"Response from API: {restaurant_data}")
        
        if 'available_seats' not in restaurant_data:
            return "No available seats data found.", 400
        
        available_seats = restaurant_data.get('available_seats', 0)
        if available_seats > 0 and accept.lower() == "true":
            send_sms(phone_number)
            return f"Seats available. Booking confirmed for phone number: {phone_number}"
        else:
            return f"No seats available or booking not confirmed for phone number: {phone_number}"
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


def send_sms(phoneNumber):
    try:
        url = "http://hackathons.masterschool.com:3030/sms/send"
        headers = {"Content-Type": "application/json"}

        data = {
            "phoneNumber": phoneNumber,
            "message": "Do you want to book a table? Answer: Yes or No",
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
