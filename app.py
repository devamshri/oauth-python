import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import logging
#from model import User
from flask_login import UserMixin
# Python standard libraries
import json
import os
import sqlite3
import PingExp

# Ping
import pandas as pd
import csv

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
#from user import User
from db import get_db

PingExp


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()

load_dotenv()
app = Flask(__name__)
app.secret_key = 'AQ0CFtmUuKO6V-O7PjiPQXLD'
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

@app.route('/pingip')
def pingip():
    return render_template('Table.html')

@app.route('/test')
def test():
    return render_template('Table.htm')


if __name__ == "__main__":
    app.run(port=5555, debug=True)

