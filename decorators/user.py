from flask import redirect, url_for, session, request
from functools import wraps
from database import user_not_in_room


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print('login_required')
        if session.get("logged_in") is not True:
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def user_in_room(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        user = session.get('current_user')
        room = kwargs['room_id']
        print('user_in_room', user, room)
        # Dodaj: ce user ni v roomu, ga redirectaj na dashboard
        if user_not_in_room(room, user):
            return redirect(url_for('index'))
        print('done')

        return f(*args, **kwargs)

    return decorated_function
