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

def validate_available_seats():
    restaurant_data = fetch_restaurant_data()
    for av_seats in restaurant_data["results"]:
        if av_seats["available_seats"] > 0:
            print(f"Available seats: {av_seats['available_seats']}")
            return send_sms()
        else:
            print("There are no seats available")
    return None

def send_sms():
    try:
        url = "http://hackathons.masterschool.com:3030/sms/send" 
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "phoneNumber": "+491753571249",
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

validate_available_seats()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
