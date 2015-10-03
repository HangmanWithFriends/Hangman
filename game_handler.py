'''
This class is responsible for handling requests
that want to get JSON responses regarding the game state.
'''

import os.path
import json
import requests
import cherrypy

class Game_Handler():
    def __init__(self):
        self.game_db = dict()
        self.waiting_gids = list()
 
    def get_dummy_game(self, gid):
        result = {}
        result["answer"] = "this is a test phrase"
        result["incorrect_letters"] = ['u','b','c']
        result["incorrect_words"] = ['wronge guess']
        result["correct_letters"] = ['s','i','t','a']
        return json.dumps(result)
    
    def handle_guess(self, game_dict, guess):
        if len(guess) == 1:
            self.guess_letter(game_dict, guess)
        elif len(guess) > 1:
            self.guess_phrase(game_dict, guess)

    def guess_phrase(self, game_dict, phrase):
        if phrase not in self.guessed_phrases:
            if phrase == self.answer_string:
                for letter in self.answer_string:
                    self.correct_letters.add(letter)
            else:
                self.incorrect_phrases.add(phrase)
        #else nothing changes
    
    def guess_letter(self, game_dict, letter):
        if letter not in self.guessed_letters:
            if letter in answer_string:
                self.correct_letters.add(letter)
            else:
                self.incorrect_letters.add(letter)
        #else nothing chnages

    def set_answer(self, game_dict, answer):
    #don't allow answer to be reset, constructs to none
        if game_dict['answer']:
            return -1  #phrase already set 
        if len(answer) > 30 or len(answer) < 3:
            return -2  #phrase illegal length
    
        game_dict['answer'] = answer
        return 0  #good phrase

    def set_guesser_uid(self, game_dict, uid):
        if self.guesser_uid == None:
            game_dict['guesser_uid'] = uid
            return 0
        else:
            return -1

    def set_creator_uid(self, game_dict, uid):
        if game_dict['uid'] == None:
            game_dict['uid'] = uid
            return 0
        return -1
 
    def get_game(self, gid):

        # Active Game
        if gid in self.waiting_gids:
            output = self.game_db[gid]
        # Logic Error: No game with this gid
        else:
            output = {'result': 'Error', 'message': 'No player has requested this game'}

        return json.dumps(output, encoding='latin-1')

    def post_game_request(self):
        # If there are players waiting for a game, choose a waiting gid
        if not len(self.waiting_gids) is 0:
            new_gid = self.waiting_gids[0]
            self.waiting_gids.pop(0)
            self.game_dict[new_gid] = {'answer': None, 'incorrect_letters': None, 'incorrect_words': None, 'correct_letters': None}

        # Otherwise, choose a new gid and add it to the list of waiting gids
        else:
            new_gid = max(self.game_db.keys()) + 1
            self.waiting_gids.append(new_gid)

        output = {'gid': new_gid}
        return json.dumps(output, encoding='latin-1')

    def post_game_answer(self, gid):
        data_in = cherrypy.request.body.read()
        data_json = json.loads(data_in)

        answer = data_json['answer']
        stripped_answer = ''.join(answer.split())  # Answer without whitespace

        if not answer is None:
            if len(stripped_answer) in range(3, 31) and answer.isalpha():
                self.game_db[gid]['answer'] = answer
                output = {'result': 'Success', 'message': 'Your game will begin shortly!'}
            else:
                output = {'result': 'Failure', 'message': 'Your phrase must be between 3 and 35 alphabetical characters.'}
