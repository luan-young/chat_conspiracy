
topics = [
    {'id': 1, 'title': 'Terra Plana', 'question': 'Você acredita que a terra é plana?'},
    {'id': 2, 'title': 'Lua Artificial', 'question': 'Você acredita que a lua não é um satélite natural e na verdade é outra coisa?'},
    {'id': 3, 'title': 'Iluminatis', 'question': 'Você acredita nos Iluminatis?'}
]

def find_topic(id):
    for topic in topics:
        if topic['id'] == id:
            return topic
    return None