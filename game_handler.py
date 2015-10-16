'''
This class is responsible for handling requests
that want to get JSON responses regarding the game state.
'''

import os.path
import json
import requests
import cherrypy
import random
from jinja2 import Environment, FileSystemLoader
from time import sleep

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))


class Game_Handler():
    def __init__(self, db):
        random.seed()
        self.db = db
        self.games_table = db['games']
        self.waiting_gids = list()
        self.next_gid = self.find_next_game_id()
 
    def get_dummy_game(self, gid):
        result = {}
        result["answer"] = "this is a test phrase"
        result["incorrect_letters"] = ['u','b','c']
        result["incorrect_words"] = ['wronge guess']
        result["correct_letters"] = ['s','i','t','a']
        result["guesser_uid"] = 'u1'
        result["creator_uid"] = 'u2'
        result["errors"] = []
        result["result"] = "Success"
        return json.dumps(result)
    
    def post_guess(self, uid, gid, guess):
        gid = int(gid)        

        if(gid not in self.games_table):
            output = {'result':'Error', 'errors':["Game does not exist"]}
            return json.dumps(output, encoding='latin-1')
        
        if(uid != self.games_table[gid]['guesser_uid']):
            output = {'result':'Error', 'errors':["Must be the guessing user to guess"]}
        
        if not guess:
            output = {'result':'Failure', 'message':"Incoming data not valid"}
            return json.dumps(output, encoding='latin-1')

        if uid != self.games_table[gid]['guesser_uid']:
            output = {'result':'Failure', 'message':"Must be the guessing user to guess"}
            return json.dumps(output, encoding='latin-1')

        guess = guess.upper()

        if len(guess) is 1:
            self.guess_letter(gid, guess)

        elif len(guess) > 1:
            self.guess_phrase(gid, guess)

        output ={'result':'Success', 'message': None}

#         return json.dumps(output,encoding='latin-1')
        raise cherrypy.HTTPRedirect('/gameplay/' + str(uid) + '/' + str(gid))

    def guess_phrase(self, gid, phrase):
        gid = int(gid)
        if gid not in self.games_table:
            return json.dumps({'result':'Error', 'errors':["Game does not exist"]})

        game_dict = self.games_table[gid]

        if not phrase in game_dict['incorrect_words']:
            if phrase == game_dict['answer']:
                for letter in phrase:
                    if not letter in game_dict['correct_letters']:
                        game_dict['correct_letters'].append(letter)
            else:
                game_dict['incorrect_words'].append(phrase)

            self.check_win(game_dict, phrase)
    
    def guess_letter(self, gid, letter):
        gid = int(gid)
        game_dict = self.games_table[gid]
        answer = game_dict['answer']
        correct_letters = game_dict['correct_letters']
        incorrect_letters = game_dict['incorrect_letters']

        if not letter in correct_letters and not letter in incorrect_letters:
            if letter in answer:
                game_dict['correct_letters'].append(letter)
            else:
                game_dict['incorrect_letters'].append(letter)

            self.check_win(game_dict, letter)

    def check_win(self, game_dict, guess):
        # Check if the guesser won
        if len(guess) > 1:
            if guess == game_dict['answer']:
                game_dict['win'] = game_dict['guesser_uid']
        else:
            if len(set(game_dict['answer'])) is len(game_dict['correct_letters']):
                game_dict['win'] = game_dict['guesser_uid']

        # Check if the creator won
        guesses_made = len(game_dict['incorrect_letters']) + len(game_dict['incorrect_words'])
        if guesses_made >= 6:
            game_dict['win'] = game_dict['creator_uid']


    def get_game(self, gid):
        gid = int(gid)
        # Active Game
        if gid in self.games_table:
            output = self.games_table[gid]
            output['result'] = 'Success'
            output['errors'] = []

        # Logic Error: No active game with this gid
        else:
            output = {'result': 'Error', 'errors': ['This is not an active game id.']}

        return json.dumps(output, encoding='latin-1')
    
    def get_game_request(self, uid):
        request_state = self.post_game_request(uid)
        waiting = request_state['waiting']
        gid = request_state['gid']

        #if waiting: 
        while(1):
            if gid not in self.games_table:
                sleep(2)    # Wait 2 seconds and check if game exists
            else:
                creator = self.games_table[gid]['creator_uid']
                if creator == uid:
                    raise cherrypy.HTTPRedirect('/phrase/' + str(uid) + '/' + str(gid))
                else:
                    answer = self.games_table[gid]['answer']
                    #if answer == "None": answer = False
                    if not answer:
                        sleep(2)
                        continue
                    else:
                        raise cherrypy.HTTPRedirect('/gameplay/' + str(uid) + '/' + str(gid))
        '''            
        if not waiting:
            while(1):
                if gid not in self.games_table:
                    sleep(2)    # Wait 2 seconds and check if game exists
                else:
                    creator = str(game_resp['creator_uid'])
                    if creator == uid:
                        raise cherrypy.HTTPRedirect('/phrase/' + str(uid) + '/' + str(j['gid']))
                    else:
                        answer = str(game_resp['answer'])
                        if answer == "None": answer = False
                        if not answer:
                            sleep(2)
                            continue
                        else:
                            raise cherrypy.HTTPRedirect('/gameplay/' + str(uid) + '/' + str(j['gid']))
        
        else: return "An error occurred"
        '''

    def post_game_request(self, uid):
        waiting = True # whether or not we need to wait for a second player
        uid = str(uid)

        # If there are players waiting for a game, choose a waiting gid
        if not len(self.waiting_gids) is 0:
            (new_gid, first_uid) = self.waiting_gids[0]

            # Make sure this uid isn't just requesting the same game twice
            if first_uid != uid:
                self.waiting_gids.pop(0)
                (guesser_uid, creator_uid) = self.assign_player_roles(first_uid, uid)
                self.games_table[new_gid] = {'answer': None, 
                                         'incorrect_letters': [], 'incorrect_words': [], 'correct_letters': [], 
                                         'guesser_uid' : guesser_uid, 'creator_uid':creator_uid,
                                         'win': None}
                waiting = False

        # Otherwise, choose a new gid and add it to the list of waiting gids
        else:
            new_gid = self.next_gid
            self.next_gid += 1
            self.waiting_gids.append((new_gid, uid))
            waiting = True

        output = {'gid': new_gid, 'waiting': waiting, 'errors':[]}
        return output #json.dumps(output, encoding='latin-1')

    def post_game_prompt(self, uid, gid, answer=None):
        gid = int(gid)
        if uid != self.games_table[gid]['creator_uid']:
            output = {'result': 'Failure', 'message': "Must be the creating user to create prompt"}
            return json.dumps(output, encoding='latin-1')

        if not answer:
            output = {'result': 'Failure', 'message': 'Incoming data insufficient'}
            return json.dumps(output, encoding='latin-1')

        answer = answer.upper()
        stripped_answer = ''.join(answer.split())  # Answer without whitespace

        if not answer is None:
            if len(stripped_answer) in range(3, 31) and answer.isalpha():
                self.games_table[gid]['answer'] = answer
                output = {'result': 'Success', 'message': 'Your game will begin shortly!'}
            else:
                output = {'result': 'Failure', 'message': 'Your phrase must be between 3 and 30 alphabetical characters.'}
        else:
            output = {'result': 'Failure', 'message': 'Empty answer'}

        if not answer is None:
            if len(stripped_answer) in range(3, 31) and answer.isalpha():
                self.games_table[gid]['answer'] = answer
                output = {'result': 'Success', 'message': 'Your game will begin shortly!'}
            else:
                output = {'result': 'Error', 'message': 'Your phrase must be between 3 and 30 alphabetical characters.'}
        raise cherrypy.HTTPRedirect('/gameplay/' + str(uid) + '/' + str(gid))
        return json.dumps(output, encoding='latin-1')

    def assign_player_roles(self, uid1, uid2):
        if random.randint(0,1) == 0:
            guesser_uid = uid1
            creator_uid = uid2
        else:
            guesser_uid = uid2
            creator_uid = uid1

        return (guesser_uid, creator_uid)

    def find_next_game_id(self):
        if len(self.games_table) is 0:
            return 1
        else:
            return max(self.games_table, key=int) + 1
