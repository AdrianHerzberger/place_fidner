from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)
load_dotenv()
info_bib_key = os.getenv("info_bib_token")

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

@app.route("/team/sendMessage", methods=["POST"])
def send_sms():
    try:
        data = request.json
        phone_number = data.get("phoneNumber")
        message = data.get("message")
        sender = data.get("sender", "place_finder")
        url = "https://api.infobip.com/sms/send"

        smsData = {"to": phone_number, "text": message, "from": sender}

        response = requests.post(url, json=smsData)

        if response.status_code == 200:
            return jsonify({"status": "Message sent successfully"}), 200
        else:
            return (
                jsonify(
                    {
                        "error": "Failed to send SMS",
                        "status_code": response.status_code,
                        "response": response.json(),
                    }
                ),
                response.status_code,
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)