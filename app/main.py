from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SENHAULTRASECRETMAXFROQROIEJQO'
socketio = SocketIO(app)

@app.route('/', methods=["GET", "POST"])
def home():
    session.clear()

    return render_template('login.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)