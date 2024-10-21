
users = [
    {'id': 1, 'nickname': 'a', 'has_quiz': False},
    {'id': 2, 'nickname': 'b', 'has_quiz': True, 'answers': [
        {'id': 1, 'value': 'YES'},
        {'id': 2, 'value': 'NO'},
        {'id': 3, 'value': None}
    ]}
]
last_user_id = 2

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