"""
Simple client to debug/test server scripts using requests.

Created by: Tony Held tony.held@gmail.com
Created on: 2021-02-10
Copyright © 2021 Tony Held.  All rights reserved.

Resources and Notes:
1) https://realpython.com/python-requests/
"""
import requests
import webbrowser

from tony_util.dir_diagnostics import values, strip_single_tag


def save_responses(filename, response):
    """Save http response headers and content to a local html file.

    Parameters
    -----------
    filename : str
        Local filename to store web response as html.

    response :
        Response created as a result of a web request.
    """
    with open(filename, 'w') as fid:
        fid.write(f'<hr><b>Response Code & Headers:</b><hr>')
        fid.write(f'Response Return Code: {strip_single_tag(str(response))}<br>')
        fid.write(f'<br>Response Headers:<br>')
        fid.write(f'{"-" * 40}<br>')
        for key, val in response.headers.items():
            fid.write(f"{key}: {val}<br>")
        fid.write(f'<br><hr><b>Response Content:</b><br><hr>')
        fid.write(response.content.decode())


def make_request(page, method, query):
    """
    Save response received from a webserver as an html file.
    Returns response and received json data (if present).

    Parameters
    -----------
    page : str
        url of webpage.

    method : str
        Method of interaction with server.
        Can be ['get', 'post', 'post_json', 'return_json']

    query : dict
        Dictionary of data sent to server

    Returns
    -----------

    """
    json_data = None

    # location and basis of file to store server responses
    fname_base = 'server_responses/results'

    if method == 'get':
        fname = fname_base + '_' + method + '.html'
        response = requests.get(page, params=query)
    elif method == 'post':
        fname = fname_base + '_' + method + '.html'
        response = requests.post(page, data=query)
    elif method == 'post_json':
        fname = fname_base + '_' + method + '.html'
        response = requests.post(page, json=query)
    elif method == 'return_json':
        fname = fname_base + '_' + method + '.html'
        response = requests.post(page, json=query)
        try:
            json_data = response.json()
            print('JSON data received:')
            print(json_data)
        except:
            print('No JSON data received:')
    else:
        raise ValueError('Unknown HTTP request method')

    save_responses(fname, response)
    # webbrowser.open(fname, new=2)

    return response, json_data


if __name__ == '__main__':
    """Test my server on pythonanywhere to see how it responds
    to various http requests with and without parameter data."""

    # Requests that send but do not receive data from server
    methods1 = ['get', 'post', 'post_json']
    query1 = {'first': 'joe', 'second': 'banks'}
    page1 = 'https://ez066144.pythonanywhere.com/parse_request'
    for method1 in methods1:
        make_request(page1, method1, query1)

    # Requests that send and receive json data from server
    methods2 = ['return_json']
    query2 = {'first': 'joe', 'second': 'banks'}
    page2 = 'https://ez066144.pythonanywhere.com/return_json'
    for method2 in methods2:
        make_request(page2, method2, query2)
