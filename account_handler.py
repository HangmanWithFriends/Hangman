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
            self.emails_to_uids[usermail] = str(new_uid)
            self.users[str(new_uid)] = {"usermail": usermail, 
                                    "hashed_pass": hashed_pass,
                                    "username": username,
                                    "friends": [],
                                    "incoming_friend_requests": []
                                    }

            result = {'errors':[], 'result':new_uid}
            
        return json.dumps(result)

    def get_guest_uid(self):
        userid = "g" + str(self.next_guest_user)
        self.users[userid] = {"username" : "Guest_" + str(self.next_guest_user)}
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

    def handle_new_friend_request(self, uid):
        cl = cherrypy.request.headers['Content-Length']
        data_json = cherrypy.request.body.read(int(cl))
        incoming_data = json.loads(data_json)
        is_friends = False

        if 'uid_requested' not in incoming_data:
            return json.dumps({"result":"Error", "errors" : ["Request must contain a 'uid_requested' key-value pair"]})

        uid_requested = incoming_data['uid_requested']
        if uid_requested not in self.users:
            return json.dumps({"result":"Error", "errors" : ["Friend requested uid is unknown to database"]})

        if uid not in self.users:
            return json.dumps({"result":"Error", "errors" : ["Request made by unknown user"]})

        #See if the uid being requested has already requested the uid requesting
        if uid_requested in self.users[uid]['incoming_friend_requests']:
            self.make_friends(uid, uid_requested)
            self.remove_pairs_pending_requests(uid, uid_requested)
            is_friends = True
        else:
            self.users[uid_requested]['incoming_friend_requests'].append(uid)
            self.users[uid]['outgoing_friends_requests'].append(uid_requested)

        return json.dumps({"result":"Success", "is_friends" : is_friends, "errors":[]})

    def handle_friend_request_reponse(self, uid):
        cl = cherrypy.request.headers['Content-Length']
        data_json = cherrypy.request.body.read(int(cl))
        incoming_data = json.loads(data_json)
        requester_uid = None
        is_accepted = None

        if 'requester_uid' not in incoming_data:
            return json.dumps({"result":"Error", "errors" : ["Request must contain a 'requester_uid' key-value pair"]})
        else:
            requster_uid = incoming_data['reqeuster_uid']

        if requester_uid not in self.users:
            return json.dumps({"result":"Error", "errors" : ["Requester uid is unknown to database"]})

        if 'is_accepted' not in incoming_data:
            return json.dumps({"result":"Error", "errors" : ["Request must contain a 'is_accepted' key-value pair"]})
        else:
            try:
                is_accepted = bool(incoming_data['is_accepted'])
            except:
                return json.dumps({"result":"Error", "errors" : ["The value of 'is_accepted' must be of type boolean"]})

        if uid not in self.users:
            return json.dumps({"result":"Error", "errors" : ["Post for friend request response made by unknown user"]})

        if is_accepted:
            self.make_friends(uid, requester_uid)

        self.remove_pairs_pending_requests(uid, requester_uid)

    def handle_friend_delete(self, uid):
        cl = cherrypy.request.headers['Content-Length']
        data_json = cherrypy.request.body.read(int(cl))
        incoming_data = json.loads(data_json)
        uid_to_delete = None

        if 'uid_to_delete' not in incoming_data:
            return json.dumps({"result" : "Error", "errors" : ["Request must contain a 'uid_to_delete' key-value pair"]})
        else:
            uid_to_delete = incoming_data['uid_to_delete']

        if uid not in self.users:
            return json.dumps({"result" : "Error", "errors" : ["Requester uid is unknown to database"]})

        self.delete_friendship(uid, uid_to_delete)
        self.remove_pairs_pending_requests(uid, uid_to_delete)
        return json.dumps({"result" : "Success", "errors" : []})


    def make_friends(self, uid1, uid2):
        self.users[uid1]['friends'].append(uid2)
        self.users[requester_uid2]['friends'].append(uid1)

    def delete_friendship(self, uid1, uid2):
        if uid2 in self.users[uid1]['friends']:
            self.users[uid1]['friends'].remove(uid2)
        if uid1 in self.users[uid2]['friends']:
            self.users[uid2]['friends'].remove(uid1)

    def remove_pairs_pending_requests(self, uid1, uid2):
        if uid2 in self.users[uid1]['incoming_friend_requests']:
            self.users[uid1]['incoming_friend_requests'].remove(uid2)
        if uid2 in self.users[uid1]['outgoing_friend_requests']:
            self.users[uid1]['outgoing_friend_requests'].remove(uid2)
        if uid1 in self.users[uid2]['incoming_friend_requests']:
            self.users[uid2]['incominig_friend_requests'].remove(uid1)
        if uid1 in self.users[uid2]['outgoing_friend_requests']:
            self.users[uid2]['outgoing_friend_requests'].remove(uid1)

    def hash_pwd(self, pwd):
        hashed = hashlib.sha224(pwd).hexdigest()
        return hashed
