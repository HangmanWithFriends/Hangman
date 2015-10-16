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
import hashlib

class Account_Handler():
    
    def __init__(self, db):
        self.db = db
        self.emails_to_uids = db['emails_to_uids']
        self.users = db['users']
        #take max of list of existing users joined with the list containing 0, will be 1 for new db
        self.next_registered_user = None
        self.next_guest_user = 1

        self.find_next_user_id()

    
    def handle_login_request(self, usermail=None, password=None):
        result={'result':"Success", 'errors':[]}
        if usermail not in self.emails_to_uids:
            result['result'] = "Error"
            result['errors'].append("Invalid email/password combination")
        else:
            expected_hash = self.users[self.emails_to_uids[usermail]]['hashed_pass']
            hashed_incoming = self.hash_pwd(pwd) 
            if hashed_incoming != expected_hash:
                result['result'] = "Error"
                result['errors'].append("Invalid email/password combination")
            else:
                result['result'] = self.emails_to_uids[usermail]
                result['errors'] = []

        return json.dumps(result)

    def handle_register_request(self, usermail=None, password=None, username=None):

        #TODO jhamilt5: update both self.users with all info and uid key
        #and also update self.emails_to_uids with key usermail and value uid
        cl = cherrypy.request.headers['Content-Length']
        data_json = cherrypy.request.body.read(int(cl))
        data = json.loads(data_json)

        pwd = data["password"]
        usermail = data["usermail"]
        hashed_pass = self.hash_pwd(pwd)
        username = data["username"]

        if usermail in self.emails_to_uids:
            result = {'errors':['Email already in use'], 'result':None}
        else:
            new_uid = self.find_next_user_id()
            self.emails_to_uids[usermail] = new_uid
            self.users[new_uid] = {"usermail": usermail, 
                                    "hashed_pass": hashed_pass,
                                    "username": username}

            result = {'errors':[], 'result':new_uid}
            
        return json.dumps(result)
   
    def get_guest_uid(self):
        userid = "g" + str(self.next_guest_user)
        self.users[userid] = {"name" : "Guest_" + str(self.next_guest_user)}
        self.next_guest_user += 1
        guest_info = {'uid' : userid}
        guest_info['errors'] = []
        return json.dumps(guest_info)

    #Looks at any existing uids in the self.db[users] and returns the highest + 1
    def find_next_user_id(self):
        if self.next_registered_user:
            to_return = self.next_registered_user
            self.next_registered_user += 1
            return to_return
        elif len(self.users) is 0:
            self.next_registered_user = 2
            return 1
        else:
            to_return = max(self.users, key=int) + 1
            self.next_registered_user = to_return + 1
            return to_return

    def hash_pwd(self, pwd):
        hashed = hashlib.sha224(pwd).hexdigest()
        return hashed
