
topics = [
    {'id': '1', 'title': 'Terra Plana', 'question': 'Você acredita que a terra é plana?'},
    {'id': '2', 'title': 'Ida do Homem à Lua', 'question': 'Você acredita que o homem foi à lua?'},
    {'id': '3', 'title': 'Vacinas', 'question': 'Você acredita que as vacinas fazem mal ao invés de fazer bem?'}
]

def find_topic(id):
    for topic in topics:
        if topic['id'] == id:
            return topic
    return None