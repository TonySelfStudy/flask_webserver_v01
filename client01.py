# Simple client to debug/test server scripts using requests

import requests
import webbrowser
from tony_util.dir_diagnostics import values, strip_single_tag
from json import JSONDecodeError


def save_responses(fname, response):
    with open(fname, 'w') as fid:
        fid.write(f'<hr><b>Response Code & Headers:</b><hr>')
        fid.write(f'Response Return Code: {strip_single_tag(str(response))}<br>')
        fid.write(f'<br>Response Headers:<br>')
        fid.write(f'{"-" * 40}<br>')
        for key, val in response.headers.items():
            fid.write(f"{key}: {val}<br>")
        fid.write(f'<br><hr><b>Response Content:</b><br><hr>')
        fid.write(response.content.decode())

def make_request(page, query):

    fname_base = 'results'

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
            tmp = response.json()
            print('JSON data received:')
            print(tmp)
        except:
            print('No JSON data received:')
    else:
        raise ValueError('Unknown HTTP request method')

    save_responses(fname, response)
    webbrowser.open(fname, new=2)


if __name__ == '__main__':

    # methods1 = []
    methods1 = ['get', 'post', 'post_json']

    query1 = {'first': 'joe', 'second': 'banks'}
    page1 = 'https://ez066144.pythonanywhere.com/parse_request'
    for method in methods1:
        make_request(page1, query1)

    # methods2 = []
    methods2 = ['return_json']

    query2 = {'first': 'joe', 'second': 'banks'}
    page2 = 'https://ez066144.pythonanywhere.com/return_json'
    for method in methods2:
        make_request(page2, query2)
