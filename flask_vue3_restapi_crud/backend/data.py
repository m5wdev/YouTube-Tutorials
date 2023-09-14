import uuid


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Fatal Purity: Robespierre and the French Revolution',
        'author': 'Ruth Scurr',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Drag: A British History Volume 23',
        'author': 'Jacob Bloomfield',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'The Schopenhauer Cure',
        'author': 'Irvin Yalom',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Napoleon: A Life',
        'author': 'Andrew Roberts',
        'read': False
    },
]
