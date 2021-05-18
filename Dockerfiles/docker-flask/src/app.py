#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

@app.route('/')
def hello_world():
    message = "Welcome to Flask Web App!"
    return render_template('index.html',
                            message=message,
                            hostName=os.uname()[1])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)