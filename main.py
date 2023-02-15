from flask import Flask, render_template, request, url_for, redirect, flash, session
import random
import requests
import database as db

from blueprints.user import user_bp
from blueprints.room import room_bp

app = Flask(__name__)
app.secret_key = "asdiajoidaj332333"

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(room_bp, url_prefix='/room')


@app.route('/')
def index():
    if "logged_in" in session and session["logged_in"]:
        rooms = db.get_rooms_with_username2(session["current_user"])
        rooms_new = []
        for room in rooms:
            name = db.get_room_name_from_id(room[0])
            rooms_new.append([room[0], name])
        return render_template("dashboard.html",
                           logged_in=session["logged_in"] if "logged_in" in session else False,
                           current_user=session["current_user"]  if "current_user" in session else None, rooms=rooms_new)
    else:
        return redirect(url_for("user.login"))
        


app.run(host='0.0.0.0', port=81)