'''
This is the main file to run from the command line 
to start up the CherryPy webserver. This will also 
house the dispatcher to handle HTTP(S) requests.
'''
import thread
import pickle
import cherrypy
import os
import time
import copy
import sys
from page_handler import Page_Handler
from game_handler import Game_Handler
from account_handler import Account_Handler
from createMockDB import createMockDB

def auto_save(db):
    old_db = copy.deepcopy(db)

    while True:
        time.sleep(5)

        # If a change has been made to the database, pickle it
        if old_db != db:
            f = 'HangmanDB.pickle'
            if len(sys.argv) > 1 and sys.argv[1] == '-d':
                f = "TestHangmanDB.pickle"
            pickle.dump(db, file(f, 'w'))
            old_db = copy.deepcopy(db)

def start_service():

    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    conf = {'global': 
                {
                    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                    'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
                    'server.socket_host':'0.0.0.0'
                }, 
            
            '/' : 
                {
                    'request.dispatch' : dispatcher, 
                },
            '/css': 
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': 'css'
                },
            '/js':
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': 'js'
                },
            '/img':
                {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': 'img'
                }
    }
    
    
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    
    if os.path.isfile('HangmanDB.pickle'):
        print 'loading db'
        db = pickle.load(file('HangmanDB.pickle'))
    else:
        db = { 'games':{}, 'users':{}, 'emails_to_uids':{}, 'username_words_to_uids':{}, 'username_word_starts_to_uids':{}, 'events':[] }
    
    if 'ai' not in db['users']:
        db['users']['ai'] = { 'usermail':"ai@watson.com",
                              'hashed_pass' : 'ai',
                              'username': "Computer",
                              'friends': [],
                              'incoming_friend_requests':[],
                              'outgoing_friend_requests':[],
                              'profile_image' : 'watson.jpg'
                            }

    if 'events' not in db: db['events'] = list()
    
    #Overwrite DB for testing
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        db = createMockDB()
    
    page_handler = Page_Handler(db)
    game_handler = Game_Handler(db)
    account_handler = Account_Handler(db)

    thread.start_new_thread(auto_save, (db,))

    connect_page_handler_dispatches(dispatcher, page_handler)
    connect_game_handler_dispatches(dispatcher, game_handler)
    connect_account_handler_dispatches(dispatcher, account_handler)
    
    cherrypy.quickstart(app)
    
def connect_page_handler_dispatches(dispatcher, page_handler):
    dispatcher.connect('default_login','/',controller=page_handler,action='get_login_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_login_page','/login',controller=page_handler, action='get_login_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_lobby_page','/lobby/{uid}',controller=page_handler, action='get_lobby_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_request_phrase_page','/phrase/{uid}/{gid}',controller=page_handler, action='get_request_phrase_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_register_page', '/register', controller=page_handler, action='get_register_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_guest_lobby_page','/guestlobby/{uid}',controller=page_handler, action='get_guest_lobby_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_guest_request_phrase_page','/guestphrase/{uid}/{gid}',controller=page_handler,action='get_guest_request_phrase_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_guest_game_page','/guestgame/{uid}/{gid}',controller=page_handler,action='get_guest_game_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_gameplay_page', '/gameplay/{uid}/{gid}',controller=page_handler,action='get_gameplay_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_wait_page', '/gameplay/{uid}/wait/{gid}', controller=page_handler, action='get_wait_html', conditions=dict(method=['GET']))
    dispatcher.connect('get_settings_page', '/settings/{uid}', controller=page_handler, action='get_settings_html', conditions=dict(method=['GET']))
    dispatcher.connect('get_manage_friends_html', '/manage_friends/{uid}',controller=page_handler, action='get_friends_management_html', conditions=dict(method=['GET']))
    dispatcher.connect('handle_manage_friends_search_html', '/manage_friends/{uid}',controller=page_handler, action='handle_friends_management_search_html', conditions=dict(method=['POST']))

def connect_game_handler_dispatches(dispatcher, game_handler):
    dispatcher.connect('get_dummy_game_JSON', '/dummygame/{gid}',controller=game_handler,action='get_dummy_game',conditions=dict(method=['GET']))
    dispatcher.connect('post_game_prompt', '/game/{uid}/prompt/{gid}',controller=game_handler,action='post_game_prompt',conditions=dict(method=['POST']))
    dispatcher.connect('post_game_request', '/game/{uid}/request',controller=game_handler,action='post_game_request',conditions=dict(method=['POST']))
    dispatcher.connect('get_game_request','/game/{uid}/request',controller=game_handler, action='get_game_request',conditions=dict(method=['GET']))
    dispatcher.connect('get_ai_game_request','/game/{uid}/ai/request',controller=game_handler, action='get_ai_game_request',conditions=dict(method=['GET']))
    dispatcher.connect('post_guess_JSON', '/game/{uid}/{gid}', controller=game_handler,action='post_phrase_guess',conditions=dict(method=['POST']))
    dispatcher.connect('post_lguess_JSON', '/game/{uid}/{gid}/{letter}', controller=game_handler,action='post_letter_guess',conditions=dict(method=['POST']))
    dispatcher.connect('get_game_JSON', '/game/{gid}',controller=game_handler,action='get_game',conditions=dict(method=['GET']))

def connect_account_handler_dispatches(dispatcher, account_handler):
    dispatcher.connect('handle_login','/login',controller=account_handler, action='handle_login_request',conditions=dict(method=['POST']))
    dispatcher.connect('handle_register','/register',controller=account_handler, action='handle_register_request',conditions=dict(method=['POST']))
    dispatcher.connect('get_guest_uid','/get-guest-uid',controller=account_handler,action='get_guest_uid',conditions=dict(method=['GET']))
    dispatcher.connect('update_settings', '/settings/{uid}', controller=account_handler, action='update_settings_request', conditions=dict(method=['POST']))
    dispatcher.connect('upload_avatar', '/upload/{uid}/avatar', controller=account_handler, action='upload_avatar', conditions=dict(method=['POST']))
    dispatcher.connect('handle_new_friend_request', '/manage_friends/{uid}/make_request/{uid_requested}',controller=account_handler, action='handle_new_friend_request', conditions=dict(method=['POST']))
    dispatcher.connect('handle_friend_request_response', '/manage_friends/{uid}/respond_request/{requester_uid}/{response}',controller=account_handler, action='handle_friend_request_response', conditions=dict(method=['GET']))
    dispatcher.connect('handle_friend_delete', '/manage_friends/{uid}/delete_friendship/{unfriended_uid}',controller=account_handler, action='handle_friend_delete', conditions=dict(method=['GET']))

if __name__ == '__main__':
    start_service()
