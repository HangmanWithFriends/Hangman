'''
This class is responsible for sending back HTML with
jinja2. This object is referenced by the CherryPy 
dispatcher function.
'''

import os.path
from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Page_Handler():
    
    def __init__(self):
        pass
    
    def get_login_html(self):
        return env.get_template('Home.html').render()
    
    def get_lobby_html(self):
        return env.get_template('Lobby.html').render()

    def get_request_phrase_html(self):
        return env.get_template('RequestPhrase.html').render()
    
    def handle_login_request(self, usermail=None, password=None):
        result={'errors':[]}
        return json.dumps(result)
