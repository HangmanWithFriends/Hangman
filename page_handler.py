'''
This class is responsible for sending back HTML with
jinja2. This object is referenced by the CherryPy 
dispatcher function.
'''

import os.path
from jinja2 import Environment, FileSystemLoader
import json
import requests
import string
import cherrypy

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Page_Handler():
    
    def __init__(self):
        self.all_users = {}
        self.next_user = 1
        self.next_guest_user = 1
    
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

    
    def get_guest_lobby_with_uid(self, uid):
        return env.get_template('GuestLobby.html').render(uid=uid);
    
    def get_guest_uid(self):
        userid = "g" + str(self.next_guest_user)
        self.all_users[userid] = {"name" : "guest"}
        self.next_guest_user += 1
        guest_info = {'uid' : userid}
        guest_info['errors'] = []
        return json.dumps(guest_info)
    
    def get_guest_request_phrase_html(self):
        return env.get_template('GuestRequestPhrase.html').render()

    def get_guest_lobby_html(self, uid):
        return env.get_template('GuestLobby.html').render(uid=uid)
    
    
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
        game_state = requests.get('http://localhost:8080/game/'+str(gid))
 
        game_dict = json.loads(game_state.content)
        if (len(game_dict['errors']) != 0):
            return "Sorry, error"
         
        alphabet = list(string.ascii_uppercase)

        list_word_progress = []
        for letter in game_dict['answer']:
            if letter == ' ':
                list_word_progress.append(' ')
            elif letter in game_dict['correct_letters']:
                list_word_progress.append(letter)
            else:
                list_word_progress.append("_")

        word_progress = ''.join(list_word_progress)
        
        num_wrong = len(game_dict['incorrect_letters']) + len(game_dict['incorrect_words'])
        
        img_name = "/img/gallows"+str(num_wrong)+".png"
        
        if(str(uid) == str(game_dict['creator_uid'])):
            return env.get_template('SpectatorGame.html').render(game_dict=game_dict, alphabet=alphabet, word_progress=word_progress, img_name=img_name, gid=gid, uid=uid)

 
        return env.get_template('Game.html').render(game_dict=game_dict, alphabet=alphabet, word_progress=word_progress, img_name=img_name, gid=gid, uid=uid)
    
    def get_wait_html(self, uid, gid):
        return env.get_template('Wait.html').render(uid=uid, gid=gid)
    
