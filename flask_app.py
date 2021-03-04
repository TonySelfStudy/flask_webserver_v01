"""
Simple Flask app to explore framework.
Created by: Tony Held tony.held@gmail.com
Created on: 2021-02-10
Copyright © 2021 Tony Held.  All rights reserved.

Resources and Notes:
1) https://realpython.com/python-requests/
"""
import logging
import json
from io import StringIO
from datetime import datetime

import os.path

from flask import Flask, request, render_template, jsonify, send_from_directory
import pytz
import pprint

from dir_diagnostics import values, strip_single_tag

pp = pprint.PrettyPrinter(indent=4)
# usage pp.pprint(stuff)

# Set timezone, dateformat and logging
pacific = pytz.timezone('US/Pacific')
datefmt = '%Y/%m/%d %I:%M:%S %p'

logging.basicConfig(filename='flask_server_01.log',
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s| %(message)s',
                    datefmt=datefmt)
logging.info(f'Initiating logging at {datetime.now(pacific)}')

app = Flask(__name__)

@app.route('/')
def hello_world():
    logging.info(f'hello_world() called at {datetime.now(pacific)}')

    txt = 'Hello from Flask hosted by pythonanywhere :)<br>\n'
    txt += 'I was uploaded through github!<br>\n'
    txt += 'My project name is: flask_webserver_v01<br>\n'

    return txt


@app.route('/details')
def details():
    logging.info(f'details called at {datetime.now(pacific)}')

    txt = f"Hello! Your IP is {request.remote_addr} <hr>\n\n"
    txt += f"You are using {request.user_agent} <hr>\n\n"

    txt += "Detailed request information:<br>\n"
    vals = values(request, mode='html', print_=False)
    txt += vals

    return txt


@app.route('/posts', methods=['GET', 'POST'])
def post_handler():

    txt = f"Hello! Your IP is {request.remote_addr} \n"
    txt += f"You are using {request.user_agent} \n"

    txt += "Detailed request information: \n"
    vals = values(request, mode='plain-text', print_=False)
    txt += vals

    return txt

@app.route('/parse_request', methods=['GET', 'POST'])
def parse_request():
    """
    Main point of entry to explore how get, post, and json data are processed.

    Accessing server: https://ez066144.pythonanywhere.com/
    will result in various diagnostic information to be displayed.
    In addition, certain requests and responses will be logged in text file(s).
    App can be directly accessed via web browser, or through client01.py routines.

    Example usage:
    https://ez066144.pythonanywhere.com/parse_request?dog=bebe&breed=rat_terrior
    """
    logging.info(f'parse_request() called at {datetime.now(pacific)}')
    log_time = str(datetime.now(pacific).strftime(datefmt))

    txt = f"<hr>\n{'*'*80}\n<br>\n"
    txt += f"Greetings!<br>\nYour IP http request was received at {log_time} <br>\n"
    txt += f"Your request method was: {request.method} <br>\n"

    txt += f"<hr>\n\nYour url information was:<br>\n"
    txt += f"host: {request.host}<br>\n"
    txt += f"host_url: {request.host_url}<br>\n"
    txt += f"path: {request.path}<br>\n"
    txt += f"full_path: {request.full_path}<br>\n"
    txt += f"url: {request.url}<br>\n"
    txt += f"base_url: {request.base_url}<br>\n"
    txt += f"url_root: {request.url_root}<br>\n"
    txt += f"remote_addr: {request.remote_addr}<br>\n"

    txt += f"request endpoint: {request.endpoint}<br>\n"

    txt += f"<hr>\n\nYour arguments were:<br>\n"
    # txt += f"type(request.args)= {strip_single_tag(type(request.args))}<br>\n"
    # txt += f"{request.args=}<br>\n"

    for key, value in request.args.items():
        txt += f"\t{key}: {value}<br>\n"

    txt += f"<hr>\n\nYour form values were:<br>\n"
    for key, value in request.form.items():
        txt += f"\t{key}: {value}<br>\n"

    if request.is_json:
        txt += "<hr>\n\nYour request contained the following json data:<br>\n"
        for key, value in request.json.items():
            txt += f"\t{key}: {value}<br>\n"
    else:
        txt += "<hr>\n\nRequest did not contain json data<br>\n"

    txt += f"<hr>\n\nYour headers were:<br>\n"
    for h in request.headers:
        txt += f"\t{h}<br>\n"

    txt += f"<hr>\n\nYour cookies were:<br>\n"
    for key, value in request.cookies.items():
        txt += f"\t{key}: {value}<br>\n"

    txt += f"<hr>\n\nYour request object's dictionary contents were:<br>\n"
    # for key, value in request.__dict__.items():
    #     txt += f"\t{key}: {value}<br>\n"

    str_io = StringIO()
    pprint.pprint(request.__dict__, stream=str_io, indent=4,
                  width=200, compact=False, sort_dicts=True)

    txt += "<br>\n<pre>\n" + str_io.getvalue() + "</pre>\n\n"

    with open('incoming_requests.html', 'a') as fid:
        fid.write(txt)

    if request.is_json:
        with open('json_requests.txt', 'a') as fid:
            fid.write(f'JSON data received at: {log_time}\n')
            json.dump(request.json, fid, indent=6)
            fid.write(f'\n')

    return txt

@app.route('/return_json', methods=['GET', 'POST'])
def return_json():
    logging.info(f'return_json() called at {datetime.now(pacific)}')
    if request.is_json:
        dict1 = request.json
        dict1['augmented'] = 'updated in return_json()'
        return jsonify(dict1)
    else:
        return "<hr>\nRequest did not contain json data<br>\n"

# original version rendered templates rather than serving static files
# @app.route('/<file_name>')
# def serve_static(file_name):
#     template_dir = '/home/ez066144/pythonAnywhere/templates'
#     exists = os.path.exists(f'{template_dir}/{file_name}')
#     logging.info(f'serve_static called at {datetime.now(pacific)}')
#     logging.info(f"Static file named {file_name} requested <hr>")
#
#     if exists and file_name.endswith('html'):
#         return render_template(file_name)
#     else:
#         return render_template('file_not_found.html')

@app.route('/<file_name>')
def serve_static(file_name):
    logging.info(f'serve_static called at {datetime.now(pacific)}')
    logging.info(f"Static file named {file_name} requested <hr>")

    static_dir_path = os.path.join(app.root_path, 'static')
    file_path = static_dir_path + "/" + file_name
    exists = os.path.exists(file_path)

    # logging.info(f"{file_path} exists = {exists} <hr>")

    if exists:
        return send_from_directory(static_dir_path, file_name)
    else:
        return send_from_directory(static_dir_path, 'file_not_found.html')


@app.route('/favicon.ico')
def favicon():
    logging.info(f'favicon() called at {datetime.now(pacific)}')
    static_dir_path = os.path.join(app.root_path, 'static')
    file_path = static_dir_path + "/" + 'favicon.ico'

    logging.info(f'{app.root_path=}')
    logging.info(f'{static_dir_path=}')
    logging.info(f'{file_path=}')

    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
