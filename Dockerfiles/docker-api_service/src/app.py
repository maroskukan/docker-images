#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from types import MethodType
from flask import Flask, jsonify, request, Response, redirect
from flask.helpers import url_for


app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 978039400165
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'isbn': 9782371000193
    }
]

def validBookObject(bookObject):
    if ("name" in bookObject and
        "price" in bookObject and
        "isbn" in bookObject):
        return True
    else:
        return False


def valid_put_request_data(request_data):
    if "name" in request_data and "price" in request_data:
        return True
    else:
        return False


@app.route('/')
def get_root():
    return redirect(url_for('get_books'))


@app.route('/api/books')
def get_books():
    return jsonify({'books': books})


@app.route('/api/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)


@app.route('/api/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("",
                            status=201,
                            mimetype='application/json')
        response.headers['Location'] = "/api/books/" + str(new_book['isbn'])
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passwd in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 978039480016"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg),
                            status=400,
                            mimetype='application/json')
    return response


@app.route('/api/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalid_book_object_error_msg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
        }
        response = Response(json.dumps(invalid_book_object_error_msg),
                                       status=400,
                                       mimetype='application/json')
        return response

    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book['isbn']
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("",
                        status=204)
    
    return response


@app.route('/api/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    update_book = {}
    if ('name' in request_data):
        update_book['name'] = request_data['name']
    if ('price' in request_data):
        update_book['price'] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(update_book)
    response = Response("",
                        status=204)
    response.headers['Location'] = "/api/books/" + str(isbn)

    return response


@app.route('/api/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book['isbn'] == isbn:
            books.pop(i)
            response = Response("",
                                status=204)
            return response
        i += 1
    invalid_book_object_error_msg = {
        "error": "Book with the ISBN number that was not provided, so therefore unable to delete"
    }
    response = Response(json.dumps(invalid_book_object_error_msg),
                        status=404,
                        mimetype='application/json')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)