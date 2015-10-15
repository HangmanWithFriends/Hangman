'''
This class is responsible for sending back 
responses to account creation, update, and
login requests. This object is referenced
by the CherryPy dispatcher function.
'''

import os.path
import json
import string
import cherrypy

class Account_Handler():
    
    def __init__(self, db):
        self.db = db
        self.users = db['users']
        #take max of list of existing users joined with the list containing 0, will be 1 for new db
        self.next_user = max(self.users.keys() + [0]) + 1
        self.next_guest_user = 1
    
    def handle_login_request(self, usermail=None, password=None):
        result={'errors':[]}
        return json.dumps(result)

    def handle_register_request(self, usermail=None, password=None, username=None):
        result = {'errors':[]}
        return json.dumps(result)
   
    def get_guest_uid(self):
        userid = "g" + str(self.next_guest_user)
        self.users[userid] = {"name" : "guest"}
        self.next_guest_user += 1
        guest_info = {'uid' : userid}
        guest_info['errors'] = []
        return json.dumps(guest_info)
