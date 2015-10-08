'''
This class is responsible for handling requests
that want to get JSON responses regarding the game state.
'''

import os.path
import json
import requests
import cherrypy
import random

class Game_Handler():
    def __init__(self):
        random.seed()
        self.game_db = dict()
        self.waiting_gids = list()
 
    def get_dummy_game(self, gid):
        result = {}
        result["answer"] = "this is a test phrase"
        result["incorrect_letters"] = ['u','b','c']
        result["incorrect_words"] = ['wronge guess']
        result["correct_letters"] = ['s','i','t','a']
        return json.dumps(result)
    
    def post_guess(self, gid):
        data_in = cherrypy.request.body.read()
        data_json = json.loads(data_in)

        guess = data_json['guess']
        if len(guess) == 1:
            self.guess_letter(gid, guess)
        elif len(guess) > 1:
            self.guess_phrase(gid, guess)

        output ={'result':'Success', 'errors':[]}
        return json.dumps(output,encoding='latin-1')

    def guess_phrase(self, gid, phrase):
        game_dict = self.game_db[gid]
        if phrase not in game_dict[guessed_phrases]:
            if phrase == game_dict['answer']:
                for letter in game_dict['correct_letters']:
                    game_dict['correct_letters'].append(letter)
            else:
                game_dict['incorrect_words'].append(phrase)
        #else nothing changes
    
    def guess_letter(self, gid, letter):
        game_dict = self.game_db[gid]
        if letter not in game_dict['correct_letters'] and letter not in game_dict['incorrect_letters']:
            if letter in game_dict['answer']:
                game_dict['correct_letters'].append(letter)
            else:
                game_dict['incorrect_letters'].append(letter)
        #else nothing chnages

    def get_game(self, gid):

        # Active Game
        if gid in self.game_db:
            output = self.game_db[gid]

        # Logic Error: No active game with this gid
        else:
            output = {'result': 'Error', 'message': 'This game was not requested by two players'}

        return json.dumps(output, encoding='latin-1')

    def post_game_request(self, uid):
        # If there are players waiting for a game, choose a waiting gid
        if not len(self.waiting_gids) is 0:
            (new_gid, first_uid) = self.waiting_gids[0]
            self.waiting_gids.pop(0)

            (guesser_uid, creator_uid) = self.assign_player_roles(first_uid, uid)

            self.game_db[new_gid] = {'answer': None, 'incorrect_letters': [], 'incorrect_words': [], 'correct_letters': [], 'guesser_uid' : guesser_uid, 'creator_uid':creator_uid}

            waiting = False
            is_creator = (creator_uid == uid)

        # Otherwise, choose a new gid and add it to the list of waiting gids
        else:
            new_gid = max(self.game_db.keys()) + 1
            self.waiting_gids.append((new_gid, uid))
            waiting = True

        output = {'gid': new_gid, 'waiting': waiting}
        return json.dumps(output, encoding='latin-1')

    def post_game_prompt(self, gid):
        data_in = cherrypy.request.body.read()
        data_json = json.loads(data_in)

        answer = data_json['answer']
        stripped_answer = ''.join(answer.split())  # Answer without whitespace

        if not answer is None:
            if len(stripped_answer) in range(3, 31) and answer.isalpha():
                self.game_db[gid]['answer'] = answer
                output = {'result': 'Success', 'message': 'Your game will begin shortly!'}
            else:
                output = {'result': 'Failure', 'message': 'Your phrase must be between 3 and 30 alphabetical characters.'}
        return json.dumps(output, encoding='latin-1')

    def assign_player_roles(self, uid1, uid2):
        if random.randint(0,1) == 0:
            guesser_uid = uid1
            creator_uid = uid2
        else:
            guesser_uid = uid2
            creator_uid = uid1

