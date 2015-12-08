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
import copy
from feed_handler import Feed_Handler

class Account_Handler():
    
    def __init__(self, db):
        self.db = db
        self.emails_to_uids = db['emails_to_uids']
        self.users = db['users']
        #take max of list of existing users joined with the list containing 0, will be 1 for new db
        self.next_registered_user = None
        self.next_guest_user = 1
        self.find_next_user_id()
        self.feedhandler = Feed_Handler(self.db)
    
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
            new_uid = str(self.find_next_user_id())
            self.users[new_uid] = {"usermail": usermail,
                                    "hashed_pass": hashed_pass,
                                    "username": username,
                                    "friends": [],
                                    "incoming_friend_requests": [],
                                    "outgoing_friend_requests": [],
                                    "profile_image" : None
                                    }

            result = {'errors':[], 'result':new_uid}
            self.emails_to_uids[usermail] = new_uid
    
        return json.dumps(result)

    def get_guest_uid(self):
        userid = "g" + str(self.next_guest_user)
        self.users[userid] = {"username" : "Guest_" + str(self.next_guest_user),
                              "hashed_pass" : None,
                              "usermail" : None,
                              "friends" : None,
                              "incoming_friend_requests" : None,
                              "outgoing_friend_requests" : None,
                              "profile_image" : None}
        self.next_guest_user += 1
        guest_info = {'uid' : userid, 'errors': []}
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

    def handle_new_friend_request(self, uid, uid_requested):
        is_friends = False

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
            if uid not in self.users[uid_requested]['incoming_friend_requests']:
                self.users[uid_requested]['incoming_friend_requests'].append(uid)
            if uid_requested not in self.users[uid]['outgoing_friend_requests']:
                self.users[uid]['outgoing_friend_requests'].append(uid_requested)

        raise cherrypy.HTTPRedirect('/lobby/' + str(uid))
        return json.dumps({"result":"Success", "is_friends" : is_friends, "errors":[]})

    def handle_friend_request_response(self, uid, requester_uid, response):
        #if response = "decline" is assumed
        is_accepted = False   
        if response == "accept":
            is_accepted = True
            
        
        if requester_uid not in self.users:
            return json.dumps({"result":"Error", "errors" : ["Requester uid is unknown to database"]})

        if uid not in self.users:
            return json.dumps({"result":"Error", "errors" : ["Post for friend request response made by unknown user"]})

        if is_accepted and (requester_uid in self.users[uid]['incoming_friend_requests']) and (uid in self.users[requester_uid]['outgoing_friend_requests']):
            self.make_friends(uid, requester_uid)

        self.remove_pairs_pending_requests(uid, requester_uid)
        
        raise cherrypy.HTTPRedirect("/lobby/" + str(uid))
        return json.dumps({"result":"Success", "errors": []})

    def handle_friend_delete(self, uid, unfriended_uid):
        if uid not in self.users:
            return json.dumps({"result" : "Error", "errors" : ["Requester uid is unknown to database"]})
        

        self.delete_friendship(uid, unfriended_uid)
        self.remove_pairs_pending_requests(uid, unfriended_uid)
        
        raise cherrypy.HTTPRedirect("/lobby/" + str(uid))
        return json.dumps({"result" : "Success", "errors" : []})
    
    def update_settings_request(self,uid):
        result={'result':"Success", 'errors':[]}
        
        cl = cherrypy.request.headers['Content-Length']
        data_json = cherrypy.request.body.read(int(cl))
        incoming_data = json.loads(data_json)

        if 'usermail' not in incoming_data:
            result = {'result':'Error', 'errors':["'usermail' is a required field in updating settings post"]}
            return json.dumps(result)
        if 'password' not in incoming_data:
            result = {'result':'Error', 'errors':["'password' is a required field in updating settings post"]}
            return json.dumps(result)
        
        if 'username' not in incoming_data:
            result = {'result':'Error', 'errors':["'username' is a required field in updating settings post"]}
            return json.dumps(result)
        
        else:
            expected_hash = self.users[uid]['hashed_pass']
            hashed_incoming = self.hash_pwd(incoming_data['password']) 
            if hashed_incoming != expected_hash:
                result['result'] = "Error"
                result['errors'].append("Invalid password")
            else:
                if incoming_data['usermail'] in self.emails_to_uids and incoming_data['usermail'] != incoming_data['old_usermail']:
                    result = {'result':'Error', 'errors':["email is already in use"]}
                    return json.dumps(result)   
                else:    
                    result['result'] = uid                                      
                    self.users[uid]["username"] = incoming_data['username']

                    if incoming_data['usermail'] != incoming_data['old_usermail']:
                        self.users[uid]["usermail"] = incoming_data['usermail']
                        self.emails_to_uids[incoming_data['usermail']] = str(uid)              
                        del self.emails_to_uids[incoming_data['old_usermail']]
                        
                    if incoming_data['newpassword'] != '':
                        hashed_pass = self.hash_pwd(incoming_data['newpassword']) 
                        self.users[uid]["hashed_pass"] = hashed_pass

                    result['errors'] = []

        return json.dumps(result)

    def upload_avatar(self, uid, img_file, submit):
        all_data = None

        while True:
            data = img_file.file.read(8192)
            if all_data:
                all_data += data
            else:
                all_data = data

            if not data:
                break

        size = len(all_data)
        file_extension = self.get_extension(img_file.filename.lower())
        filename = str(uid) + '.' + file_extension
        filepath = './img/' + filename

        saved_file = open(filepath, 'wb') 
        saved_file.write(all_data) 
        saved_file.close()

        self.users[uid]['profile_image'] = filename

        #raise cherrypy.HTTPRedirect('/settings/' + str(uid))

    def get_extension(self, filename):
        for ext in ['png', 'jpg', 'gif']:
            if filename.endswith(ext):
                return ext
        
        return 'png'

    def make_friends(self, uid1, uid2):
        if uid2 not in self.users[uid1]['friends']:
            self.users[uid1]['friends'].append(uid2)
        if uid1 not in self.users[uid2]['friends']:
            self.users[uid2]['friends'].append(uid1)
        
        self.feedhandler.post_new_friendship(uid1, uid2)

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
