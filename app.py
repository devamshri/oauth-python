import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import logging
from model import User
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from db import db_init, db

app = Flask(__name__)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)
db = SQLAlchemy()

load_dotenv()
app = Flask(__name__)
#client_id = os.getenv('504060966146-ntucaatnmibslnch5afr4p3qpkhjdrrj.apps.googleusercontent.com')
#client_secret = os.getenv('AQ0CFtmUuKO6V-O7PjiPQXLD')
app.secret_key = 'AQ0CFtmUuKO6V-O7PjiPQXLD'
#print(client_id)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id='504060966146-ntucaatnmibslnch5afr4p3qpkhjdrrj.apps.googleusercontent.com',
    client_secret='AQ0CFtmUuKO6V-O7PjiPQXLD',
    reprompt_consent=True,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

    return render_template('index.j2',
                           google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)

@app.route('/login')
def login():
    return redirect(url_for('google.login'))

if __name__ == "__main__":
    app.run(port=5555, debug=True)
