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

    def get_game_html(self, game_id):
        return env.get_template('Game.html').render(game_id=game_id)

    def handle_login_request(self, usermail=None, password=None):
        result={'errors':[]}
        return json.dumps(result)

    def get_register_html(self):
        return env.get_template('Register.html').render()

    def handle_register_request(self, usermail=None, password=None, username=None):
        result = {'errors':[]}
        return json.dumps(result)

    def get_guest_lobby_html(self):
        return env.get_template('GuestLobby.html').render()
    
    def get_guest_request_phrase_html(self):
        return env.get_template('GuestRequestPhrase.html').render()
    
    def get_guest_game_html(self, gid):
        return env.get_template('GuestGame.html').render(gid=gid)
    
    def get_dummy_game(self, gid):
        result = {}
        result["answer"] = "this is a test phrase"
        result["incorrect_letters"] = ['u','b','c']
        result["incorrect_words"] = ['wronge guess']
        result["correct_letters"] = ['s','i','t','a']
        return json.dumps(result)