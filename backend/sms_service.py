from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
import requests
import json

def send_booking_verification(phoneNumber, restaurant_name, available_seats):
    try:
        url = "http://hackathons.masterschool.com:3030/sms/send"
        headers = {"Content-Type": "application/json"}

        data = {
            "phoneNumber": phoneNumber,
            "message": f"You have booked a table in {restaurant_name}. There are currently {available_seats} seats available!",
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