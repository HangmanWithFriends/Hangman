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
        self.emails_to_uids = db['emails_to_uids']
        self.users = db['users']
        #take max of list of existing users joined with the list containing 0, will be 1 for new db
        self.next_registered_user = self.find_first_new_user_id()
        self.next_guest_user = 1
    
    def handle_login_request(self):
        result={'result':"Success", 'errors':[]}
        
        incoming_data =  json.loads(cherrypy.request.body.read())
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
            expected_hash = self.users[self.emails_to_uids[usermail]]['hashed_pass']
            hashed_incoming = self.hash_pwd(incoming_data['password']) 
            if hashed_incoming != expected_hash:
                result['result'] = "Error"
                result['errors'].append("Invalid email/password combination")
            else:
                result['uid'] = self.emails_to_uids['usermail']

        return json.dumps(result)

    def handle_register_request(self, usermail=None, password=None, username=None):
        #TODO jhamilt5: update both self.users with all info and str(uid) key
        #and also update self.emails_to_uids with key usermail and value uid
        uid = str(self.get_next_uid())
        hashed_pass = self.hash_pwd(password)
        result = {'errors':[]}
        return json.dumps(result)
   
    def get_guest_uid(self):
        userid = "g" + str(self.next_guest_user)
        self.users[userid] = {"name" : "Guest_" + str(self.next_guest_user)}
        self.next_guest_user += 1
        guest_info = {'uid' : userid}
        guest_info['errors'] = []
        return json.dumps(guest_info)
    
    def find_first_new_user_id(self):
        max_existing_uid = 0
        for key in self.users:
            if key[0] != 'g':
                if int(key) > max_existing_uid:
                    max_existing_uid = int(key)

        return max_existing_uid + 1

    #Looks at any existing uids in the self.db[users] and returns the highest + 1
    def get_next_user_id(self):
        to_return = self.next_registered_user
        self.next_registered_user += 1
        return to_return

    def hash_pwd(pwd):
        return md5.new(pwd).digest()
