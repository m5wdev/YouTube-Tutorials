from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


def now_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d, %H:%M:%S')


rooms = {
    'main': [
        { 'username': 'User', 'message': 'Hi, there! from MAIN room', 'room': 'main', 'date': now_datetime() },
    ],
    'room1': [
        { 'username': 'User', 'message': 'Hi, there! from ROOM1 room', 'room': 'room1', 'date': now_datetime() },
    ],
}


@app.route('/')
def home():
    page_title = 'Home'
    return render_template('pages/home.html', page_title=page_title, rooms=rooms)


@app.route('/create-room', methods=['GET', 'POST'])
def create_new_room():
    page_title = 'Create new chat room'

    if request.method == 'POST':
        room_name = request.form.get('room_name')
        rooms[room_name] = []
        return redirect(url_for('home'))

    return render_template('pages/create-room.html', page_title=page_title)


# @socketio.on('connect')
# def handle_connect():
#     print('Connected!')


@socketio.on('join')
def handle_join(data):
    print('handle_join', data)
    room = data['room']
    join_room(room)

    msg = {'message': f'{now_datetime()}: {data["username"]} has entered the room {room}'}
    emit('status', {**msg}, room=room)

    # emit('previous_messages', rooms[room], broadcast=True) # if add broadcast=True, all messages will appear in all rooms
    emit('previous_messages', rooms[room])


@socketio.on('leave')
def handle_leave(data):
    print('handle_leave', data)
    room = data['room']
    leave_room(room)
    emit('status', {'message': f'{now_datetime()}: {data["username"]} has left room {room}'}, room=room)


@socketio.on('message', namespace='/')
def handle_message(data):
    print('handle_message', data)
    room = data['room']
    data['date'] = now_datetime()
    emit('message', {**data}, room=room)

    # if room not exist, create it
    if room not in rooms:
        rooms[room] = []

    # add messages to rooms
    rooms[room].append(data)


if __name__ == '__main__':
    socketio.run(app, debug=True)
