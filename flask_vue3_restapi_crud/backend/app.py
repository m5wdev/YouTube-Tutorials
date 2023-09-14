from flask import Flask, jsonify, request
from flask_cors import CORS

import uuid

from data import BOOKS


app = Flask(__name__)
# app.config.from_object(__name__)


CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/books', methods=['GET'])
def all_books():
    return jsonify({'books': BOOKS})


@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book_from_db = {}

    for index, book in enumerate(BOOKS):
        if book_id == book['id']:
            book_from_db = BOOKS[index]
            break

    return jsonify(book_from_db)


@app.route('/books/add', methods=['POST'])
def add_book():
    response_obj = {}

    if request.method == 'POST':
        request_data = request.get_json()
        new_book = {
            'id': uuid.uuid4().hex,
            'title': request_data.get('title'),
            'author': request_data.get('author'),
            'read': request_data.get('read'),
        }

        # BOOKS.append(new_book)
        BOOKS.insert(0, new_book)

        response_obj['message'] = 'New book added!'
        response_obj['book'] = new_book

    return jsonify(response_obj)


@app.route('/books/edit/<book_id>', methods=['PUT'])
def edit_book(book_id):
    if request.method == 'PUT':
        request_data = request.get_json()
        print('request_data', request_data)

        book_from_db = {}

        for index, book in enumerate(BOOKS):
            if book_id == book['id']:
                BOOKS[index] = {
                    'id': request_data.get('id'),
                    'title': request_data.get('title'),
                    'author': request_data.get('author'),
                    'read': request_data.get('read'),
                }
                book_from_db = BOOKS[index]
                break

        print('book_from_db', book_from_db)

    return jsonify({
        'message': 'book updated!',
        'book': book_from_db
    })


@app.route('/books/remove/<int:index>', methods=['DELETE'])
def remove_book(index):
    if request.method == 'DELETE':
        deleted_book = BOOKS[index]
        BOOKS.pop(index)
    return jsonify({
        'message': 'successfully deleted',
        'book': deleted_book
    })


if __name__ == '__main__':
    app.run(debug=True)
