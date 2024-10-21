
# user = {'id', 'nickname', 'has_quiz', 'answers':, 'opposers', 'rooms'}
# answers = [{'topic_id', 'title, 'value'}]
# opposers = [{'topic_id', 'title', 'opposers_data'}]
# opposers_data = [{'nickname', 'room_id'}]
# rooms = [{}]

users = [
    {'id': '1', 'nickname': 'a', 'has_quiz': False, 'answers': [], 'opposers': [], 'rooms': []},
    {'id': '2', 'nickname': 'b', 'has_quiz': True,
        'answers': [
            {'topic_id': '1', 'title': 'Terra Plana', 'value': 'YES'},
            {'topic_id': '2', 'title': 'Lua Artificial', 'value': 'NO'},
            {'topic_id': '3', 'title': 'Iluminatis', 'value': None}
        ],
        'opposers': [], 'rooms': []
    }
]
last_user_id = 2

def create_answer(topic_id, title, value):
    return {'topic_id': topic_id, 'title': title, 'value': value}

def create_opposers(topic_id, title):
    return {'topic_id': topic_id, 'title': title, 'opposers_data': []}

def create_opposer_data(nickname, room_id):
    return {'nickname': nickname, 'room_id': room_id}

def add_user(nickname):
    global last_user_id
    last_user_id += 1
    users.append({'id': str(last_user_id), 'nickname': nickname, 'has_quiz': False,
                  'answers': [], 'opposers': [], 'rooms': []})

def find_user(nickname):
    for user in users:
        if user['nickname'] == nickname:
            return user
    return None

def find_user_opposer_data(user, topic_id, opposer_nick):
    for opposer_topic in user['opposers']:
        if opposer_topic['topic_id'] == topic_id:
            for opposer in opposer_topic['opposers_data']:
                if opposer['nickname'] == opposer_nick:
                    return opposer
    return None

def update_user_quiz(nickname, answers):
    for user in users:
        if user['nickname'] == nickname:
            user['has_quiz'] = True
            user['answers'] = answers
            update_users_opposers(nickname)
            break

def update_users_room(nickname, other_nickname, topic_id, room_id):
    user = find_user(nickname)
    other_user = find_user(other_nickname)
    opposer_data = find_user_opposer_data(user, topic_id, other_nickname)
    other_opposer_data = find_user_opposer_data(other_user, topic_id, nickname)
    opposer_data['room_id'] = room_id
    other_opposer_data['room_id'] = room_id

def update_users_opposers(nickname):
    user = find_user(nickname)
    if user is None:
        return
    for other in users:
        if other['id'] == user['id']:
            continue
        for answer in user['answers']:
            if answer['value'] is None:
                continue
            other_answer = find_answer_from_user(other, answer['topic_id'])
            if other_answer is None or other_answer['value'] is None:
                continue
            if answer['value'] != other_answer['value']:
                add_opposer(user, answer['topic_id'], answer['title'], other['nickname'])
                add_opposer(other, answer['topic_id'], answer['title'], user['nickname'])

def find_answer_from_user(user, topic_id):
    for answer in user['answers']:
        if answer['topic_id'] == topic_id:
            return answer
    return None

def add_opposer(user, topic_id, title, nickname):
    for topic in user['opposers']:
        if topic['topic_id'] == topic_id:
            topic['opposers_data'].append(create_opposer_data(nickname, None))
            return
    new_opposers = create_opposers(topic_id, title)
    new_opposers['opposers_data'].append(create_opposer_data(nickname, None))
    user['opposers'].append(new_opposers)

def print_user(user):
    print(f"User: {user['nickname']}")
    print(f"Has quiz: {user['has_quiz']}")
    for ans in user['answers']:
        print(f"Answer to {ans['topic_id']}: {ans['value']}")