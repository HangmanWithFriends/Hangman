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
    def __init__(self):
        random.seed()
        self.game_db = dict()
        self.waiting_gids = list()
        self.next_gid = 1
 
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
    
    def post_guess(self, uid, gid):
        data_in = cherrypy.request.body.read()
        data_json = json.loads(data_in)

        if(gid not in self.game_db):
            output = {'result':'Error', 'errors':["Game does not exist"]}
            return json.dumps(output, encoding='latin-1')
        
        if(uid != self.game_db[gid]['guesser_uid']):
            output = {'result':'Error', 'errors':["Must be the guessing user to guess"]}
        
        if not 'guess' in data_json:
            output = {'result':'Failure', 'message':"Incoming data not valid"}
            return json.dumps(output, encoding='latin-1')

        if uid != self.game_db[gid]['guesser_uid']:
            output = {'result':'Failure', 'message':"Must be the guessing user to guess"}
            return json.dumps(output, encoding='latin-1')

        guess = data_json['guess'].upper()

        if len(guess) is 1:
            win = self.guess_letter(gid, guess)

        elif len(guess) > 1:
            win = self.guess_phrase(gid, guess)

        output ={'result':'Success', 'message': None}

        return json.dumps(output,encoding='latin-1')

    def guess_phrase(self, gid, phrase):
        if gid not in self.game_db:
            return json.dumps({'result':'Error', 'errors':["Game does not exist"]})

        game_dict = self.game_db[gid]

        if not phrase in game_dict['guessed_phrases']:
            if phrase == game_dict['answer']:
                for letter in phrase:
                    game_dict['correct_letters'].append(letter)
                return True
            else:
                game_dict['incorrect_words'].append(phrase)
                return False
    
    def guess_letter(self, gid, letter):
        game_dict = self.game_db[gid]
        answer = game_dict['answer']
        correct_letters = game_dict['correct_letters']
        incorrect_letters = game_dict['incorrect_letters']

        if not letter in correct_letters and not letter in incorrect_letters:
            if letter in answer:
                game_dict['correct_letters'].append(letter)

                if len(set(correct_letters.split())) is len(answer):
                    return True
            else:
                game_dict['incorrect_letters'].append(letter)
                return False

    def get_game(self, gid):

        # Active Game
        if str(gid) in self.game_db:
            output = self.game_db[gid]
            output['result'] = 'Success'

        # Logic Error: No active game with this gid
        else:
            output = {'result': 'Error', 'errors': ['This is not an active game id.']}

        return json.dumps(output, encoding='latin-1')
    
    def get_game_request(self, uid):
        request_state = requests.post('http://localhost:8080/game/' + str(uid) + '/request')
        j = json.loads(request_state.content)
        waiting = str(j['waiting'])
        if (waiting == "True"): 
#             return env.get_template('Wait.html').render(uid=uid,gid=str(j['gid']))
            while(1):
                check_game = requests.get('http://localhost:8080/game/' + str(j['gid']))
                game_resp = json.loads(check_game.content)
                if(str(game_resp['result']) == "Error"):
                    sleep(2)    # Wait 2 seconds and check if game exists
                elif(str(game_resp['result']) == "Success"):
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
                    
        if (waiting == "False"):
            check_game = requests.get('http://localhost:8080/game/' + str(j['gid']))
            game_resp = json.loads(check_game.content)
            if(str(game_resp['result']) == "Error"):
                sleep(2)    # Wait 2 seconds and check if game exists
            elif(str(game_resp['result']) == "Success"):
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
                self.game_db[new_gid] = {'answer': None, 
                                         'incorrect_letters': [], 'incorrect_words': [], 'correct_letters': [], 
                                         'guesser_uid' : guesser_uid, 'creator_uid':creator_uid}
                waiting = False

        # Otherwise, choose a new gid and add it to the list of waiting gids
        else:
            new_gid = str(self.next_gid)
            self.next_gid += 1
            self.waiting_gids.append((new_gid, uid))
            waiting = True

        output = {'gid': new_gid, 'waiting': waiting, 'errors':[]}
        return json.dumps(output, encoding='latin-1')

    def post_game_prompt(self, uid, gid):
        data_in = cherrypy.request.body.read()
        data_json = json.loads(data_in)

        if 'answer' in data_json:
            answer = data_json['answer'].upper()
            stripped_answer = ''.join(answer.split())  # Answer without whitespace

            if not answer is None:
                if len(stripped_answer) in range(3, 31) and answer.isalpha():
                    self.game_db[gid]['answer'] = answer
                    output = {'result': 'Success', 'message': 'Your game will begin shortly!'}
                else:
                    output = {'result': 'Failure', 'message': 'Your phrase must be between 3 and 30 alphabetical characters.'}
        else:
            output = {'result': 'Failure', 'message': 'Incoming data insufficient'}

        if not answer is None:
            if len(stripped_answer) in range(3, 31) and answer.isalpha():
                self.game_db[gid]['answer'] = answer
                output = {'result': 'Success', 'message': 'Your game will begin shortly!'}
            else:
                output = {'result': 'Error', 'message': 'Your phrase must be between 3 and 30 alphabetical characters.'}
        return json.dumps(output, encoding='latin-1')

    def assign_player_roles(self, uid1, uid2):
        if random.randint(0,1) == 0:
            guesser_uid = uid1
            creator_uid = uid2
        else:
            guesser_uid = uid2
            creator_uid = uid1

        return (guesser_uid, creator_uid)
