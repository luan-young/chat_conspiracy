from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SENHAULTRASECRETMAXFROQROIEJQO'
socketio = SocketIO(app)


topics = [
    {'id': 1, 'title': 'Terra Plana', 'question': 'Você acredita que a terra é plana?'},
    {'id': 2, 'title': 'Lua Artificial', 'question': 'Você acredita que a lua não é um satélite natural e na verdade é outra coisa?'},
    {'id': 3, 'title': 'Iluminatis', 'question': 'Você acredita nos Iluminatis?'}
]

users = [
    {'id': 1, 'nickname': 'a', 'has_quiz': False},
    {'id': 2, 'nickname': 'b', 'has_quiz': True, 'answers': [
        {'id': 1, 'value': 'YES'},
        {'id': 2, 'value': 'NO'},
        {'id': 3, 'value': None}
    ]}
]
last_user_id = 2

dashboard_data_for_user_sample = [
    {'title': 'topic 1', 'users': ['ana', 'bob']},
    {'title': 'topic 2', 'users': ['bob', 'caca']}
]


def add_user(nickname):
    global last_user_id
    last_user_id += 1
    users.append({'id': last_user_id, 'nickname': nickname, 'has_quiz': False})

def find_user(nickname):
    for user in users:
        if user['nickname'] == nickname:
            return user
    return None

def update_user_quiz(nickname, answers):
    for user in users:
        if user['nickname'] == nickname:
            user['has_quiz'] = True
            user['answers'] = answers

def print_user(user):
    print(f"User: {user['nickname']}")
    print(f"Has quiz: {user['has_quiz']}")
    for ans in user['answers']:
        print(f"Answer to {ans['id']}: {ans['value']}")


@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    session.clear()

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
    print(dashboard_data_for_user_sample)

    return render_template('dashboard.html', nickname=nickname, dashboard_data=dashboard_data_for_user_sample)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)