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

        if response.status_code == 200:
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


@app.route("/book/phone_number/<phoneNumber>/<accept>", methods=["GET", "POST"])
def book(phoneNumber, accept):
    try:
        if accept.lower() not in ["true", "false"]:
            return "'accept' parameter must be either 'true' or 'false'.", 400

        if accept.lower() == "true":
            validate_available_seats(phoneNumber, accept)
            return f"Booking confirmed for phone number: {phoneNumber}"
        else:
            return f"Booking canceled for phone number: {phoneNumber}"
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


def register_phone(phone_number):
    print(f"Show phone number : {phone_number}")
    try:
        url = "http://hackathons.masterschool.com:3030//team/registerNumber"
        headers = {"Content-Type": "application/json"}
        data = {"phone_number": phone_number, "teamName": "TeamOne"}
        response = requests.post(url, json=data, headers=headers)

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


def validate_available_seats(phone_number, accept):
    print(f"Parameters passed from book query : {phone_number}, {accept}")
    restaurant_data = fetch_restaurant_data()
    for av_seats in restaurant_data["results"]:
        if av_seats["available_seats"] > 0 and accept == "true":
            print(f"Available seats: {av_seats['available_seats']}")
            send_sms(phone_number)
        else:
            print("There are no seats available")
    return None


def send_sms(phoneNumber):
    try:
        url = "http://hackathons.masterschool.com:3030/sms/send"
        headers = {"Content-Type": "application/json"}

        data = {
            "phoneNumber": phoneNumber,
            "message": "Do you want to book a table? Yes or No",
            "sender": "Place Finder",
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
