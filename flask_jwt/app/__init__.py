from flask import Flask, jsonify, request, session, make_response, render_template, redirect, url_for
from functools import wraps
import jwt
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_secret_string'


users = [
    {
        'id': 0,
        'role': 'superuser',
        'name': 'admin'
    },
    {
        'id': 1,
        'role': 'superuser',
        'name': 'second_admin'
    },
    {
        'id': 3,
        'role': 'moderator',
        'name': 'mod'
    },
    {
        'id': 4,
        'role': 'user',
        'name': 'user_one'
    },
    {
        'id': 5,
        'role': 'user',
        'name': 'user_two'
    },
]


def check_jwt_token(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return function(*args, **kwargs)
    return wrapped


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Now you logged in'


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'])
        # return jsonify({'token': token.decode('UTF-8')})
        return redirect(url_for('authorised_access', token=token.decode('UTF-8')))
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Login required"'})


@app.route('/auth')
@check_jwt_token
def authorised_access():
    # return 'You successfully authorised!'
    return jsonify(users)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))