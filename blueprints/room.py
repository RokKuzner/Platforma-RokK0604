from flask import Blueprint, request, redirect, render_template, url_for, session, flash
import database as db

# tukaj bo vse povezano s sobo
room_bp = Blueprint('room',
                    __name__,
                    static_folder='../static',
                    template_folder='../templates')

@room_bp.route("/<room_id>/")
def displayRoom(room_id):
    # return "Soba št." + room_id
    logged_in = session["logged_in"]
    current_user = session["current_user"]
    users = db.get_users_in_room(room_id)
    messages = db.get_messages(room_id)
    print(messages)
    return render_template("room/room.html",
                           room_id=room_id,
                           logged_in=logged_in,
                           users=users,
                           messages=messages,
                           current_user=current_user
                          )

@room_bp.route("/create/", methods = ["POST"])
def createRoom():
    user = session["current_user"]
    #name = "room name"
    name = request.form["name"]
    room = db.create_room(user, name)
    db.join_room(room, user)
    return redirect(url_for("index"))

@room_bp.route("/join/", methods = ["POST"])
def joinRoom():
    user = session["current_user"]
    room = request.form["room"]
    if db.room_exists(room):
        if db.user_not_in_room(room, user):
            db.join_room(room, user)   
        else:
            flash("User already in this room.")
    else:
        flash("No room with this code.")
    return redirect(url_for("index"))

@room_bp.route("/remove/", methods = ["POST"])

# def removeFromRoom(user):
#     if db.room_exist()
#         if db.user_exisets()
#            if.db_user_not_room_owner()
#             db.remove_user_from_room(roomid, user)


@room_bp.route("/message/", methods = ["POST"])
def sendMessage():
    user = session["current_user"]
    message = request.form["blub"]
    room_code = request.referrer.split("/")[-2]
    print(room_code)
    db.add_message_to_room(user, message, room_code)
    print(message)

    return redirect(
        url_for(
            "room.displayRoom", room_id=room_code
        )
    )
    