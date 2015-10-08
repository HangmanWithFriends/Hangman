'''
This class is responsible for sending back HTML with
jinja2. This object is referenced by the CherryPy 
dispatcher function.
'''

import os.path
from jinja2 import Environment, FileSystemLoader
import json
import requests

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Page_Handler():
    
    def __init__(self):
        pass
    
    def get_login_html(self):
        return env.get_template('Home.html').render()
    
    def get_lobby_html(self, uid):
        return env.get_template('Lobby.html').render(uid=uid)

    def get_request_phrase_html(self, uid, gid):
        return env.get_template('RequestPhrase.html').render(uid=uid, gid=gid)

    def get_game_html(self, uid, gid):
        return env.get_template('Game.html').render(uid=uid, gid=gid)

    def handle_login_request(self, usermail=None, password=None):
        result={'errors':[]}
        return json.dumps(result)

    def get_register_html(self):
        return env.get_template('Register.html').render()

    def handle_register_request(self, usermail=None, password=None, username=None):
        result = {'errors':[]}
        return json.dumps(result)

    def get_guest_lobby_html(self, uid):
        return env.get_template('GuestLobby.html').render(uid=uid)
    
    def get_guest_request_phrase_html(self, uid, gid):
        return env.get_template('GuestRequestPhrase.html').render(uid=uid, gid=gid)
    
    def get_guest_game_html(self, uid, gid):
        return env.get_template('GuestGame.html').render(uid=uid, gid=gid)
    
    def get_gameplay_html(self, uid, gid):
        '''
        This is the function that displays the actual game 
        to the user. What the user sees is dependent on the 
        uid supplied (creator/guesser/invalid user). This is 
        a wrapper function of sorts that uses the API to get 
        the correct game info to display to the user. It will 
        do some backend work and then send that info to a HTML 
        template page. 
        '''
        game_state = requests.get('http://localhost:8080/dummygame/1')
        game_state = json.loads(game_state.content)
        return "Game info:<br>Answer: " + game_state["answer"] + "<br>Incorrect Letters:" + str(game_state["incorrect_letters"]) + "<br>Incorrect Phrases" + \
            str(game_state["incorrect_words"]) + "<br>Correct Letters" + str(game_state["correct_letters"])

    def get_wait_html(self, uid, gid):
        return env.get_template('Wait.html').render(uid=uid, gid=gid)
    
