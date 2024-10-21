from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send

from users import *
from topics import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SENHAULTRASECRETMAXFROQROIEJQO'
socketio = SocketIO(app)



users_connected = []

dashboard_data_for_user_sample = [
    {'title': 'topic 1', 'users': ['ana', 'bob']},
    {'title': 'topic 2', 'users': ['bob', 'caca']}
]

def get_opposing_users_for_topic(target_user, topic_ans):
    opposing_users = []
    if topic_ans['value'] == None:
        return opposing_users
    for user in users:
        if user['id'] == target_user['id']:
            continue
        if 'answers' not in user:
            continue
        for ans in user['answers']:
            if ans['id'] == topic_ans['id']:
                if ans['value'] != None and ans['value'] != topic_ans['value']:
                    opposing_users.append(user['nickname'])
                break
    return opposing_users

def get_opposing_users_by_topic(user):
    opposing_users_by_topic = []
    if ('answers' not in user) or (user['answers'] == None):
        return opposing_users_by_topic
    for topic_ans in user['answers']:
        topic = find_topic(topic_ans['id'])
        if topic == None:
            continue
        opposing_users = get_opposing_users_for_topic(user, topic_ans)
        opposing_users_by_topic.append({'id': topic['id'], 'title': topic['title'], 'users': opposing_users})
    return opposing_users_by_topic

def test():
    add_user('luan')
    user_answers = []
    user_answers.append({'id': 1, 'value': 'YES'})
    user_answers.append({'id': 2, 'value': 'YES'})
    user_answers.append({'id': 3, 'value': 'YES'})
    update_user_quiz('luan', user_answers)

    user = find_user('luan')
    opposing_users = get_opposing_users_by_topic(user)
    print(opposing_users)

def connect_user(nickname):
    global users_connected
    for user in users_connected:
        if user == nickname:
            return
    users_connected.append(nickname)
    join_room(nickname)

def disconnect_user(nickname):
    global users_connected
    users_connected.remove(nickname)
    leave_room(nickname)

last_topic = 10
def send_new_topic(nickname):
    global last_topic
    global users_connected
    if not nickname in users_connected:
        return
    title = 'topic ' + str(last_topic)
    topic = {'title': title, 'users': ['xxx', 'yyy']}
    send(topic, to=nickname)


@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    session.clear()

    # send_new_topic('luan')

    # return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        nickname = request.form.get('nickname')

        if not nickname:
            return render_template('login.html', error="Campo Apelido é obrigatório")
        user = find_user(nickname)
        if user == None:
            # return render_template('login.html', error="Usuário não cadastrado")
            add_user(nickname)
            user = find_user(nickname)
            if user == None:
                return render_template('login.html', error="Usuário não cadastrado")
        
        session['nickname'] = nickname

        if user['has_quiz']:
            return redirect(url_for('dashboard'))
        return redirect(url_for('quiz'))

    return render_template('login.html')


@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    nickname = session.get('nickname', None)
    if not nickname:
        return redirect(url_for('login'))
    user = find_user(nickname).copy() # so we don't update inplace to emulate a real db

    if user['has_quiz']:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user_answers = []
        for topic in topics:
            title = topic['title']
            answer = request.form.get(title, None)
            user_answers.append({'id': topic['id'], 'value': answer})
        update_user_quiz(nickname, user_answers)
        return redirect(url_for('dashboard'))
    
    return render_template('quiz.html', topics=topics)


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    global dashboard_data_for_user_sample

    nickname = session['nickname']
    user = find_user(nickname).copy() # so we don't update inplace to emulate a real db
    print_user(user)
    
    opposing_users = get_opposing_users_by_topic(user)

    return render_template('dashboard.html', nickname=nickname, dashboard_data=opposing_users)


@app.route('/room')
def room():
    room = 'teste_room'
    nickname = session['nickname']

    session['room'] = room

    return render_template('room.html', room=room, user=nickname)



@socketio.on('connect')
def handle_connect():
    nickname = session.get('nickname', None)
    room = session.get('room', None)

    if nickname is None or room is None:
        return

    print(f'User {nickname} has connected')
    # connect_user(nickname)
    join_room(room)
    send({
        "sender": "",
        "message": f"{nickname} has entered the chat"
    }, to=room)


@socketio.on('disconnect')
def handle_connect():
    nickname = session.get('nickname', None)
    room = session.get('room', None)

    if nickname is None or room is None:
        return

    print(f'User {nickname} has DISCONECTED')
    # disconnect_user(nickname)
    leave_room(room)
    send({
        "message": f"{nickname} has left the chat",
        "sender": ""
    }, to=room)


@socketio.on('message')
def handle_message(payload):
    nickname = session.get('nickname', None)
    room = session.get('room', None)

    if nickname is None or room is None:
        return

    # if room not in rooms:
    #     return

    message = {
        "sender": nickname,
        "message": payload["message"]
    }
    send(message, to=room)
    # rooms[room]["messages"].append(message)


if __name__ == '__main__':
    # test()
    socketio.run(app, host='0.0.0.0', debug=True)