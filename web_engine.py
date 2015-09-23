'''
This is the main file to run from the command line 
to start up the CherryPy webserver. This will also 
house the dispatcher to handle HTTP(S) requests.
'''

import cherrypy
import os
from page_handler import Page_Handler


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
    
    page_handler = Page_Handler()
    
    dispatcher.connect('default_login','/',controller=page_handler,action='get_login_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_login_page','/login',controller=page_handler, action='get_login_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_lobby_page','/lobby',controller=page_handler, action='get_lobby_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_request_phrase_page','/phrase',controller=page_handler, action='get_request_phrase_html',conditions=dict(method=['GET']))
    dispatcher.connect('handle_login','/login',controller=page_handler, action='handle_login_request',conditions=dict(method=['POST']))
    dispatcher.connect('get_game_page','/game/{game_id}',controller=page_handler, action='get_game_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_register_page', '/register', controller=page_handler, action='get_register_html',conditions=dict(method=['GET']))
    dispatcher.connect('handle_register','/register',controller=page_handler, action='handle_register_request',conditions=dict(method=['POST']))
    dispatcher.connect('get_guest_lobby_page','/guestlobby',controller=page_handler, action='get_guest_lobby_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_guest_request_phrase_page','/guestphrase',controller=page_handler,action='get_guest_request_phrase_html',conditions=dict(method=['GET']))
    dispatcher.connect('get_guest_game_page','/guestgame/{game_id}',controller=page_handler,action='get_guest_game_html',conditions=dict(method=['GET']))
    
    cherrypy.quickstart(app)
    
if __name__ == '__main__':
    start_service()
