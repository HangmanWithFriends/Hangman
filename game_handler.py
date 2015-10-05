'''
This class is responsible for handling requests
that want to get JSON responses regarding the game state.
'''

import os.path
import json
import requests

class Game_Handler():
    def __init__(self):
        self.game_dict = {}

    def get_dummy_game(self, gid):
        result = {}
        result["answer"] = "this is a test phrase"
        result["incorrect_letters"] = ['u','b','c']
        result["incorrect_words"] = ['wronge guess']
        result["correct_letters"] = ['s','i','t','a']
        return json.dumps(result)
    
    def post_guess(self, game_dict, guess):
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

    def set_answer(self, gid, answer):
    #don't allow answer to be reset, constructs to none
        if self.game_dict[gid]['answer']:
            return -1  #phrase already set 
        if len(answer) > 30 or len(answer) < 3:
            return -2  #phrase illegal length
    
        self.game_dict[gid]['answer'] = answer
        return 0  #good phrase

    def set_guesser_uid(self, gid, uid):
        if self.game_dict[gid]['guesser_uid'] == None:
            self.game_dict[gid]['guesser_uid'] = uid
            return 0
        else:
            return -1

    def set_creator_uid(self, gid, uid):
        if self.game_dict[gid]['uid'] == None:
            game_dict[gid]['uid'] = uid
            return 0
        return -1
