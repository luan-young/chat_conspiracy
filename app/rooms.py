
# room: {'id', 'users', 'messages'}
# users: [user1, user2]
# message: {'sender', 'message'}

last_room_id = 0
rooms = []

def find_room(id):
    for room in rooms:
        if id == room['id']:
            return room
    return None

def add_room(user1, user2):
    global last_room_id
    last_room_id += 1
    rooms.append({'id': str(last_room_id), 'users': [user1, user2], 'messages': []})
    return rooms[-1]
