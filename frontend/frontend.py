
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
app_key = os.getenv("app_key")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)