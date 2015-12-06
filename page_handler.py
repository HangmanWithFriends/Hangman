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
import re
from feed_handler import Feed_Handler

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Page_Handler():
    
    def __init__(self, db):
        self.db = db
        self.emails_to_uids = db['emails_to_uids']
        self.users = db['users']
        self.default_image_name = "unknown.png"
        self.images_path = '/img/'
        self.feedhandler = Feed_Handler(self.db)
        
    def get_login_html(self):
        return env.get_template('Home.html').render()
    
    def get_lobby_html(self, uid):
        uid_info = self.get_info_dict_from_uid(uid)
        friends = self.get_friend_info_dicts_from_uid(uid)
        num_requests = len(self.users[uid]['incoming_friend_requests'])
        feed_events = self.feedhandler.get_feed_lines(15)
        event_phrases = []
        for elem in feed_events:
            uid1_info = self.get_info_dict_from_uid(elem[0])
            uid2_info = self.get_info_dict_from_uid(elem[1])
            name1 = uid1_info['username']
            name2 = uid2_info['username']
            image1= uid1_info['profile_image']
            image2= uid2_info['profile_image']
            if elem[2] == 'friendship':
                display_string = (name1 + ' became friends with ' + name2)
                event_phrases.append({'display_string' : display_string, 'image_source' : image1})
            elif elem[2] == 'guesser_wins':
                display_string = (name1 + ' beat ' + name2 + ' by guessing "' + elem[3] + '"')
                event_phrases.append({'display_string' : display_string, 'image_source' : image1})
            elif elem[2] == 'creator_wins':
                display_string = (name2 + ' stumped ' + name1 + ' with "' + elem[3] + '"')
                event_phrases.append({'display_string' : display_string, 'image_source' : image2})
        return env.get_template('Lobby.html').render(uid=uid_info['uid'], display_name=uid_info['username'], avatar=uid_info['profile_image'], friends=friends, num_requests=num_requests, news_feed=event_phrases)

    def get_request_phrase_html(self, uid, gid):
        print 'from page_handler gid is ' + gid
        guesser_uid = self.db['games'][gid]['guesser_uid']

        if guesser_uid != 'ai':
            guesser_name = self.users[guesser_uid]['username']
        else:
            guesser_name = 'the Computer'

        return env.get_template('RequestPhrase.html').render(uid=uid, gid=gid, guesser_name=guesser_name, error=0)

    def get_game_html(self, uid, gid):
        return env.get_template('Game.html').render(uid=uid, gid=gid)

    def get_register_html(self):
        return env.get_template('Register.html').render()

    def get_guest_lobby_with_uid(self, uid):
        display_name = "New Guest " + str(uid)
        return env.get_template('GuestLobby.html').render(uid=uid, display_name = display_name);
    
    def get_guest_request_phrase_html(self):
        return env.get_template('GuestRequestPhrase.html').render(error = 0)

    def get_guest_lobby_html(self, uid):
        uid_info = self.get_info_dict_from_uid(uid) 
        if uid in self.users.keys() and 'g' not in uid:                    
            return env.get_template('Lobby.html').render(uid=uid, display_name=uid_info['username'], avatar=uid_info['profile_image'])   
        return env.get_template('GuestLobby.html').render(uid=uid,display_name=uid_info['username'])
    
    
    def get_guest_game_html(self, uid, gid):
        return env.get_template('GuestGame.html').render(uid=uid, gid=gid)
    
    def get_gameplay_html(self, uid, gid):
        '''
        This is the function that displays the actual game 
        to the user. What the user sees is dependent on the 
        uid supplied (creator/guesser/invalid user). It will 
        do some backend work and then send that info to a HTML 
        template page. 
        '''

        if gid not in self.db['games']:
                return ['This is not an active game id.']

        game_dict = self.db['games'][gid]
        
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
        
        #These would be the users display names
        creator_uid = self.db['games'][gid]['creator_uid']
        guesser_uid = self.db['games'][gid]['guesser_uid']

        if creator_uid != 'ai':
            creator_name = self.db['users'][creator_uid]['username']
        else:
            creator_name = "the Computer"

        if guesser_uid != 'ai':
            guesser_name = self.db['users'][guesser_uid]['username']
        else:
            guesser_name = 'the Computer'
        
        if(str(uid) == str(game_dict['creator_uid'])):
            return env.get_template('SpectatorGame.html').render(game_dict=game_dict, alphabet=alphabet, word_progress=word_progress, img_name=img_name, gid=str(gid), uid=uid, guesser_name = guesser_name, creator_name = creator_name)

 
        return env.get_template('Game.html').render(game_dict=game_dict, alphabet=alphabet, word_progress=word_progress, img_name=img_name, gid=str(gid), uid=uid, guesser_name = guesser_name, creator_name = creator_name)
    
    def get_wait_html(self, uid, gid):
        return env.get_template('Wait.html').render(uid=uid, gid=gid)
    
    def get_settings_html(self, uid):
        uid_info = self.get_info_dict_from_uid(uid)
        return env.get_template('Settings.html').render(uid=uid, display_name=uid_info['username'], avatar=uid_info['profile_image'], email=uid_info['usermail'])

    def handle_friends_management_search_html(self, uid, search_string=None):
#         cl = cherrypy.request.headers['Content-Length']
#         data_json = cherrypy.request.body.read(int(cl))
#         incoming_data = json.loads(data_json)
# 
#         search_string = None
#         if 'search_string' in incoming_data:
#             search_string = incoming_data['search_string']

        return self.get_friends_management_html(uid, search_string)

    def get_friends_management_html(self, uid, search_string=None):
        search_results_info_dicts_list = []
        pending_requests_info_dicts_list = []

        search_result_uids = self.search_for_friends(uid, search_string) 
        pending_request_uids = self.users[uid]['incoming_friend_requests']

        for pending_request_uid in pending_request_uids:
            pending_requests_info_dicts_list.append(self.get_info_dict_from_uid(pending_request_uid))
        
        for search_result_uid in search_result_uids:
            search_results_info_dicts_list.append(self.get_info_dict_from_uid(search_result_uid))

        uid_info = self.get_info_dict_from_uid(uid)
        return env.get_template('ManageFriends.html').render(uid=uid, display_name=uid_info['username'], avatar=uid_info['profile_image'], num_requests = len(pending_requests_info_dicts_list), pending_requests=pending_requests_info_dicts_list, search_results=search_results_info_dicts_list, search_string=search_string)

    def get_friend_info_dicts_from_uid(self, uid):
        if uid not in self.db['users']:
            return []

        friends_uids = self.users[uid]['friends']
        friends_dicts_list = []
        for f_uid in friends_uids:
            friends_dicts_list.append(self.get_info_dict_from_uid(f_uid))

        return friends_dicts_list
    
    def get_info_dict_from_uid(self, uid):
        to_return = {'uid':uid, 'username':self.users[uid]['username'], 'profile_image':self.images_path+self.get_image_name_from_uid(uid)}
        if uid[0] != 'g':
            to_return['usermail'] = self.users[uid]['usermail']
        return to_return

    def get_image_name_from_uid(self, uid):
        image_name = self.default_image_name
        if uid not in self.db['users']:
            return image_name
        
        if self.users[uid]['profile_image'] != None:
            #now ensure image is where it needs to be
            if os.path.isfile('img/'+self.users[uid]['profile_image']):
                image_name = self.users[uid]['profile_image']

        return image_name

    
    def search_for_friends(self, uid, search_string):
        if not search_string:
            return []

        match_uids = []
  
        for k in self.db['users'].keys():
            val = self.db['users'][k]
            usermail = val['usermail']
            if search_string in val['username'].lower(): match_uids.append(k)
            elif usermail:
	        if search_string in val['usermail'].lower(): match_uids.append(k)
            
        return match_uids
