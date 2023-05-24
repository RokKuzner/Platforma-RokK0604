from flask import Blueprint, request
import database as db
import device.deviceDB as ddb
import json

device_bp = Blueprint('device',
                      __name__,
                      static_folder='../static',
                      template_folder='../templates')


@device_bp.route("<device_id>/tictactoe/get")
def device_get_tictactoe(device_id):
    device = ddb.get_device_info(device_id)
    if device is None:
        return "Unknown device id", 400
    if device["game_id"] is None:
        return ""
    game = db.get_tictactoe(device["game_id"])
    return {"game": game, "device_info": device}


@device_bp.route("<device_id>/tictactoe/list")
def list_tictactoe(device_id):
    device = ddb.get_device_info(device_id)
    if device is None:
        return "Unknown device id", 400

    games = ddb.list_available_games(device["user"])
    print('Games:', games)
    return {"games": games, "device_info": device}


@device_bp.route("<device_id>/assign/<game_id>")
def assign_to_game(device_id, game_id):
    device_info = ddb.get_device_info(device_id)
    if device_info is None:
        return "Unknown device id", 400

    if not ddb.is_user_in_game(device_info['user'], game_id):
        return "User not in game", 400

    ddb.assign_game_to_device(device_id, game_id)

    return {"game": db.get_tictactoe(game_id)}


@device_bp.route("<device_id>/tictactoe/update", methods=["POST"])
def device_update_tictactoe(device_id):
    device_info = ddb.get_device_info(device_id)

    if device_info is None:
        return "Unknown device id"

    user = device_info["user"]
    if device_info["game_id"] is None:
        return "Device not in game"

    game = db.get_tictactoe(device_info["game_id"])
    new_state = json.loads(request.data)['state']

    if game is None:
        return "Game does not exist"

    if new_state is None:
        return "Invalid state"

    if user != game['next_player'] or game['ended']:
        return f"Unauthorised {user} != {game['next_player']}"

    sprememba = False
    for i in range(3):
        for j in range(3):
            nov_znak = new_state[i][j]
            star_znak = game["state"][i][j]

            if nov_znak != star_znak:
                if sprememba or star_znak != "#":
                    return "Bad request"
                sprememba = True

    if sprememba is False:
        return "No changes"

    game['state'] = new_state

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
    db.update_tictactoe_state(device_info['game_id'], game['state'],
                              next_player)
    print("update state")

    game['next_player'] = next_player

    if winner is not None:
        winner_player = game["player_x"] if winner == "X" else game["player_o"]
        game['winner'] = winner_player
        db.update_tictactoe_winner(device_info['game_id'], winner_player)

    return {"game": game}
