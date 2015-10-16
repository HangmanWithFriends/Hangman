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

    
    def handle_login_request(self):
        result={'result':"Success", 'errors':[]}
        
        cl = cherrypy.request.headers['Content-Length']
        data_json = cherrypy.request.body.read(int(cl))
        incoming_data = json.loads(data_json)

        if 'usermail' not in incoming_data:
            result = {'result':'Error', 'errors':["'usermail' is a required field in a login post"]}
            return json.dumps(result)
        if 'password' not in incoming_data:
            result = {'result':'Error', 'errors':["'password' is a required field in a login post"]}
            return json.dumps(result)
        
        if incoming_data['usermail'] not in self.emails_to_uids:
            result['result'] = "Error"
            result['errors'].append("Invalid email/password combination")
        else:
            expected_hash = self.users[self.emails_to_uids[incoming_data['usermail']]]['hashed_pass']
            hashed_incoming = self.hash_pwd(incoming_data['password']) 
            if hashed_incoming != expected_hash:
                result['result'] = "Error"
                result['errors'].append("Invalid email/password combination")
            else:
                result['result'] = self.emails_to_uids[incoming_data['usermail']]
                result['errors'] = []

        return json.dumps(result)

    def handle_register_request(self, usermail=None, password=None, username=None):
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
    
    def find_next_user_id(self):
        if self.next_registered_user:
            to_return = self.next_registered_user
            self.next_registered_user += 1
            return to_return
        else:
            to_return = 0
            for uid in self.users:
                try:
                    intuid = int(uid)
                    if to_return < intuid:
                        to_return = intuid
                except:
                    pass

            to_return += 1
            self.next_registered_user = to_return + 1
            return to_return

    def hash_pwd(self, pwd):
        hashed = hashlib.sha224(pwd).hexdigest()
        return hashed
