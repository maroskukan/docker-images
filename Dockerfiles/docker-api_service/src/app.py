#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
#from types import MethodType
from flask import Flask, jsonify, request, Response, redirect
from flask.helpers import url_for

from book_model import *
from settings import *

# books = [
#     {
#         'name': 'Green Eggs and Ham',
#         'price': 7.99,
#         'isbn': 978039400165
#     },
#     {
#         'name': 'The Cat In The Hat',
#         'price': 6.99,
#         'isbn': 9782371000193
#     }
# ]

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


def valid_patch_request_data(request_data):
    if "name" in request_data or "price" in request_data:
        return True
    else:
        return False


@app.route('/')
def get_root():
    return redirect(url_for('get_books'))


@app.route('/api/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


@app.route('/api/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    if return_value is None:
        invalid_book_object_error_msg = {
            "error": f"Book with ISBN number {isbn} not found."
        }
        response = Response(json.dumps(invalid_book_object_error_msg),
                            status=404,
                            mimetype='application/json')
    else:
        response = Response(json.dumps(return_value),
                                       status=200,
                                       mimetype='application/json')
    return response

@app.route('/api/books', methods=['POST'])
def add_book():    
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        book_to_be_added = Book.get_book(new_book['isbn'])
        if book_to_be_added is not None:
            invalid_book_object_error_msg = {
                "error": "Book with ISBN number is already in database, use PUT or PATCH to update.",
            }
            response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
            return response        
        else:
            Book.add_book(new_book['name'], new_book['price'], new_book['isbn'])
            response = Response("",
                                status=201,
                                mimetype='application/json')
            response.headers['Location'] = f"/api/books/{str(new_book['isbn'])}"
    else:
        invalid_book_object_error_msg = {
            "error": "Invalid book object passwd in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 978039480016"
        }
        response = Response(json.dumps(invalid_book_object_error_msg),
                            status=400,
                            mimetype='application/json')
    return response


@app.route('/api/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    book_to_be_updated = Book.get_book(isbn)
    if book_to_be_updated is None:
        invalid_book_object_error_msg = {
            "error": "Book with ISBN number provided not found, so unable to update.",
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
        return response
    else:    
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
    Book.replace_book(new_book['isbn'], new_book['name'], new_book['price'])
    response = Response("",
                        status=204)
    
    return response


@app.route('/api/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    book_to_be_patched = Book.get_book(isbn)
    if book_to_be_patched is None:
        invalid_book_object_error_msg = {
            "error": "Book with ISBN number provided not found, so unable to patch.",
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
        return response
    else:
        request_data = request.get_json()
        if not valid_patch_request_data(request_data):
            invalid_book_object_error_msg = {
                "error": "Invalid book object passed in request",
                "helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
            }
            response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
            return response

        if "price" in request_data:
            Book.update_book_price(isbn, request_data['price'])

        if "name" in request_data:
            Book.update_book_name(request_data['name'])

        response = Response("", status=204)
        response.headers['Location'] = "/books/" + str(isbn)
        return response


@app.route('/api/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    book_to_be_deleted = Book.get_book(isbn)
    if book_to_be_deleted is None:
        invalid_book_object_error_msg = {
            "error": "Book with ISBN number provided not found, so unable to delete.",
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=404, mimetype='application/json')
        return response
    else:
        Book.delete_book(book_to_be_deleted['isbn'])
        response = Response("", status=204)
        return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)