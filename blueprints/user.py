from flask import Blueprint, request, redirect, render_template, url_for, session, flash
import database as db
from decorators.user import login_required

user_bp = Blueprint('user',
                    __name__,
                    static_folder='../static',
                    template_folder='../templates')


@user_bp.route("/registration/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        # function should return True al False
        if db.user_exists(username, email):
            # opzoorilo da user obstaja
            flash("Username or email alreay in use.")

        else:
            db.add_user(username, email, password)
            session["logged_in"] = True
            session["current_user"] = username
            return redirect(url_for("index"))

    return render_template("user/registration.html", hide_title=True)


@user_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if db.validate_user(username, password):
            # Log the user in
            session["logged_in"] = True
            session["current_user"] = username
            return redirect(url_for("index"))

        else:
            flash("Wrong username/password")

    return render_template("/user/login.html", hide_title=True)


@user_bp.route('/logout', methods=["GET"])
@login_required
def logout():
    session["logged_in"] = False
    session["current_user"] = None
    flash("Odjava uspešna.")
    return redirect(url_for("user.login"))
