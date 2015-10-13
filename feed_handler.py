'''
This class is responsible for handling requests
that want to update the news feed or query it.
'''

import os.path
import json
import requests
import cherrypy
import random
from jinja2 import Environment, FileSystemLoader
from time import sleep

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Feed_Handler():
    def __init__(self):
        self.text_file = "./news_feed/news.txt"

    def get_guest_feed(self, uid, num_lines):
        #get most recent min(num_lines, 20) events
        #foreach event, generate prhase and add to list
        #return json with errors:[] result:"Success", events: [event, event, event...] in most recent first order

    def get_user_feed(self, uid, num_lines):
        #find the uids of friends
        #read list of most recent games, new friendships looking for friend's or own uid
        #construct feed from this with most recent events from friends and if necessary just from recent events

    def post_game_result(self, guesser_uid, creator_uid, is_winner_guesser, phrase):
        #insert into db/txt file

    def post_new_friendship(self, uid1, uid2):
        #insert into db/txt file

    def find_name(self, requester_uid, name_uid):
        #open db connection
        # if requrester_uid = name_uid, return "You" and picture
        #query name table for first, last, picture given uid
        #resturn result of query

    def generate_friend_feed_item(self, uid1, uid2):
        #find_name(uid1) became friends with find_name(uid2)
        
    def generate_game_feed_item(self, guesser_uid, creator_uid, is_winner_guesser, phrase):
        #if is_winner_guesser:
            #ifind_name(guesser_uid) correctly find_name(creator_uid)'s phrase $phrase.toUpper
        #else
            #find_name(guesser_uid) got hung up on $find_name(creator_uid)'s word $phrase.toUpper
