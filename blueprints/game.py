from flask import Blueprint, request, redirect, render_template, url_for, session, flash
import database as db
from decorators.user import login_required, user_in_room
import random

game_bp = Blueprint('game',
                    __name__,
                    static_folder='../static',
                    template_folder='../templates')


@game_bp.route("/tictactoe/<game_id>/")
@login_required
def tictactoe(game_id):
    current_user = session["current_user"]
    logged_in = session["logged_in"]
    return render_template("games/tictactoe.html",
                           current_user=current_user,
                           logged_in=logged_in,
                           game_id=game_id)


@game_bp.route("/tictactoe/create/<room_id>")
@login_required
def create_tictactoe(room_id):
    current_user = session["current_user"]

    options = [current_user, ""]
    player_x = random.choice(options)
    options.remove(player_x)
    player_o = random.choice(options)

    db.create_tictactoe(room_id, player_x, player_o)
    return redirect(url_for("room.displayRoom", room_id=room_id))
    #redirect nazaj v room iz katerega


@game_bp.route("/tictactoe/delete/<room_id>")
@login_required
@user_in_room
def delete_all_tictactoes(room_id):
    db.delete_all_tictactoes(room_id)
    return redirect(url_for("room.displayRoom", room_id=room_id))


@game_bp.route("/tictactoe/delete/<room_id>/<game_id>")
@login_required
@user_in_room
def delete_one_tictactoe(room_id, game_id):
    db.delete_one_tictactoe(room_id, game_id)
    return redirect(url_for("room.displayRoom", room_id=room_id))


@game_bp.route("/tictactoe/<game_id>/get")
def get_tictactoe(game_id):
    game = db.get_tictactoe(game_id)
    return game if game is not None else "Game not found"


@game_bp.route("/tictactoe/<room_id>/<game_id>/join")
def join_tictactoe(room_id, game_id):
    current_user = session["current_user"]
    game = db.get_tictactoe(game_id)
    player_x = game["player_x"]
    player_o = game["player_o"]

    if player_x == current_user or player_o == current_user:
        return redirect(url_for("game.tictactoe", game_id=game_id))

    if player_x == "":
        db.add_user_to_tictactoe(game_id, "x", current_user)
    elif player_o == "":
        db.add_user_to_tictactoe(game_id, "o", current_user)
    else:
        return "error"
    print("ok join")
    return redirect(url_for("game.tictactoe", game_id=game_id))


@game_bp.route("/tictactoe/<game_id>/update", methods=["POST"])
@login_required
def update_tictactoe(game_id):
    new_state = request.json["state"]
    game = db.get_tictactoe(game_id)

    if game is None:
        return "Game does not exist", 400

    if game['next_player'] != session["current_user"] or game['ended']:
        return "Unauthorised", 400

    # Ali je sprememba stanja legitimna
    # - natanko 1 sprememba
    # - polje, ki se je spremenilo, je moralo biti prej prazno

    # gremo cez vse elemente
    sprememba = False
    for i in range(3):
        for j in range(3):
            nov_znak = new_state[i][j]  # znak v i-ti vrstici in j-tem stolpcu
            star_znak = game["state"][i][j]

            if nov_znak != star_znak:  # zgodila se je sprememba
                if sprememba or star_znak != "#":
                    return "Bad request", 400  # ce smo ze prej videli spremembo, ali pa se je spremenilo prej-neprazno polje, koncamo
                sprememba = True

    if sprememba is False:
        return "No changes", 400

    game['state'] = new_state
    # Ali je kdorkoli zmagal?

    winner = None
    stolpci_sum = ["", "", ""]
    for i in range(3):
        vrstica_sum = ""
        for j in range(3):
            vrstica_sum += game["state"][i][j]
            stolpci_sum[j] += game["state"][i][j]

        # vrstice
        if vrstica_sum == "XXX" or vrstica_sum == "OOO":
            winner = vrstica_sum[0]

    # stolpci
    for sum in stolpci_sum:
        if sum == "XXX" or sum == "OOO":
            winner = sum[0]

    # diagonali
    diag_sum = ["", ""]
    for i in range(3):
        diag_sum[0] += game["state"][i][i]
        diag_sum[1] += game["state"][i][2 - i]

    for sum in diag_sum:
        if sum == "XXX" or sum == "OOO":
            winner = sum[0]

    # V bazo shranimo spremembe

    next_player = game['player_x'] if game['next_player'] == game[
        'player_o'] else game['player_o']
    db.update_tictactoe_state(game_id, game['state'], next_player)
    print("update state")

    game['next_player'] = next_player

    if winner is not None:
        winner_player = game["player_x"] if winner == "X" else game["player_o"]
        game['winner'] = winner_player
        db.update_tictactoe_winner(game_id, winner_player)

    return game, 200
