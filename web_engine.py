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
from page_handler import Page_Handler
from game_handler import Game_Handler
from account_handler import Account_Handler

def auto_save(db):
    old_db = copy.deepcopy(db)

    while True:
        time.sleep(5)

        # If a change has been made to the database, pickle it
        if old_db != db:
            f = 'HangmanUsers.pickle'
            pickle.dump(db, file(f, 'w'))
            old_db = copy.deepcopy(db)

def start_service():

    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    conf = {'global': 
                {
                    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                    'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
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
    
    if os.path.isfile('HangmanUsers.pickle'):
        print 'loading db'
        db = pickle.load(file('HangmanUsers.pickle'))
    else:
        db = { 'games':{}, 'users':{}, 'emails_to_uids':{} }

    page_handler = Page_Handler(db)
    game_handler = Game_Handler(db)
    account_handler = Account_Handler(db)

    thread.start_new_thread(auto_save, (db,))
    
    dispatcher.connect('default_login','/',controller=page_handler,action='get_login_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_login_page','/login',controller=page_handler, action='get_login_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_lobby_page','/lobby/{uid}',controller=page_handler, action='get_lobby_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_request_phrase_page','/phrase/{uid}/{gid}',controller=page_handler, action='get_request_phrase_html',conditions=dict(method=['GET']))
    dispatcher.connect('handle_login','/login',controller=account_handler, action='handle_login_request',conditions=dict(method=['POST']))
    #dispatcher.connect('get_game_page','/gameplay/{uid}/{gid}/other',controller=page_handler, action='get_game_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_register_page', '/register', controller=page_handler, action='get_register_html',conditions=dict(method=['GET']))
    dispatcher.connect('handle_register','/register',controller=account_handler, action='handle_register_request',conditions=dict(method=['POST']))
    dispatcher.connect('get_guest_lobby_page','/guestlobby/{uid}',controller=page_handler, action='get_guest_lobby_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_guest_request_phrase_page','/guestphrase/{uid}/{gid}',controller=page_handler,action='get_guest_request_phrase_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_guest_game_page','/guestgame/{uid}/{gid}',controller=page_handler,action='get_guest_game_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_dummy_game_JSON', '/dummygame/{gid}',controller=game_handler,action='get_dummy_game',conditions=dict(method=['GET']))
    dispatcher.connect('get_gameplay_page', '/gameplay/{uid}/{gid}',controller=page_handler,action='get_gameplay_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_game_JSON', '/game/{gid}',controller=game_handler,action='get_game',conditions=dict(method=['GET']))

    dispatcher.connect('get_guest_uid','/get-guest-uid',controller=account_handler,action='get_guest_uid',conditions=dict(method=['GET']))
    
    dispatcher.connect('post_game_prompt', '/game/{uid}/prompt/{gid}',controller=game_handler,action='post_game_prompt',conditions=dict(method=['POST']))
    dispatcher.connect('post_game_request', '/game/{uid}/request',controller=game_handler,action='post_game_request',conditions=dict(method=['POST']))
    dispatcher.connect('get_game_request','/game/{uid}/request',controller=game_handler, action='get_game_request',conditions=dict(method=['GET']))
    dispatcher.connect('post_guess_JSON', '/game/{uid}/{gid}', controller=game_handler,action='post_guess',conditions=dict(method=['POST']))
    dispatcher.connect('get_wait_page', '/gameplay/{uid}/wait/{gid}', controller=page_handler, action='get_wait_html', conditions=dict(method=['GET']))
    
    cherrypy.quickstart(app)
        
if __name__ == '__main__':
    start_service()
